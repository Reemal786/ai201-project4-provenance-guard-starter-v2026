
#!/usr/bin/env python3
"""
Provenance Guard — the web service.

Run:
    python app.py

Routes:
    POST /ping       Worked example. Do not change.
    POST /submit     Analyze and classify submitted text.
    POST /appeal     Appeal an existing classification.
    GET  /log        View audit log.
    GET  /health     Check service health.
"""

import time
import uuid

from flask import Flask, jsonify, request, g

import audit
import config
import detector
import scoring
import stylometry


app = Flask(__name__)


# ── CAPSTONE — Request monitoring ─────────────────────────────

@app.before_request
def start_request():
    """Assign a request ID and start a monotonic timer."""
    g.request_id = str(uuid.uuid4())
    g.start_time = time.perf_counter()


@app.after_request
def record_request(response):
    """
    Record request timing, status, and error category.

    Request logs are separate from the decision audit log.
    Submitted text and request bodies are not included.
    """
    start = getattr(g, "start_time", None)

    duration_ms = (
        round((time.perf_counter() - start) * 1000, 3)
        if start is not None
        else None
    )

    error_category = None

    if response.status_code >= 400:
        payload = response.get_json(silent=True)

        if isinstance(payload, dict):
            error_category = payload.get("error")

        if not error_category:
            error_category = "http_error"

    audit.log_request(
        request_id=getattr(
            g,
            "request_id",
            str(uuid.uuid4()),
        ),
        endpoint=request.path,
        method=request.method,
        status_code=response.status_code,
        duration_ms=duration_ms,
        error_category=error_category,
    )

    response.headers["X-Request-ID"] = g.request_id

    return response


# ── Rate limiting — UNIT 8 ────────────────────────────────────

class _LimiterOff:
    """Placeholder when rate limiting is disabled."""

    def limit(self, *args, **kwargs):
        return lambda view: view


limiter = _LimiterOff()

if config.RATE_LIMITING_ENABLED:
    from flask_limiter import Limiter
    from flask_limiter.util import get_remote_address

    def rate_limit_key():
        """Identify the caller for rate limiting."""
        payload = request.get_json(silent=True)

        if not isinstance(payload, dict):
            return get_remote_address()

        creator = payload.get("creator_id")

        if isinstance(creator, str) and creator.strip():
            return creator.strip()

        return get_remote_address()

    limiter = Limiter(
        key_func=rate_limit_key,
        app=app,
        storage_uri=config.RATE_LIMIT_STORAGE,
        default_limits=[],
    )

    @app.errorhandler(429)
    def rate_limited(exc):
        """Log requests rejected by the rate limiter."""
        payload = request.get_json(silent=True)

        if not isinstance(payload, dict):
            payload = {}

        audit.log_rejection(
            creator_id=payload.get(
                "creator_id",
                "unknown",
            ),
            reason="rate_limited",
            limit=str(exc.description),
        )

        return jsonify({
            "error": "rate_limited",
            "message": (
                "Too many submissions. Try again shortly."
            ),
            "limit": str(exc.description),
        }), 429


# ── Worked example — leave unchanged ─────────────────────────

@app.post("/ping")
def ping():
    """Example route provided by CodePath."""
    payload = request.get_json(silent=True) or {}

    return jsonify({
        "ok": True,
        "you_sent": payload.get("message"),
        "service": "provenance-guard",
    })


# ── Health check ──────────────────────────────────────────────

@app.get("/health")
def health():
    """Check service status and model loading."""
    loaded = detector._model is not None

    return jsonify({
        "ok": True,
        "detector_model": config.DETECTOR_MODEL,
        "detector_loaded": loaded,
        "rate_limiting": config.RATE_LIMITING_ENABLED,
        "log_entries": len(audit.read_entries()),
    })


# ── Submission endpoint ───────────────────────────────────────

@app.post("/submit")
@limiter.limit(
    f"{config.RATE_LIMIT_PER_MINUTE}/minute;"
    f"{config.RATE_LIMIT_PER_DAY}/day"
)
def submit():
    """
    Accept text, calculate detection signals, classify writing,
    and record the decision.
    """

    # Step 1: Read JSON.
    payload = request.get_json(silent=True)

    if not isinstance(payload, dict):
        return jsonify({
            "error": "invalid_request",
            "message": (
                "The request body must be a JSON object."
            ),
        }), 400

    # Step 2: Extract fields.
    text = payload.get("text")
    creator_id = payload.get("creator_id")

    # Step 3: Validate text.
    if not isinstance(text, str) or not text.strip():
        return jsonify({
            "error": "invalid_text",
            "message": (
                "The text field must be a non-empty string."
            ),
        }), 400

    # Step 4: Validate creator ID.
    if (
        not isinstance(creator_id, str)
        or not creator_id.strip()
    ):
        return jsonify({
            "error": "invalid_creator_id",
            "message": (
                "The creator_id field must be "
                "a non-empty string."
            ),
        }), 400

    text = text.strip()
    creator_id = creator_id.strip()

    # Step 5: Validate length.
    if len(text) > config.MAX_TEXT_LENGTH:
        return jsonify({
            "error": "text_too_long",
            "message": (
                f"The text must not exceed "
                f"{config.MAX_TEXT_LENGTH} characters."
            ),
        }), 413

    # Step 6: Generate content ID.
    content_id = str(uuid.uuid4())

    # Step 7: Calculate the detector signal.
    try:
        model_score = detector.model_signal(text)

    except ValueError as exc:
        audit.log_rejection(
            creator_id=creator_id,
            reason="detector_invalid_text",
            limit=str(exc),
        )

        return jsonify({
            "error": "text_too_short",
            "message": str(exc),
        }), 400

    # Original capstone extension: detector failure handling.
    except Exception as exc:
        audit.log_detector_failure(
            content_id=content_id,
            creator_id=creator_id,
            error_type=type(exc).__name__,
        )

        return jsonify({
            "error": "detector_unavailable",
            "message": (
                "The text detector is temporarily unavailable. "
                "Please try again later."
            ),
        }), 503

    # ── MILESTONE 6 IMPROVEMENT ────────────────────────────────
    #
    # Protect the downstream analysis pipeline.
    #
    # Previously, an unexpected exception in stylometry or
    # scoring could escape and produce HTTP 500.
    #
    # Now these failures produce a controlled HTTP 503
    # response and a categorized audit record.

    try:
        # Step 8: Calculate stylometry signal.
        style_score = stylometry.style_signal(text)

        # Step 9: Combine both signals.
        combined_score = scoring.combine_signals(
            model_score,
            style_score,
        )

        # Step 10: Determine classification.
        guess, label = scoring.score_to_label(
            combined_score
        )

        # Step 11: Calculate confidence.
        confidence = round(
            abs(combined_score - 0.5) * 2,
            4,
        )

    except Exception as exc:
        audit.log_detector_failure(
            content_id=content_id,
            creator_id=creator_id,
            error_type=type(exc).__name__,
            reason="analysis_pipeline_error",
        )

        return jsonify({
            "error": "analysis_unavailable",
            "message": (
                "The analysis service is temporarily "
                "unavailable. Please try again later."
            ),
        }), 503

    # Step 12: Record successful decision.
    audit.log_decision(
        content_id=content_id,
        creator_id=creator_id,
        guess=guess,
        model_score=model_score,
        style_score=style_score,
        combined_score=combined_score,
        label=label,
    )

    # Step 13: Return classification.
    return jsonify({
        "content_id": content_id,
        "guess": guess,
        "confidence": confidence,
        "label": label,
        "model_score": model_score,
        "style_score": style_score,
    })


# ── Appeal endpoint ───────────────────────────────────────────

@app.post("/appeal")
def appeal():
    """Allow a writer to challenge an existing classification."""

    # Step 1: Read JSON.
    payload = request.get_json(silent=True)

    if not isinstance(payload, dict):
        return jsonify({
            "error": "invalid_request",
            "message": (
                "The request body must be a JSON object."
            ),
        }), 400

    # Step 2: Extract fields.
    content_id = payload.get("content_id")
    reasoning = payload.get("reasoning")

    # Step 3: Validate content ID.
    if (
        not isinstance(content_id, str)
        or not content_id.strip()
    ):
        return jsonify({
            "error": "invalid_content_id",
            "message": "A valid content_id is required.",
        }), 400

    # Step 4: Validate reasoning.
    if (
        not isinstance(reasoning, str)
        or not reasoning.strip()
    ):
        return jsonify({
            "error": "invalid_reasoning",
            "message": (
                "Please explain why you are appealing "
                "this decision."
            ),
        }), 400

    content_id = content_id.strip()
    reasoning = reasoning.strip()

    # Step 5: Find original submission.
    entries = audit.entries_for(content_id)

    decisions = [
        entry
        for entry in entries
        if entry.get("status") == "decided"
    ]

    if not decisions:
        return jsonify({
            "error": "content_not_found",
            "message": (
                "No submission was found with this content ID."
            ),
        }), 404

    # Step 6: Retrieve creator ID.
    original_decision = decisions[0]
    creator_id = original_decision["creator_id"]

    # Step 7: Prevent duplicate appeals.
    already_appealed = any(
        entry.get("event") == "appeal"
        for entry in entries
    )

    if already_appealed:
        return jsonify({
            "error": "already_appealed",
            "message": (
                "An appeal has already been submitted "
                "for this content."
            ),
            "content_id": content_id,
            "status": "under_review",
        }), 409

    # Step 8: Record appeal.
    audit.log_appeal(
        content_id=content_id,
        creator_id=creator_id,
        reasoning=reasoning,
    )

    # Step 9: Confirm appeal.
    return jsonify({
        "content_id": content_id,
        "status": "under_review",
        "message": (
            "Your appeal has been recorded and "
            "is awaiting review."
        ),
    })


# ── Audit log ─────────────────────────────────────────────────

@app.get("/log")
def get_log():
    """Return audit log entries, most recent last."""
    limit = request.args.get("limit", type=int)

    entries = audit.read_entries(limit=limit)

    return jsonify({
        "count": len(entries),
        "entries": entries,
    })


# ── Start Flask ───────────────────────────────────────────────

def main():
    print(
        f"Provenance Guard on "
        f"http://{config.HOST}:{config.PORT}"
    )

    print(f"  detector model:  {config.DETECTOR_MODEL}")
    print(
        f"  rate limiting:   "
        f"{'ON' if config.RATE_LIMITING_ENABLED else 'off'}"
    )
    print(f"  audit log:       {config.AUDIT_LOG}")
    print(
        f"  request log:     "
        f"{config.LOG_DIR / 'requests.jsonl'}"
    )
    print()

    print("Check it's alive:")
    print(
        f"  curl http://{config.HOST}:{config.PORT}/health"
    )
    print()

    app.run(
        host=config.HOST,
        port=config.PORT,
        debug=config.DEBUG,
    )


if __name__ == "__main__":
    main()
