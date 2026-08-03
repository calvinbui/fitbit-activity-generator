#!/usr/bin/env python3
"""Authorize one Google account and save credentials for the activity generator."""

import argparse
import json
import logging
from pathlib import Path

from google_auth_oauthlib.flow import Flow


SCOPE = "https://www.googleapis.com/auth/googlehealth.activity_and_fitness.writeonly"
# This is the callback URI specified by the Google Health API setup guide.
DEFAULT_REDIRECT_URI = "https://www.google.com"
AUTHORIZATION_URI = "https://accounts.google.com/o/oauth2/v2/auth"


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("credentials_file", type=Path, help="Downloaded Google OAuth client JSON")
    parser.add_argument("token_file", type=Path, help="Where to write this account's token JSON")
    return parser.parse_args()


def load_client_config(credentials_file):
    """Load Google OAuth client credentials using the Health API's v2 auth endpoint."""
    client_config = json.loads(credentials_file.read_text(encoding="utf-8"))
    client_type = "web" if "web" in client_config else "installed"
    client_config[client_type]["auth_uri"] = AUTHORIZATION_URI
    return client_config


def main():
    args = parse_args()
    flow = Flow.from_client_config(
        load_client_config(args.credentials_file),
        scopes=[SCOPE],
        redirect_uri=DEFAULT_REDIRECT_URI,
    )
    authorization_url, _ = flow.authorization_url(access_type="offline", prompt="consent")

    print("Open this URL in a browser and authorize the intended Google account:\n")
    print(authorization_url)

    authorization_response = input(
        "\nAfter approval, copy the complete URL from the browser address bar and paste it here: "
    ).strip()
    flow.fetch_token(authorization_response=authorization_response)

    args.token_file.write_text(flow.credentials.to_json(), encoding="utf-8")
    print(f"Saved credentials to {args.token_file}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
