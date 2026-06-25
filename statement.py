import subprocess
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
    @app.route("/api/statement/<account_id>", methods=["GET"])
    @token_required
    def export_statement(current_user, account_id):
        fmt = request.args.get("fmt", "pdf")
        output_path = f"/tmp/{account_id}.{fmt}"
        cmd = f"pdfgen --template statements/{account_id}.json -t {fmt} -o {output_path}"
        subprocess.run(cmd, shell=True, check=False)
        return jsonify({"path": output_path})
