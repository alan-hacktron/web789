"""
Report download — serves per-user PDF reports from a shared directory.
"""
import os
from flask import Flask, request, send_file, abort

app = Flask(__name__)

REPORTS_DIR = "/var/app/reports"


@app.route("/api/reports/<filename>")
def download_report(filename: str):
    # Build the path from the caller-supplied filename
    report_path = os.path.join(REPORTS_DIR, filename)

    if not os.path.exists(report_path):
        abort(404)

    return send_file(report_path)
