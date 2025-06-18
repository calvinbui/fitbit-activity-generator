#!/usr/bin/env python3
"""
Fitbit activity logger that automatically logs activities at scheduled intervals.
"""

import json
import logging
import time
import os
from datetime import datetime

import schedule
import fitbit

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def refresh(token):
    logger.info("Refreshing token")
    with open("token.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(token))


def hours_to_milliseconds(hours):
    return int(hours * 60 * 60 * 1000)


def main():
    logger.info("Reading token")
    with open("token.json", "r", encoding="utf-8") as f:
        data = json.loads(f.read())

    logger.info("Creating client")
    authd_client = fitbit.Fitbit(
        os.environ["CLIENT_ID"],
        os.environ["CLIENT_SECRET"],
        access_token=data["access_token"],
        refresh_token=data["refresh_token"],
        expires_at=data["expires_at"],
        refresh_cb=refresh,
        system="en_AU",
    )

    logger.info("Log Swim activity")
    authd_client.log_activity(
        {
            "activityId": "90024",
            "date": datetime.today().strftime("%Y-%m-%d"),
            "startTime": "01:00",
            "durationMillis": hours_to_milliseconds(1),
            "distance": "10.0",
        }
    )

    logger.info("Log Meditating activity")
    authd_client.log_activity(
        {
            "activityId": "52001",
            "date": datetime.today().strftime("%Y-%m-%d"),
            "startTime": "02:00",
            "durationMillis": hours_to_milliseconds(1),
        }
    )

    logger.info("Log Yoga activity")
    authd_client.log_activity(
        {
            "activityId": "7075",
            "date": datetime.today().strftime("%Y-%m-%d"),
            "startTime": "03:00",
            "durationMillis": hours_to_milliseconds(1),
        }
    )

    logger.info("Log Running activity")
    authd_client.log_activity(
        {
            "activityId": "90009",
            "date": datetime.today().strftime("%Y-%m-%d"),
            "startTime": "04:00",
            "durationMillis": hours_to_milliseconds(1),
            "distance": "10000.00",
            "distanceUnit": "Steps",
        }
    )

    logger.info("Log CrossFit activity")
    authd_client.log_activity(
        {
            "activityId": "91045",
            "date": datetime.today().strftime("%Y-%m-%d"),
            "startTime": "05:00",
            "durationMillis": hours_to_milliseconds(1),
        }
    )

    logger.info("Log sleep")
    now = datetime.now()
    authd_client.log_sleep(
        start_time=datetime(year=now.year, month=now.month, day=now.day, hour=6, minute=0),
        duration=hours_to_milliseconds(7),
    )


if __name__ == "__main__":
    logger.info("Creating schedule")
    schedule.every(int(os.environ["INTERVAL"])).minutes.do(main)

    while True:
        schedule.run_pending()
        time.sleep(1)
