# Fitbit Activity Generator

Create a swimming, yoga and meditation activity every 6 hours starting at 3 AM.

## Setup

1. Run `gather_keys_oauth2.py <CLIENT_ID> <CLIENT_SECRET>` to generate `token.json`
1. Run Docker container:
  - mounting `token.json` at `/usr/src/app/token.json`
  - add `TZ`, `INTERVAL`, `CLIENT_ID` and `CLIENT_SECRET` env vars
