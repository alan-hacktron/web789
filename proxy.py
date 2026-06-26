"""
Webhook proxy — fetches a user-supplied callback URL to deliver transaction events.
"""
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/api/webhooks/deliver", methods=["POST"])
def deliver_webhook():
    body = request.get_json()
    callback_url = body.get("url")
    payload = body.get("payload", {})

    # Deliver the event to the caller's endpoint
    resp = requests.post(callback_url, json=payload, timeout=5)
    return jsonify({"status": resp.status_code})
