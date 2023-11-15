# Fitbit Activity Generator

Create a swimming, yoga and meditation activity every 6 hours starting at 3 AM.

## Setup

1. Run `gather_keys_oauth2.py` to generate `token.json`
1. Run Docker container, while mounting `token.json` at `/usr/src/app/token.json`
