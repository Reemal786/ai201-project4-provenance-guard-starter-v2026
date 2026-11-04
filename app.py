
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

import uuid

from flask import Flask, jsonify, request

import audit
import config
import detector
import scoring
import stylometry


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
    loaded = detector._model is not None

    return jsonify({
        "ok": True,
        "detector_model": config.DETECTOR_MODEL,
        "detector_loaded": loaded,
        "rate_limiting": config.RATE_LIMITING_ENABLED,
        "log_entries": len(audit.read_entries()),
    })


# ── Submission endpoint — MILESTONES 3, 4 AND 5 ───────────────────────────────

@app.post("/submit")
# @limiter.limit(f"{config.RATE_LIMIT_PER_MINUTE}/minute;{config.RATE_LIMIT_PER_DAY}/day")
def submit():
    """
    Accept text, calculate both detection signals,
    combine their scores, classify the writing,
    and record the decision.

    Expected JSON:
        {
            "text": "...",
            "creator_id": "..."
        }

    Returns:
        content_id
        guess
        confidence
        label
        model_score
        style_score
    """

    # Step 1: Read the JSON request.
    payload = request.get_json(silent=True)

    if not isinstance(payload, dict):
        return jsonify({
            "error": "invalid_request",
            "message": "The request body must be a JSON object.",
        }), 400

    # Step 2: Extract the text and creator ID.
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

    text = text.strip()
    creator_id = creator_id.strip()

    # Step 5: Generate a unique content ID.
    content_id = str(uuid.uuid4())

    # Step 6: Calculate both signals.
    model_score = detector.model_signal(text)
    style_score = stylometry.style_signal(text)

    # Step 7: Combine the signals.
    combined_score = scoring.combine_signals(
        model_score,
        style_score,
    )

    # Step 8: Assign the final classification.
    guess, label = scoring.score_to_label(combined_score)

    # Classification strength, not a probability of authorship.
    confidence = round(abs(combined_score - 0.5) * 2, 4)

    # Step 9: Record the complete decision.
    audit.log_decision(
        content_id=content_id,
        creator_id=creator_id,
        guess=guess,
        model_score=model_score,
        style_score=style_score,
        combined_score=combined_score,
        label=label,
    )

    # Step 10: Return the result.
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
    Allow a writer to challenge an existing classification.

    Expected JSON:
        {
            "content_id": "...",
            "reasoning": "..."
        }

    An appeal:
        1. Checks that the content ID exists.
        2. Retrieves the original creator ID.
        3. Records the appeal in the audit log.
        4. Sets the item's latest status to under_review.
        5. Returns a confirmation.

    The audit log is append-only. The original decision
    remains available for later review.
    """

    # Step 1: Read the JSON request.
    payload = request.get_json(silent=True)

    if not isinstance(payload, dict):
        return jsonify({
            "error": "invalid_request",
            "message": "The request body must be a JSON object.",
        }), 400

    # Step 2: Extract the appeal information.
    content_id = payload.get("content_id")
    reasoning = payload.get("reasoning")

    # Step 3: Validate the content ID.
    if not isinstance(content_id, str) or not content_id.strip():
        return jsonify({
            "error": "invalid_content_id",
            "message": "A valid content_id is required.",
        }), 400

    # Step 4: Validate the reasoning.
    if not isinstance(reasoning, str) or not reasoning.strip():
        return jsonify({
            "error": "invalid_reasoning",
            "message": "Please explain why you are appealing this decision.",
        }), 400

    content_id = content_id.strip()
    reasoning = reasoning.strip()

    # Step 5: Find the original submission.
    entries = audit.entries_for(content_id)

    decisions = [
        entry for entry in entries
        if entry.get("status") == "decided"
    ]

    if not decisions:
        return jsonify({
            "error": "content_not_found",
            "message": "No submission was found with this content ID.",
        }), 404

    # Step 6: Retrieve the creator ID from the original decision.
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
            "message": "An appeal has already been submitted for this content.",
            "content_id": content_id,
            "status": "under_review",
        }), 409

    # Step 8: Record the appeal and change its latest status.
    audit.log_appeal(
        content_id=content_id,
        creator_id=creator_id,
        reasoning=reasoning,
    )

    # Step 9: Confirm the appeal.
    return jsonify({
        "content_id": content_id,
        "status": "under_review",
        "message": "Your appeal has been recorded and is awaiting review.",
    })


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
