
"""
Provenance Guard — Audit and Request Logging

The original audit log records classification decisions,
appeals, and rejected requests.

The capstone adds a separate structured JSONL log for
HTTP request monitoring and execution-time measurements.

Milestone 6:
Distinguish detector failures from downstream analysis
pipeline failures without exposing internal error messages.
"""

import json
import threading
from datetime import datetime, timezone

import config


_lock = threading.Lock()

# CAPSTONE — Separate request-level logging.
REQUEST_LOG = config.LOG_DIR / "requests.jsonl"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def log_decision(
    content_id: str,
    creator_id: str,
    guess: str | None = None,
    model_score: float | None = None,
    style_score: float | None = None,
    combined_score: float | None = None,
    label: str | None = None,
    status: str = "decided",
    **extra,
) -> dict:
    """
    Write a classification decision to the audit log.
    """
    entry = {
        "timestamp": _now(),
        "content_id": content_id,
        "creator_id": creator_id,
        "guess": guess,
        "model_score": model_score,
        "style_score": style_score,
        "combined_score": combined_score,
        "label": label,
        "status": status,
    }

    entry.update(extra)
    return _append(entry)


def log_appeal(
    content_id: str,
    creator_id: str,
    reasoning: str,
) -> dict:
    """
    Record an appeal without overwriting the original decision.
    """
    return _append({
        "timestamp": _now(),
        "content_id": content_id,
        "creator_id": creator_id,
        "event": "appeal",
        "status": "under_review",
        "reasoning": reasoning,
    })


def log_rejection(
    creator_id: str,
    reason: str,
    **extra,
) -> dict:
    """
    Record requests rejected before classification.
    """
    return _append({
        "timestamp": _now(),
        "creator_id": creator_id,
        "event": "rejected",
        "status": "rejected",
        "reason": reason,
        **extra,
    })


def log_detector_failure(
    content_id: str,
    creator_id: str,
    error_type: str,
    reason: str = "detector_unavailable",
) -> dict:
    """
    Record an unexpected detector or analysis failure.

    The default reason preserves the original detector
    failure behavior.

    Downstream analysis failures can specify:
        reason="analysis_pipeline_error"

    Submitted text and internal exception messages
    are never stored.
    """
    return _append({
        "timestamp": _now(),
        "content_id": content_id,
        "creator_id": creator_id,
        "event": "detector_failure",
        "status": "failed",
        "reason": reason,
        "error_type": error_type,
    })


# ── CAPSTONE — Structured Request Logging ─────────────────────

def log_request(
    request_id: str,
    endpoint: str,
    method: str,
    status_code: int,
    duration_ms: float | None,
    error_category: str | None = None,
) -> dict:
    """
    Record one HTTP request as structured JSON.

    Includes:
        timestamp
        request_id
        endpoint
        method
        status_code
        duration_ms
        error_category

    No submitted text or request body is stored.
    """
    entry = {
        "timestamp": _now(),
        "request_id": request_id,
        "endpoint": endpoint,
        "method": method,
        "status_code": status_code,
        "duration_ms": duration_ms,
        "error_category": error_category,
    }

    config.LOG_DIR.mkdir(parents=True, exist_ok=True)

    line = json.dumps(entry, ensure_ascii=False)

    with _lock:
        with REQUEST_LOG.open("a", encoding="utf-8") as f:
            f.write(line + "\n")

    return entry


# ── Original audit file operations ────────────────────────────

def _append(entry: dict) -> dict:
    config.LOG_DIR.mkdir(parents=True, exist_ok=True)
    line = json.dumps(entry, ensure_ascii=False)

    with _lock:
        with config.AUDIT_LOG.open("a", encoding="utf-8") as f:
            f.write(line + "\n")

    return entry


def read_entries(limit: int | None = None) -> list[dict]:
    """
    Read audit log entries, oldest first.

    Malformed JSON lines are skipped.
    """
    if not config.AUDIT_LOG.exists():
        return []

    entries = []

    for line in config.AUDIT_LOG.read_text(
        encoding="utf-8"
    ).splitlines():
        line = line.strip()

        if not line:
            continue

        try:
            entries.append(json.loads(line))
        except json.JSONDecodeError:
            continue

    return entries[-limit:] if limit else entries


def clear() -> int:
    """
    Clear the original audit log.

    Request-level logs are preserved separately.
    """
    count = len(read_entries())

    if config.AUDIT_LOG.exists():
        config.AUDIT_LOG.unlink()

    return count


def entries_for(content_id: str) -> list[dict]:
    """
    Return all audit entries associated with one content ID.
    """
    return [
        entry for entry in read_entries()
        if entry.get("content_id") == content_id
    ]
