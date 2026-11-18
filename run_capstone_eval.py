
#!/usr/bin/env python3
"""
Provenance Guard — Capstone Formal Evaluation

Shape B: Harden Against Failure
Path B: Local with Logs

Evaluates five capstone acceptance criteria across three trials.

Usage:
    python run_capstone_eval.py --label before
    python run_capstone_eval.py --label after

This script uses Flask's test client and simulated detector failures.
It does not require a running Flask server or a loaded GPT-2 model.

Formal evaluation logs are isolated in a temporary directory.
Existing Project 4 audit and request logs are not modified.
"""

import argparse
import json
import tempfile
import uuid
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

import app
import audit
import config


CRITERIA = {
    1: {
        "name": "Controlled detector failure responses",
        "target": "3/3 cases return HTTP 503 and detector_unavailable",
    },
    2: {
        "name": "Internal error information protection",
        "target": "0/3 responses expose internal exception details",
    },
    3: {
        "name": "Detector failure audit logging",
        "target": "3/3 failures create complete audit records",
    },
    4: {
        "name": "Existing input validation",
        "target": "5/5 invalid submissions return HTTP 400 or 413",
    },
    5: {
        "name": "Structured request logging",
        "target": "3/3 failures create complete request records",
    },
}


def read_jsonl(path):
    """Read structured JSONL records from a file."""
    if not path.exists():
        return []

    records = []

    with path.open("r", encoding="utf-8") as file:
        for line in file:
            if line.strip():
                records.append(json.loads(line))

    return records


def unique_creator(criterion, trial, case):
    """Generate a unique creator ID for each test case."""
    return (
        f"capstone_c{criterion}_"
        f"t{trial}_case{case}_{uuid.uuid4().hex[:8]}"
    )


def simulate_failure(client, criterion, trial, case, message):
    """Submit valid text while simulating a detector exception."""
    creator_id = unique_creator(criterion, trial, case)

    with patch.object(
        app.detector,
        "model_signal",
        side_effect=RuntimeError(message),
    ):
        response = client.post(
            "/submit",
            json={
                "text": (
                    "This is a valid submission used to evaluate "
                    "graceful detector failure handling."
                ),
                "creator_id": creator_id,
            },
        )

    return response, creator_id


def make_result(case, passed, observed, expected):
    """Build one measurable evaluation result."""
    return {
        "case": case,
        "passed": bool(passed),
        "expected": expected,
        "observed": observed,
    }


def criterion_one(client, trial):
    """Verify controlled HTTP 503 responses."""
    results = []

    for case in range(1, 4):
        response, _ = simulate_failure(
            client,
            1,
            trial,
            case,
            f"Simulated detector failure {case}",
        )

        payload = response.get_json(silent=True) or {}

        passed = (
            response.status_code == 503
            and payload.get("error") == "detector_unavailable"
        )

        results.append(make_result(
            case,
            passed,
            {
                "status": response.status_code,
                "error": payload.get("error"),
            },
            {
                "status": 503,
                "error": "detector_unavailable",
            },
        ))

    return results


def criterion_two(client, trial):
    """Verify that internal exception details are not exposed."""
    results = []

    for case in range(1, 4):
        secret = (
            f"PRIVATE_INTERNAL_ERROR_"
            f"T{trial}_C{case}_{uuid.uuid4().hex}"
        )

        response, _ = simulate_failure(
            client,
            2,
            trial,
            case,
            secret,
        )

        body = response.get_data(as_text=True)
        payload = response.get_json(silent=True) or {}

        exposed = (
            secret in body
            or "Traceback (most recent call last)" in body
            or 'File "' in body
        )

        passed = (
            response.status_code == 503
            and payload.get("error") == "detector_unavailable"
            and not exposed
        )

        results.append(make_result(
            case,
            passed,
            {
                "status": response.status_code,
                "internal_details_exposed": exposed,
                "error": payload.get("error"),
                "response_body": body,
            },
            {
                "status": 503,
                "internal_details_exposed": False,
            },
        ))

    return results


def criterion_three(client, trial):
    """Verify detector failures are recorded in the audit log."""
    results = []

    for case in range(1, 4):
        response, creator_id = simulate_failure(
            client,
            3,
            trial,
            case,
            f"Audit test failure {case}",
        )

        entries = read_jsonl(config.AUDIT_LOG)

        matching = [
            entry
            for entry in entries
            if entry.get("creator_id") == creator_id
            and entry.get("event") == "detector_failure"
        ]

        entry = matching[-1] if matching else {}

        passed = (
            response.status_code == 503
            and len(matching) == 1
            and entry.get("status") == "failed"
            and entry.get("error_type") == "RuntimeError"
            and isinstance(entry.get("content_id"), str)
            and bool(entry.get("content_id"))
        )

        results.append(make_result(
            case,
            passed,
            {
                "status": response.status_code,
                "matching_entries": len(matching),
                "audit_entry": entry,
            },
            {
                "status": 503,
                "matching_entries": 1,
                "event": "detector_failure",
                "audit_status": "failed",
                "error_type": "RuntimeError",
                "content_id": "non-empty string",
            },
        ))

    return results


def criterion_four(client, trial):
    """Verify that invalid submissions are safely rejected."""
    results = []

    cases = [
        {
            "name": "empty_text",
            "body": {
                "text": "",
                "creator_id": unique_creator(4, trial, 1),
            },
            "expected_status": 400,
        },
        {
            "name": "missing_text",
            "body": {
                "creator_id": unique_creator(4, trial, 2),
            },
            "expected_status": 400,
        },
        {
            "name": "invalid_text_type",
            "body": {
                "text": 12345,
                "creator_id": unique_creator(4, trial, 3),
            },
            "expected_status": 400,
        },
        {
            "name": "missing_creator_id",
            "body": {
                "text": "Valid text without a creator ID.",
            },
            "expected_status": 400,
        },
        {
            "name": "excessively_long_text",
            "body": {
                "text": "A" * (config.MAX_TEXT_LENGTH + 1),
                "creator_id": unique_creator(4, trial, 5),
            },
            "expected_status": 413,
        },
    ]

    for index, case in enumerate(cases, 1):
        with patch.object(
            app.detector,
            "model_signal",
        ) as mocked_detector:
            response = client.post(
                "/submit",
                json=case["body"],
            )

        payload = response.get_json(silent=True) or {}

        detector_called = mocked_detector.called

        passed = (
            response.status_code == case["expected_status"]
            and isinstance(payload.get("error"), str)
            and bool(payload.get("error"))
            and not detector_called
        )

        results.append(make_result(
            index,
            passed,
            {
                "input_case": case["name"],
                "status": response.status_code,
                "error": payload.get("error"),
                "detector_called": detector_called,
            },
            {
                "status": case["expected_status"],
                "detector_called": False,
                "error": "non-empty error code",
            },
        ))

    return results


def criterion_five(client, trial):
    """Verify structured request logging for detector failures."""
    results = []

    for case in range(1, 4):
        response, _ = simulate_failure(
            client,
            5,
            trial,
            case,
            f"Request logging failure {case}",
        )

        request_id = response.headers.get("X-Request-ID")

        records = read_jsonl(audit.REQUEST_LOG)

        matching = [
            record
            for record in records
            if record.get("request_id") == request_id
        ]

        record = matching[-1] if matching else {}

        duration = record.get("duration_ms")

        duration_valid = (
            isinstance(duration, (int, float))
            and not isinstance(duration, bool)
            and duration >= 0
        )

        timestamp_valid = False

        if isinstance(record.get("timestamp"), str):
            try:
                datetime.fromisoformat(record["timestamp"])
                timestamp_valid = True
            except ValueError:
                pass

        passed = (
            response.status_code == 503
            and bool(request_id)
            and len(matching) == 1
            and record.get("endpoint") == "/submit"
            and record.get("method") == "POST"
            and record.get("status_code") == 503
            and record.get("error_category") == "detector_unavailable"
            and duration_valid
            and timestamp_valid
        )

        results.append(make_result(
            case,
            passed,
            {
                "status": response.status_code,
                "request_id": request_id,
                "matching_records": len(matching),
                "request_record": record,
            },
            {
                "status": 503,
                "matching_records": 1,
                "endpoint": "/submit",
                "method": "POST",
                "error_category": "detector_unavailable",
                "duration_ms": "non-negative number",
                "timestamp": "valid ISO timestamp",
            },
        ))

    return results


TEST_FUNCTIONS = {
    1: criterion_one,
    2: criterion_two,
    3: criterion_three,
    4: criterion_four,
    5: criterion_five,
}


def run_evaluation(trial_count):
    """Execute all five criteria across independent trials."""
    evaluation = []

    # Separate test evidence from existing Project 4 audit logs.
    with tempfile.TemporaryDirectory(
        prefix="provenance_capstone_"
    ) as temporary_directory:

        temporary_path = Path(temporary_directory)

        with (
            patch.object(
                config,
                "AUDIT_LOG",
                temporary_path / "audit.jsonl",
            ),
            patch.object(
                audit,
                "REQUEST_LOG",
                temporary_path / "requests.jsonl",
            ),
        ):
            client = app.app.test_client()

            for number, details in CRITERIA.items():
                print(f"\nCriterion {number}: {details['name']}")

                trials = []

                for trial in range(1, trial_count + 1):
                    # Each trial starts with its own clean evidence files.
                    config.AUDIT_LOG.unlink(missing_ok=True)
                    audit.REQUEST_LOG.unlink(missing_ok=True)

                    try:
                        cases = TEST_FUNCTIONS[number](
                            client,
                            trial,
                        )
                    except Exception as exc:
                        cases = [make_result(
                            "evaluation_error",
                            False,
                            {
                                "exception_type": type(exc).__name__,
                                "message": str(exc),
                            },
                            "Evaluation completes without an exception",
                        )]

                    passed_count = sum(
                        case["passed"] for case in cases
                    )

                    trial_passed = (
                        len(cases) == (5 if number == 4 else 3)
                        and passed_count == len(cases)
                    )

                    trials.append({
                        "trial": trial,
                        "passed": trial_passed,
                        "passed_cases": passed_count,
                        "total_cases": len(cases),
                        "cases": cases,
                    })

                    outcome = "PASS" if trial_passed else "FAIL"

                    print(
                        f"  Trial {trial}: {outcome} "
                        f"({passed_count}/{len(cases)})"
                    )

                criterion_met = (
                    len(trials) == 3
                    and all(trial["passed"] for trial in trials)
                )

                verdict = "MET" if criterion_met else "MISSED"

                print(f"  Verdict: {verdict}")

                evaluation.append({
                    "criterion": number,
                    "name": details["name"],
                    "target": details["target"],
                    "verdict": verdict,
                    "trials": trials,
                })

    return evaluation


def save_results(evaluation, label):
    """Save complete JSON evidence and a readable Markdown report."""
    config.RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    stamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    suffix = f"_{label}" if label else ""

    base = f"capstone_{stamp}{suffix}"

    json_path = config.RESULTS_DIR / f"{base}.json"
    md_path = config.RESULTS_DIR / f"{base}.md"

    report = {
        "project": "Provenance Guard",
        "extension": "Shape B - Harden Against Failure",
        "run_path": "Path B - Local with Logs",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "trial_count": 3,
        "evaluation_method": (
            "Flask test client with mocked detector exceptions"
        ),
        "criteria": evaluation,
    }

    json_path.write_text(
        json.dumps(report, indent=2),
        encoding="utf-8",
    )

    lines = [
        "# Provenance Guard — Capstone Evaluation",
        "",
        f"**Label:** {label or 'unlabeled'}",
        "",
        "**Extension:** Shape B — Harden Against Failure",
        "",
        "**Run Path:** Path B — Local with Logs",
        "",
        "**Method:** Flask test client with simulated detector failures",
        "",
        "Three trials were performed for each acceptance criterion.",
        "",
        "## Summary",
        "",
        "| Criterion | Target | Trial 1 | Trial 2 | Trial 3 | Verdict |",
        "|---|---|---|---|---|---|",
    ]

    for item in evaluation:
        trial_cells = []

        for trial in item["trials"]:
            trial_cells.append(
                f"{trial['passed_cases']}/{trial['total_cases']}"
            )

        lines.append(
            f"| {item['criterion']}. {item['name']} "
            f"| {item['target']} "
            f"| {' | '.join(trial_cells)} "
            f"| {item['verdict']} |"
        )

    lines += [
        "",
        "## Detailed Results",
        "",
    ]

    for item in evaluation:
        lines += [
            f"### Criterion {item['criterion']}: {item['name']}",
            "",
            f"**Target:** {item['target']}",
            "",
            f"**Verdict:** {item['verdict']}",
            "",
        ]

        for trial in item["trials"]:
            lines += [
                f"#### Trial {trial['trial']}",
                "",
                f"**Result:** "
                f"{'PASS' if trial['passed'] else 'FAIL'}",
                "",
                "```json",
                json.dumps(trial["cases"], indent=2),
                "```",
                "",
            ]

    lines += [
        "## Evaluation Limitations",
        "",
        "- Detector failures were simulated, not naturally occurring.",
        "- Tests used Flask's in-process test client.",
        "- Results do not measure real network latency.",
        "- The GPT-2 model was not required for these trials.",
        "- Request timing includes local Flask processing only.",
        "- Formal logs were isolated from existing project logs.",
        "- Additional live-service testing would provide broader evidence.",
        "",
    ]

    md_path.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    return json_path, md_path


def main():
    parser = argparse.ArgumentParser(
        description="Run the capstone acceptance criteria."
    )

    parser.add_argument(
        "--label",
        default="before",
        help="Evaluation label, such as before or after.",
    )

    parser.add_argument(
        "--trials",
        type=int,
        default=3,
        help="Number of trials; formal evaluation requires exactly 3.",
    )

    args = parser.parse_args()

    if args.trials != 3:
        parser.error(
            "The committed capstone criteria require exactly 3 trials."
        )

    if not args.label.replace("-", "").replace("_", "").isalnum():
        parser.error(
            "The label may contain only letters, numbers, - and _."
        )

    print("=" * 60)
    print("PROVENANCE GUARD — CAPSTONE EVALUATION")
    print("=" * 60)
    print("Extension: Shape B — Harden Against Failure")
    print("Run Path: Path B — Local with Logs")
    print("Trials per criterion: 3")
    print()

    evaluation = run_evaluation(args.trials)

    json_path, md_path = save_results(
        evaluation,
        args.label,
    )

    met = sum(
        item["verdict"] == "MET"
        for item in evaluation
    )

    print("\n" + "=" * 60)
    print(f"FINAL RESULT: {met}/5 CRITERIA MET")
    print("=" * 60)

    print(f"\nJSON evidence: {json_path}")
    print(f"Markdown report: {md_path}")

    print("\nReview all MISSED criteria before making changes.")


if __name__ == "__main__":
    main()
