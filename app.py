from flask import Flask, request, redirect
import datetime
import csv
import os

app = Flask(__name__)

LOG_FILE = "logs.csv"

@app.route("/track")
def track():
    email = request.args.get("email", "unknown")
    action = request.args.get("action", "open")
    campaign = request.args.get("campaign", "general")
    redirect_to = request.args.get("redirect_to", "")

    # Log to CSV (simple + reliable)
    file_exists = os.path.isfile(LOG_FILE)

    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["timestamp", "email", "action", "campaign", "redirect"])
        writer.writerow([datetime.datetime.now(), email, action, campaign, redirect_to])

    # Redirect
    if action == "click" and redirect_to:
        return redirect(redirect_to)
    else:
        # 1x1 pixel for open tracking
        return "", 204

if __name__ == "__main__":
    app.run()