#!/usr/bin/env python3

import json
import time
import os
from datetime import datetime

import schedule
import fitbit


def refresh(token):
    print("Refreshing token")
    with open("token.json", "w") as f:
        f.write(json.dumps(token))


def main():
    print("Reading token")
    with open("token.json", "r") as f:
        data = json.loads(f.read())

    print("Creating client")
    authd_client = fitbit.Fitbit(
        os.environ["CLIENT_ID"],
        os.environ["CLIENT_SECRET"],
        access_token=data["access_token"],
        refresh_token=data["refresh_token"],
        expires_at=data["expires_at"],
        refresh_cb=refresh,
        system="en_AU",
    )

    print("Log Swim activity")
    authd_client.log_activity(
        {
            "activityId": "90024",
            "date": datetime.today().strftime("%Y-%m-%d"),
            "startTime": "01:00",
            "durationMillis": "3600000",
            "distance": "10.0",
        }
    )

    print("Log Meditating activity")
    authd_client.log_activity(
        {
            "activityId": "52001",
            "date": datetime.today().strftime("%Y-%m-%d"),
            "startTime": "02:00",
            "durationMillis": "3600000",
        }
    )

    print("Log Yoga activity")
    authd_client.log_activity(
        {
            "activityId": "7075",
            "date": datetime.today().strftime("%Y-%m-%d"),
            "startTime": "03:00",
            "durationMillis": "3600000",
        }
    )


if __name__ == "__main__":
    print("Creating schedule")
    schedule.every(int(os.environ["INTERVAL"])).minutes.do(main)

    while True:
        schedule.run_pending()
        time.sleep(1)
