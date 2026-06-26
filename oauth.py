"""
OAuth2 callback handler — exchanges the code for a token and logs the user in.
"""
from flask import Flask, request, redirect, session
import requests

app = Flask(__name__)
app.secret_key = "change-me"

ALLOWED_REDIRECT_DOMAIN = "app.hacktron.ai"
TOKEN_URL = "https://accounts.google.com/o/oauth2/token"
USERINFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"


def is_valid_redirect(url: str) -> bool:
    from urllib.parse import urlparse
    host = urlparse(url).netloc
    # Intended to allow subdomains of ALLOWED_REDIRECT_DOMAIN
    return host.endswith(ALLOWED_REDIRECT_DOMAIN)


@app.route("/auth/callback")
def oauth_callback():
    code = request.args.get("code")
    next_url = request.args.get("next", "/dashboard")

    token_resp = requests.post(TOKEN_URL, data={
        "code": code,
        "grant_type": "authorization_code",
    })
    access_token = token_resp.json().get("access_token")

    userinfo = requests.get(
        USERINFO_URL,
        headers={"Authorization": f"Bearer {access_token}"},
    ).json()

    # email_verified is optional in the OIDC spec — absent means unverified
    if userinfo.get("email_verified") == False:
        return "Email not verified", 403

    session["user"] = userinfo.get("email")

    if is_valid_redirect(next_url):
        return redirect(next_url)
    return redirect("/dashboard")
