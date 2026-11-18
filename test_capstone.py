
"""
Provenance Guard — Capstone Extension Tests

Tests Shape B: Harden Against Failure.

Original tests:
1. Unexpected detector failure returns HTTP 503.
2. Internal detector errors are not exposed.
3. Detector failures are recorded in the audit log.
4. Invalid text still returns HTTP 400.

Milestone 6 regression tests:
5. Unexpected stylometry failure returns HTTP 503.
6. Unexpected scoring failure returns HTTP 503.
7. Downstream failure details are hidden and audited.
"""

import unittest
import uuid
from unittest.mock import patch

import app
import audit


class TestCapstoneExtension(unittest.TestCase):

    def setUp(self):
        self.client = app.app.test_client()

    def creator(self):
        return "capstone_test_" + uuid.uuid4().hex

    def submit(self, creator_id=None):
        return self.client.post(
            "/submit",
            json={
                "text": "This is a valid test submission.",
                "creator_id": creator_id or self.creator(),
            },
        )

    def test_detector_failure_returns_503(self):
        """Unexpected detector exceptions return HTTP 503."""
        with patch.object(
            app.detector,
            "model_signal",
            side_effect=RuntimeError("Simulated detector failure"),
        ):
            response = self.submit()

        self.assertEqual(response.status_code, 503)
        self.assertEqual(
            response.get_json()["error"],
            "detector_unavailable",
        )

    def test_failure_does_not_expose_internal_error(self):
        """Internal detector exception details remain private."""
        secret = "PRIVATE_INTERNAL_DETECTOR_ERROR"

        with patch.object(
            app.detector,
            "model_signal",
            side_effect=RuntimeError(secret),
        ):
            response = self.submit()

        self.assertEqual(response.status_code, 503)
        self.assertNotIn(
            secret,
            response.get_data(as_text=True),
        )

    def test_detector_failure_is_logged(self):
        """Unexpected detector failures create audit entries."""
        creator_id = self.creator()

        with patch.object(
            app.detector,
            "model_signal",
            side_effect=RuntimeError("Simulated failure"),
        ):
            response = self.submit(creator_id)

        self.assertEqual(response.status_code, 503)

        matching = [
            entry for entry in audit.read_entries()
            if entry.get("creator_id") == creator_id
            and entry.get("event") == "detector_failure"
        ]

        self.assertEqual(len(matching), 1)
        self.assertEqual(matching[0]["status"], "failed")
        self.assertEqual(
            matching[0]["error_type"],
            "RuntimeError",
        )

    def test_existing_invalid_text_behavior(self):
        """Empty text still returns HTTP 400."""
        response = self.client.post(
            "/submit",
            json={
                "text": "",
                "creator_id": self.creator(),
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.get_json()["error"],
            "invalid_text",
        )

    # ── Milestone 6 regression tests ───────────────────────────

    def test_stylometry_failure_returns_503(self):
        """Unexpected stylometry exceptions return HTTP 503."""
        with (
            patch.object(
                app.detector,
                "model_signal",
                return_value=0.5,
            ),
            patch.object(
                app.stylometry,
                "style_signal",
                side_effect=RuntimeError(
                    "Simulated stylometry failure"
                ),
            ),
        ):
            response = self.submit()

        self.assertEqual(response.status_code, 503)
        self.assertEqual(
            response.get_json()["error"],
            "analysis_unavailable",
        )

    def test_scoring_failure_returns_503(self):
        """Unexpected scoring exceptions return HTTP 503."""
        with (
            patch.object(
                app.detector,
                "model_signal",
                return_value=0.5,
            ),
            patch.object(
                app.stylometry,
                "style_signal",
                return_value=0.5,
            ),
            patch.object(
                app.scoring,
                "combine_signals",
                side_effect=RuntimeError(
                    "Simulated scoring failure"
                ),
            ),
        ):
            response = self.submit()

        self.assertEqual(response.status_code, 503)
        self.assertEqual(
            response.get_json()["error"],
            "analysis_unavailable",
        )

    def test_downstream_failure_is_private_and_logged(self):
        """Downstream failures must be private and auditable."""
        creator_id = self.creator()
        secret = "PRIVATE_INTERNAL_SCORING_ERROR"

        with (
            patch.object(
                app.detector,
                "model_signal",
                return_value=0.5,
            ),
            patch.object(
                app.stylometry,
                "style_signal",
                return_value=0.5,
            ),
            patch.object(
                app.scoring,
                "score_to_label",
                side_effect=RuntimeError(secret),
            ),
        ):
            response = self.submit(creator_id)

        self.assertEqual(response.status_code, 503)
        self.assertEqual(
            response.get_json()["error"],
            "analysis_unavailable",
        )
        self.assertNotIn(
            secret,
            response.get_data(as_text=True),
        )

        matching = [
            entry for entry in audit.read_entries()
            if entry.get("creator_id") == creator_id
            and entry.get("event") == "detector_failure"
        ]

        self.assertEqual(len(matching), 1)
        self.assertEqual(
            matching[0]["status"],
            "failed",
        )
        self.assertEqual(
            matching[0]["error_type"],
            "RuntimeError",
        )
        self.assertEqual(
            matching[0].get("reason"),
            "analysis_pipeline_error",
        )


if __name__ == "__main__":
    unittest.main()
