import unittest
from datetime import datetime
from zoneinfo import ZoneInfo

import main


class ActivityPayloadTest(unittest.TestCase):
    def test_activity_payload_has_explicit_interval_and_manual_source(self):
        start = datetime(2026, 8, 3, 1, tzinfo=ZoneInfo("Australia/Sydney"))

        payload = main.activity_payload("SWIMMING", start, {"distanceMillimeters": 10_000})

        self.assertEqual(payload["dataSource"], {"recordingMethod": "MANUAL"})
        self.assertEqual(payload["exercise"]["exerciseType"], "SWIMMING")
        self.assertEqual(payload["exercise"]["metricsSummary"], {"distanceMillimeters": 10_000})
        self.assertEqual(
            payload["exercise"]["interval"],
            {
                "startTime": "2026-08-03T01:00:00+10:00",
                "startUtcOffset": "36000s",
                "endTime": "2026-08-03T02:00:00+10:00",
                "endUtcOffset": "36000s",
            },
        )

    def test_activities_preserve_expected_types_and_metrics(self):
        self.assertEqual(
            [(activity_type, metrics) for activity_type, _hour, metrics in main.ACTIVITIES],
            [
                ("SWIMMING", {"distanceMillimeters": 10_000}),
                ("MEDITATE", {}),
                ("YOGA", {}),
                ("RUNNING", {"steps": "10000"}),
                ("CROSSFIT", {}),
            ],
        )


if __name__ == "__main__":
    unittest.main()
