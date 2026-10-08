import pandas as pd
from urllib.parse import urlparse
import re

def extract_features(url):
    """Turn a single URL string into a dictionary of numeric features."""
    url = str(url)  # safety: some rows might not be clean strings
    features = {}

    features["url_length"] = len(url)
    features["num_dots"] = url.count(".")
    features["num_hyphens"] = url.count("-")

    # IP address instead of a domain name
    ip_pattern = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
    features["has_ip"] = 1 if re.search(ip_pattern, url) else 0

    # HTTPS present anywhere in the string
    features["has_https"] = 1 if "https" in url.lower() else 0

    suspicious_words = ["login", "verify", "secure", "account",
                        "update", "signin", "banking", "confirm",
                        "webscr", "free", "winner", "prize", "paypal",
                        "ebay", "bank"]
    features["num_suspicious_words"] = sum(
        1 for word in suspicious_words if word in url.lower()
    )

    features["num_digits"] = sum(1 for char in url if char.isdigit())
    features["num_at"] = url.count("@")
    features["num_slashes"] = url.count("/")   # new: deep paths are suspicious

    return features


# --- Process the whole real dataset ---
if __name__ == "__main__":
    print("Loading dataset...")
    df = pd.read_csv("phishing_data.csv")

    # Convert text labels to numbers: bad=1 (phishing), good=0 (legit)
    df["label_num"] = df["Label"].map({"bad": 1, "good": 0})

    # Drop any rows where the URL or label is missing
    df = df.dropna(subset=["URL", "label_num"])

    print(f"Extracting features from {len(df)} URLs... (this takes a minute)")

    # Apply feature extraction to every URL
    feature_list = [extract_features(url) for url in df["URL"]]
    features_df = pd.DataFrame(feature_list)

    # Attach the numeric label
    features_df["label"] = df["label_num"].values

    features_df.to_csv("features.csv", index=False)

    print("Done! Features saved to features.csv")
    print(features_df.head())
    print("\nShape:", features_df.shape)