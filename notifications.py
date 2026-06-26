"""
In-app notification renderer — displays alert banners on the dashboard.
"""
from flask import Flask, request, render_template_string

app = Flask(__name__)

TEMPLATE = """
<!DOCTYPE html>
<html>
<head><title>Notifications</title></head>
<body>
  <div id="banner">{{ message }}</div>
</body>
</html>
"""


@app.route("/notifications")
def notifications():
    # Display a one-time alert passed via query string (e.g. from email links)
    message = request.args.get("msg", "")
    return render_template_string(TEMPLATE, message=message)
