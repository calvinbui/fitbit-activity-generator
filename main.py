#!/usr/bin/env python3
"""Create scheduled manual activities through the Google Health API."""

import json
import logging
import os
import signal
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

import google.auth.transport.requests
from google.auth.exceptions import RefreshError
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import AuthorizedSession
import schedule


HEALTH_API_BASE_URL = "https://health.googleapis.com/v4"
EXERCISE_URL = f"{HEALTH_API_BASE_URL}/users/me/dataTypes/exercise/dataPoints"
TOKEN_PATH = Path(os.environ.get("TOKEN_PATH", "token.json"))
TIME_ZONE = os.environ.get("TZ", "Australia/Sydney")

ACTIVITIES = (
    ("SWIMMING", 1, {"distanceMillimeters": 10_000}),
    ("MEDITATE", 2, {}),
    ("YOGA", 3, {}),
    ("RUNNING", 4, {"steps": "10000"}),
    ("CROSSFIT", 5, {}),
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

shutdown_requested = False


def signal_handler(sig, _frame):
    """Handle shutdown signals gracefully."""
    global shutdown_requested
    logger.info("Received signal %s, shutting down gracefully...", sig)
    shutdown_requested = True


def save_credentials(credentials, token_path=TOKEN_PATH):
    token_path.write_text(credentials.to_json(), encoding="utf-8")


def load_credentials(token_path=TOKEN_PATH):
    """Load and refresh persisted Google user credentials."""
    if not token_path.exists():
        raise FileNotFoundError(
            f"Google token file {token_path} does not exist. Run gather_keys_oauth2.py first."
        )

    credentials = Credentials.from_authorized_user_file(str(token_path))
    if not credentials.valid:
        if not credentials.refresh_token:
            raise ValueError(f"Google token file {token_path} has no refresh token. Re-authorize it.")
        logger.info("Refreshing Google access token")
        try:
            credentials.refresh(google.auth.transport.requests.Request())
        except RefreshError as error:
            raise RuntimeError("Unable to refresh Google credentials. Re-authorize this account.") from error
        save_credentials(credentials, token_path)

    return credentials


def activity_payload(exercise_type, start_time, metrics_summary):
    """Build a Google Health API exercise data point for a one-hour activity."""
    end_time = start_time + timedelta(hours=1)
    return {
        "dataSource": {"recordingMethod": "MANUAL"},
        "exercise": {
            "interval": {
                "startTime": start_time.isoformat(timespec="seconds"),
                "startUtcOffset": f"{int(start_time.utcoffset().total_seconds())}s",
                "endTime": end_time.isoformat(timespec="seconds"),
                "endUtcOffset": f"{int(end_time.utcoffset().total_seconds())}s",
            },
            "exerciseType": exercise_type,
            "metricsSummary": metrics_summary,
        },
    }


def log_activity(session, exercise_type, hour, metrics_summary, now):
    start_time = now.replace(hour=hour, minute=0, second=0, microsecond=0)
    payload = activity_payload(exercise_type, start_time, metrics_summary)
    logger.info("Log %s activity", exercise_type.title())
    response = session.post(EXERCISE_URL, json=payload, timeout=30)
    if not response.ok:
        raise RuntimeError(
            f"Google Health API rejected {exercise_type}: {response.status_code} {response.text}"
        )


def main():
    credentials = load_credentials()
    session = AuthorizedSession(credentials)
    now = datetime.now(ZoneInfo(TIME_ZONE))
    for exercise_type, hour, metrics_summary in ACTIVITIES:
        log_activity(session, exercise_type, hour, metrics_summary, now)


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)

    logger.info("Creating schedule")
    schedule.every(int(os.environ["INTERVAL"])).minutes.do(main)

    while not shutdown_requested:
        schedule.run_pending()
        time.sleep(1)

    logger.info("Shutdown complete")
    sys.exit(0)
