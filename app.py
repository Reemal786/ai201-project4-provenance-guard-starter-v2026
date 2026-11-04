
#!/usr/bin/env python3
"""
Provenance Guard — the web service.

Run:
    python app.py

Routes:
    POST /ping       Worked example. Do not change.
    POST /submit     Submission endpoint (Milestones 3, 4, 5).
    POST /appeal     Appeal endpoint (Milestone 5).
    GET  /log        View audit log.
    GET  /health     Check service health.
"""

import uuid

from flask import Flask, jsonify, request

import audit
import config


app = Flask(__name__)


# ── Rate limiting — UNIT 8 ────────────────────────────────────────────────────
# Rate limiting stays disabled until Unit 8.
# To enable it later:
#   1. Set RATE_LIMITING_ENABLED = True in config.py.
#   2. Choose your rate limits.
#   3. Uncomment the @limiter.limit(...) decorator on /submit.


class _LimiterOff:
    """
    Placeholder limiter used while rate limiting is disabled.
    """

    def limit(self, *args, **kwargs):
        return lambda view: view


limiter = _LimiterOff()

if config.RATE_LIMITING_ENABLED:
    from flask_limiter import Limiter
    from flask_limiter.util import get_remote_address

    def rate_limit_key():
        """
        Identify the caller for rate limiting.
        """
        payload = request.get_json(silent=True)

        if not isinstance(payload, dict):
            return get_remote_address()

        creator = payload.get("creator_id")

        if isinstance(creator, str) and creator.strip():
            return creator

        return get_remote_address()

    limiter = Limiter(
        key_func=rate_limit_key,
        app=app,
        storage_uri=config.RATE_LIMIT_STORAGE,
        default_limits=[],
    )

    @app.errorhandler(429)
    def rate_limited(exc):
        """
        Log requests rejected by the rate limiter.
        """
        payload = request.get_json(silent=True)

        if not isinstance(payload, dict):
            payload = {}

        audit.log_rejection(
            creator_id=payload.get("creator_id", "unknown"),
            reason="rate_limited",
            limit=str(exc.description),
        )

        return jsonify({
            "error": "rate_limited",
            "message": "Too many submissions. Try again shortly.",
            "limit": str(exc.description),
        }), 429


# ── Worked example — leave unchanged ─────────────────────────────────────────

@app.post("/ping")
def ping():
    """
    Example route provided by CodePath.
    """
    payload = request.get_json(silent=True) or {}

    return jsonify({
        "ok": True,
        "you_sent": payload.get("message"),
        "service": "provenance-guard",
    })


# ── Health check — already implemented ───────────────────────────────────────

@app.get("/health")
def health():
    """
    Check whether the service is running and the model is loaded.
    """
    import detector

    loaded = detector._model is not None

    return jsonify({
        "ok": True,
        "detector_model": config.DETECTOR_MODEL,
        "detector_loaded": loaded,
        "rate_limiting": config.RATE_LIMITING_ENABLED,
        "log_entries": len(audit.read_entries()),
    })


# ── Submission endpoint — MILESTONE 3 ────────────────────────────────────────

@app.post("/submit")
# @limiter.limit(f"{config.RATE_LIMIT_PER_MINUTE}/minute;{config.RATE_LIMIT_PER_DAY}/day")
def submit():
    """
    Accept a piece of writing, calculate the model signal,
    log the submission, and return a JSON response.

    Expected JSON:
        {
            "text": "...",
            "creator_id": "..."
        }

    Milestone 3:
        - Validate the submitted text and creator ID.
        - Generate a unique content ID.
        - Calculate the GPT-2 model signal.
        - Record the submission in the audit log.
        - Return the required response fields.

    Milestone 4 will add the stylometry signal and combined score.
    Milestone 5 will add the final classification labels.
    """

    # Step 1: Read the JSON request.
    payload = request.get_json(silent=True)

    if not isinstance(payload, dict):
        return jsonify({
            "error": "invalid_request",
            "message": "The request body must be a JSON object.",
        }), 400

    # Step 2: Extract the submitted text and creator ID.
    text = payload.get("text")
    creator_id = payload.get("creator_id")

    # Step 3: Validate the text.
    if not isinstance(text, str) or not text.strip():
        return jsonify({
            "error": "invalid_text",
            "message": "The text field must be a non-empty string.",
        }), 400

    # Step 4: Validate the creator ID.
    if not isinstance(creator_id, str) or not creator_id.strip():
        return jsonify({
            "error": "invalid_creator_id",
            "message": "The creator_id field must be a non-empty string.",
        }), 400

    # Remove unnecessary whitespace.
    text = text.strip()
    creator_id = creator_id.strip()

    # Step 5: Generate a unique identifier for this submission.
    content_id = str(uuid.uuid4())

    # Step 6: Calculate the real model signal using GPT-2.
    import detector

    model_score = detector.model_signal(text)

    # Milestone 4 will replace this placeholder with a real style score.
    style_score = 0.0

    # Milestone 4 will combine both signals.
    # For now, preserve the real model score for logging.
    combined_score = model_score

    # Milestone 5 will calculate the final classification.
    guess = "unsure"
    confidence = 0.0
    label = "Classification pending: second signal not yet implemented."

    # Step 7: Record the submission in the audit log.
    audit.log_decision(
        content_id=content_id,
        creator_id=creator_id,
        guess=guess,
        model_score=model_score,
        style_score=style_score,
        combined_score=combined_score,
        label=label,
    )

    # Step 8: Return the submission result.
    return jsonify({
        "content_id": content_id,
        "guess": guess,
        "confidence": confidence,
        "label": label,
        "model_score": model_score,
        "style_score": style_score,
    })


# ── Appeal endpoint — MILESTONE 5 ─────────────────────────────────────────────

@app.post("/appeal")
def appeal():
    """
    Allow a writer to challenge a classification.

    Expected JSON:
        {
            "content_id": "...",
            "reasoning": "..."
        }

    TODO — Milestone 5:
        1. Check whether the content ID exists.
        2. Record the appeal using audit.log_appeal().
        3. Change the status to under_review.
        4. Return a confirmation.
    """

    payload = request.get_json(silent=True) or {}

    return jsonify({
        "error": "not_implemented",
        "message": "POST /appeal isn't built yet — see the TODO in app.py.",
        "you_sent": payload,
    }), 501


# ── Audit log — already implemented ──────────────────────────────────────────

@app.get("/log")
def get_log():
    """
    Return audit log entries, most recent last.
    """
    limit = request.args.get("limit", type=int)

    entries = audit.read_entries(limit=limit)

    return jsonify({
        "count": len(entries),
        "entries": entries,
    })


# ── Start the Flask application ───────────────────────────────────────────────

def main():
    print(f"Provenance Guard on http://{config.HOST}:{config.PORT}")
    print(f"  detector model:  {config.DETECTOR_MODEL}")
    print(f"  rate limiting:   {'ON' if config.RATE_LIMITING_ENABLED else 'off (unit 8)'}")
    print(f"  audit log:       {config.AUDIT_LOG}")
    print()

    print("Check it's alive:")
    print(f'  curl -X POST http://{config.HOST}:{config.PORT}/ping \\')
    print('    -H "Content-Type: application/json" \\')
    print('    -d \'{"message": "hello"}\'')
    print()

    # debug=True is intended for local development only.
    app.run(
        host=config.HOST,
        port=config.PORT,
        debug=config.DEBUG,
    )


if __name__ == "__main__":
    main()
