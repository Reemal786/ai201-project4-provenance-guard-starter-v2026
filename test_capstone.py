
"""
Provenance Guard — Capstone Extension Tests

Tests the Shape B extension:
Graceful handling of unexpected detector failures.

These are preliminary implementation tests, not the formal
capstone acceptance-criteria trials.
"""

import unittest
from unittest.mock import patch

import app
import audit
import config


class TestCapstoneExtension(unittest.TestCase):

    def setUp(self):
        self.client = app.app.test_client()

    def test_detector_failure_returns_503(self):
        """An unexpected detector exception should return HTTP 503."""

        with patch.object(
            app.detector,
            "model_signal",
            side_effect=RuntimeError("Simulated detector failure"),
        ):
            response = self.client.post(
                "/submit",
                json={
                    "text": "This is a valid test submission.",
                    "creator_id": "capstone_test_001",
                },
            )

        self.assertEqual(response.status_code, 503)
        self.assertEqual(
            response.get_json()["error"],
            "detector_unavailable",
        )

    def test_failure_does_not_expose_internal_error(self):
        """Internal exception details must not appear in the response."""

        secret_message = "PRIVATE_INTERNAL_DETECTOR_ERROR"

        with patch.object(
            app.detector,
            "model_signal",
            side_effect=RuntimeError(secret_message),
        ):
            response = self.client.post(
                "/submit",
                json={
                    "text": "Another valid test submission.",
                    "creator_id": "capstone_test_002",
                },
            )

        self.assertEqual(response.status_code, 503)
        self.assertNotIn(
            secret_message,
            response.get_data(as_text=True),
        )

    def test_detector_failure_is_logged(self):
        """An unexpected detector failure should create an audit entry."""

        with patch.object(
            app.detector,
            "model_signal",
            side_effect=RuntimeError("Simulated failure"),
        ):
            response = self.client.post(
                "/submit",
                json={
                    "text": "This submission will trigger a simulated failure.",
                    "creator_id": "capstone_test_003",
                },
            )

        self.assertEqual(response.status_code, 503)

        entries = audit.read_entries()

        matching_entries = [
            entry for entry in entries
            if entry.get("creator_id") == "capstone_test_003"
            and entry.get("event") == "detector_failure"
        ]

        self.assertTrue(
            matching_entries,
            "Expected a detector_failure entry in the audit log.",
        )

        self.assertEqual(
            matching_entries[-1]["status"],
            "failed",
        )

    def test_existing_invalid_text_behavior(self):
        """Empty text should still return HTTP 400."""

        response = self.client.post(
            "/submit",
            json={
                "text": "",
                "creator_id": "capstone_test_004",
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.get_json()["error"],
            "invalid_text",
        )


if __name__ == "__main__":
    unittest.main()
