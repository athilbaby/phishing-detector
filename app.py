from flask import Flask, render_template, request
from urllib.parse import urlparse
import joblib
import pandas as pd
import re

app = Flask(__name__)

# Load the model once when the app starts
model = joblib.load("phishing_model.pkl")

def extract_features(url):
    """Identical to training — MUST match or predictions are garbage."""
    url = str(url)
    features = {}
    features["url_length"] = len(url)
    features["num_dots"] = url.count(".")
    features["num_hyphens"] = url.count("-")
    ip_pattern = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
    features["has_ip"] = 1 if re.search(ip_pattern, url) else 0
    features["has_https"] = 1 if "https" in url.lower() else 0
    suspicious_words = ["login", "verify", "secure", "account",
                        "update", "signin", "banking", "confirm",
                        "webscr", "free", "winner", "prize", "paypal",
                        "ebay", "bank"]
    features["num_suspicious_words"] = sum(
        1 for word in suspicious_words if word in url.lower()
    )
    features["num_digits"] = sum(1 for c in url if c.isdigit())
    features["num_at"] = url.count("@")
    features["num_slashes"] = url.count("/")
    return features

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    confidence = None
    submitted_url = None

    if request.method == "POST":
        submitted_url = request.form["url"]

        # Extract features in the SAME column order as training
        feats = extract_features(submitted_url)
        feature_order = ["url_length", "num_dots", "num_hyphens", "has_ip",
                         "has_https", "num_suspicious_words", "num_digits",
                         "num_at", "num_slashes"]
        row = pd.DataFrame([feats])[feature_order]

        prediction = model.predict(row)[0]
        # predict_proba gives the probability for each class
        proba = model.predict_proba(row)[0]

        if prediction == 1:
            result = "Phishing"
            confidence = round(proba[1] * 100, 1)
        else:
            result = "Legitimate"
            confidence = round(proba[0] * 100, 1)

    return render_template("index.html", result=result,
                           confidence=confidence, url=submitted_url)

if __name__ == "__main__":
    app.run(debug=True)