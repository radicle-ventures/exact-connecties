import json
import time
import webbrowser
from urllib.parse import urlencode, urlparse, parse_qs

import requests

import config

TOKENS_FILE = "tokens.json"


def get_auth_url():
    params = {
        "client_id": config.CLIENT_ID,
        "redirect_uri": config.REDIRECT_URI,
        "response_type": "code",
        "force_login": 0,
    }
    return f"{config.AUTH_URL}?{urlencode(params)}"


def _capture_auth_code():
    """Ask the user to paste the redirect URL and extract the authorization code."""
    print("After approving, you will be redirected to a URL containing a 'code' parameter.")
    print("Copy the FULL URL from your browser's address bar and paste it here.\n")
    redirect_url = input("Paste the redirect URL: ").strip()
    qs = parse_qs(urlparse(redirect_url).query)
    code = qs.get("code", [None])[0]
    return code


def exchange_code(code):
    """Exchange authorization code for access + refresh tokens."""
    resp = requests.post(config.TOKEN_URL, data={
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": config.REDIRECT_URI,
        "client_id": config.CLIENT_ID,
        "client_secret": config.CLIENT_SECRET,
    })
    resp.raise_for_status()
    return resp.json()


def refresh_access_token(refresh_token):
    """Use refresh token to get a new access token."""
    resp = requests.post(config.TOKEN_URL, data={
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": config.CLIENT_ID,
        "client_secret": config.CLIENT_SECRET,
    })
    resp.raise_for_status()
    return resp.json()


def save_tokens(token_data):
    token_data["obtained_at"] = time.time()
    with open(TOKENS_FILE, "w") as f:
        json.dump(token_data, f, indent=2)


def load_tokens():
    try:
        with open(TOKENS_FILE) as f:
            return json.load(f)
    except FileNotFoundError:
        return None


def _is_expired(token_data):
    obtained = token_data.get("obtained_at", 0)
    expires_in = int(token_data.get("expires_in", 600))
    # Refresh 60 seconds before actual expiry
    return time.time() > obtained + expires_in - 60


def get_valid_token():
    """Return a valid access token, refreshing or re-authenticating as needed."""
    token_data = load_tokens()

    if token_data and not _is_expired(token_data):
        return token_data["access_token"]

    # Try refreshing
    if token_data and "refresh_token" in token_data:
        try:
            token_data = refresh_access_token(token_data["refresh_token"])
            save_tokens(token_data)
            print("Tokens refreshed successfully.")
            return token_data["access_token"]
        except requests.HTTPError:
            print("Refresh failed, starting new authorization flow...")

    # Full auth flow
    url = get_auth_url()
    print("\n=== Open this URL in your browser to authorize ===\n")
    print(url)
    print()
    try:
        webbrowser.open(url)
    except Exception:
        pass
    code = _capture_auth_code()
    if not code:
        raise RuntimeError("Did not receive authorization code from callback.")
    token_data = exchange_code(code)
    save_tokens(token_data)
    print("Authorization successful, tokens saved.")
    return token_data["access_token"]
