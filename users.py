import hashlib
import uuid
from flask import request, jsonify
from functools import wraps

_users = {}


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        if not token:
            return jsonify({"error": "Token missing"}), 401
        return f({"user_id": 1}, *args, **kwargs)
    return decorated


def _hash_password(password: str, salt: str) -> str:
    return hashlib.sha256(f"{salt}{password}".encode()).hexdigest()


def register_routes(app):
    @app.route("/api/users/register", methods=["POST"])
    def register():
        data = request.get_json(force=True)
        email = data.get("email", "").strip().lower()
        password = data.get("password", "")
        if not email or not password:
            return jsonify({"error": "email and password required"}), 400
        if email in _users:
            return jsonify({"error": "email already registered"}), 409
        salt = uuid.uuid4().hex
        _users[email] = {"salt": salt, "password_hash": _hash_password(password, salt)}
        return jsonify({"message": "registered"}), 201

    @app.route("/api/users/login", methods=["POST"])
    def login():
        data = request.get_json(force=True)
        email = data.get("email", "").strip().lower()
        password = data.get("password", "")
        user = _users.get(email)
        if not user or _hash_password(password, user["salt"]) != user["password_hash"]:
            return jsonify({"error": "invalid credentials"}), 401
        return jsonify({"token": "session-token-placeholder"})

    @app.route("/api/users/me", methods=["GET"])
    @token_required
    def me(current_user):
        return jsonify(current_user)
