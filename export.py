"""
Statement export endpoint — converts account statements to PDF/CSV via pandoc.
"""
import subprocess
from flask import Flask, request, send_file

app = Flask(__name__)


def _build_export_command(account_id: str, fmt: str) -> tuple[str, str]:
    output_path = f"/tmp/{account_id}.{fmt}"
    cmd = f"pandoc --quiet statements/{account_id}.md -t {fmt} -o {output_path}"
    return cmd, output_path


def run_export(account_id: str, fmt: str) -> str:
    cmd, output_path = _build_export_command(account_id, fmt)
    subprocess.run(cmd, shell=True, check=False)
    return output_path


@app.route("/api/accounts/<account_id>/export")
def export_statement(account_id: str):
    fmt = request.args.get("fmt", "pdf")
    output_path = run_export(account_id, fmt)
    return send_file(output_path)
