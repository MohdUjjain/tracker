from flask import Flask, request, redirect
import requests
import datetime

app = Flask(__name__)

# 🔥 PUT YOUR APPS SCRIPT URL HERE
GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/YOUR_SCRIPT_ID/exec"


def log_to_sheets(email, action, campaign, redirect_to):
    try:
        requests.get(GOOGLE_SCRIPT_URL, params={
            "email": email,
            "action": action,
            "campaign": campaign,
            "redirect_to": redirect_to
        }, timeout=3)
    except Exception as e:
        print("Logging failed:", e)


@app.route("/track")
def track():
    email = request.args.get("email", "unknown")
    action = request.args.get("action", "open")
    campaign = request.args.get("campaign", "general")
    redirect_to = request.args.get("redirect_to", "")

    # ✅ Log (non-blocking mindset)
    log_to_sheets(email, action, campaign, redirect_to)

    print("Tracked:", email, action, campaign)

    # ✅ Redirect cleanly
    if action == "click" and redirect_to:
        return redirect(redirect_to)
    else:
        return "", 204  # for email open pixel


if __name__ == "__main__":
    app.run()
