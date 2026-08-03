# Fitbit Activity Generator

Creates five manual activities (swimming, meditation, yoga, running, and CrossFit) every configured interval through the Google Health API. It replaces the deprecated Fitbit Web API.

## Google Cloud setup

1. In the Google Cloud project, enable the Google Health API.
1. Configure the OAuth consent screen, add each of the three Google accounts as a test user, and add the `googlehealth.activity_and_fitness.writeonly` scope.
1. Create or use a **Web application** OAuth client with `https://www.google.com` as its authorized redirect URI, as specified by the Google Health API setup guide.
1. Download the OAuth client JSON as `credentials.json`. Do not commit it or any generated token files.

## Authorize each account

Install the helper's dependencies on the machine where you will authorize the accounts:

```console
python -m venv .venv
.venv/bin/pip install -r requirements.txt
```

Run the helper once for each intended Google account. It prints an authorization URL; after you allow access, copy the complete final URL from the browser address bar and paste it into the helper.

```console
.venv/bin/python gather_keys_oauth2.py credentials.json token-account-1.json
.venv/bin/python gather_keys_oauth2.py credentials.json token-account-2.json
.venv/bin/python gather_keys_oauth2.py credentials.json token-account-3.json
```

All three token files use the same Google OAuth client, but each represents one account. The helper uses the registered HTTPS callback `https://www.google.com`.

## Run one container per account

Each container needs only its own token file. `TOKEN_PATH` is the path inside the container and defaults to `token.json`.

```console
docker build -t fitbit-activity-generator .
docker run -d --name fitbit-activities-1 \
  -e TZ=Australia/Sydney -e INTERVAL=360 \
  -e TOKEN_PATH=/usr/src/app/token.json \
  -v "$PWD/token-account-1.json:/usr/src/app/token.json:rw" \
  fitbit-activity-generator
```

Repeat with a distinct container name and token file for the other two accounts. The token mount is writable because Google access tokens expire hourly and the application persists refreshed credentials. Google test-mode refresh tokens expire after seven days; publish the consent screen before relying on this long-term.

The activities are dated for the configured `TZ` and are recorded at 01:00 through 05:00. Swimming records 10 m and running records 10,000 steps; the other activities have no extra metrics.
