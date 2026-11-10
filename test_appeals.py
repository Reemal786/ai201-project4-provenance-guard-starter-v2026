
#!/usr/bin/env python3
"""
Unit 8 — Acceptance Criterion 4

Run three trials of five valid appeals.
Verify HTTP 200, under_review status, and audit log entries.

Usage:
    python test_appeals.py
"""

import datetime as dt
import json
import uuid
from pathlib import Path

import requests

BASE_URL = "http://127.0.0.1:5000"
RESULTS_DIR = Path(__file__).resolve().parent / "results"

SAMPLE_TEXT = (
    "This is an original paragraph written to test the appeal workflow. "
    "The purpose of this submission is to verify that a writer can request "
    "a review of a classification and that the service records the appeal. "
    "The test checks the response status and the audit log entry."
)


def run_trial(trial_number):
    """Submit and appeal five unique pieces of content."""
    results = []

    for sample_number in range(1, 6):
        creator_id = (
            f"appeal_trial_{trial_number}_sample_{sample_number}_"
            f"{uuid.uuid4().hex[:8]}"
        )

        submission = requests.post(
            f"{BASE_URL}/submit",
            json={
                "text": SAMPLE_TEXT,
                "creator_id": creator_id,
            },
            timeout=90,
        )

        submission_data = submission.json()
        content_id = submission_data.get("content_id")

        result = {
            "trial": trial_number,
            "sample": sample_number,
            "creator_id": creator_id,
            "submit_status": submission.status_code,
            "content_id": content_id,
        }

        if submission.status_code != 200 or not content_id:
            result["passed"] = False
            result["error"] = "Submission failed"
            results.append(result)
            continue

        appeal = requests.post(
            f"{BASE_URL}/appeal",
            json={
                "content_id": content_id,
                "reasoning": (
                    "Requesting a review of this classification "
                    "to verify the appeal workflow."
                ),
            },
            timeout=30,
        )

        appeal_data = appeal.json()

        audit_response = requests.get(
            f"{BASE_URL}/log",
            params={"limit": 200},
            timeout=30,
        )

        audit_data = audit_response.json()
        audit_entries = audit_data.get("entries", [])

        audit_verified = any(
            entry.get("content_id") == content_id
            and entry.get("event") == "appeal"
            and entry.get("status") == "under_review"
            for entry in audit_entries
        )

        passed = (
            appeal.status_code == 200
            and appeal_data.get("status") == "under_review"
            and audit_verified
        )

        result.update({
            "appeal_status": appeal.status_code,
            "appeal_response": appeal_data,
            "audit_verified": audit_verified,
            "passed": passed,
        })

        results.append(result)

    return results


def main():
    RESULTS_DIR.mkdir(exist_ok=True)

    all_results = []

    for trial_number in range(1, 4):
        print(f"\nTrial {trial_number}")

        results = run_trial(trial_number)
        all_results.extend(results)

        for result in results:
            status = "PASS" if result["passed"] else "FAIL"
            print(f"  Sample {result['sample']}: {status}")

    passed_count = sum(result["passed"] for result in all_results)

    report = {
        "criterion": 4,
        "target": "Five valid appeals succeed per trial, across three trials.",
        "trials": 3,
        "total_appeals": 15,
        "passed": passed_count,
        "failed": 15 - passed_count,
        "results": all_results,
    }

    timestamp = dt.datetime.now().strftime("%Y-%m-%d_%H%M")
    output_path = RESULTS_DIR / f"appeal_run_{timestamp}.json"

    output_path.write_text(
        json.dumps(report, indent=2),
        encoding="utf-8",
    )

    print(f"\nPassed: {passed_count}/15")
    print(f"Report saved: {output_path}")


if __name__ == "__main__":
    main()
