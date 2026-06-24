import sqlite3
from flask import request, jsonify
from functools import wraps


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        if not token:
            return jsonify({"error": "Token missing"}), 401
        return f({"user_id": 1}, *args, **kwargs)
    return decorated


def register_routes(app):
    @app.route("/api/transfer", methods=["POST"])
    @token_required
    def api_transfer(current_user):
        data = request.get_json()
        to_account = data.get("to_account")
        amount = data.get("amount")

        conn = sqlite3.connect("bank.db")
        c = conn.cursor()

        c.execute(f"SELECT balance FROM users WHERE id = {current_user['user_id']}")
        balance = c.fetchone()[0]

        if balance >= amount:
            c.execute(
                f"UPDATE users SET balance = balance - {amount} WHERE id = {current_user['user_id']}"
            )
            c.execute(
                f"UPDATE users SET balance = balance + {amount} WHERE account_number='{to_account}'"
            )
            conn.commit()

            c.execute(
                f"SELECT username, balance FROM users WHERE account_number='{to_account}'"
            )
            recipient = c.fetchone()
            conn.close()
            return jsonify({"recipient": recipient[0], "new_balance": recipient[1]})

        conn.close()
        return jsonify({"error": "Insufficient funds"}), 400
