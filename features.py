import pandas as pd
from urllib.parse import urlparse
import re

def extract_features(url):
    """Turn a single URL string into a dictionary of numeric features."""
    features = {}

    # 1. Overall length — phishing URLs tend to be longer
    features["url_length"] = len(url)

    # 2. Number of dots — lots of subdomains (a.b.c.d.com) is suspicious
    features["num_dots"] = url.count(".")

    # 3. Number of hyphens — phishers pad with them (secure-login-verify)
    features["num_hyphens"] = url.count("-")

    # 4. Has an IP address instead of a domain name? Big red flag.
    #    This regex looks for four numbers separated by dots.
    ip_pattern = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
    features["has_ip"] = 1 if re.search(ip_pattern, url) else 0

    # 5. Uses HTTPS? Legit sites almost always do. (1 = yes, 0 = no)
    features["has_https"] = 1 if url.startswith("https") else 0

    # 6. Count of suspicious words commonly used to bait victims
    suspicious_words = ["login", "verify", "secure", "account",
                        "update", "signin", "banking", "confirm",
                        "webscr", "free", "winner", "prize"]
    features["num_suspicious_words"] = sum(
        1 for word in suspicious_words if word in url.lower()
    )

    # 7. Number of digits — phishing URLs often stuff in numbers
    features["num_digits"] = sum(1 for char in url if char.isdigit())

    # 8. Number of '@' symbols — a trick to hide the real destination
    features["num_at"] = url.count("@")

    # 9. Length of the domain part only
    try:
        domain = urlparse(url).netloc
        features["domain_length"] = len(domain)
    except Exception:
        features["domain_length"] = 0

    return features


# --- Test it on our dataset ---
if __name__ == "__main__":
    df = pd.read_csv("urls.csv")   # load the URLs we saved earlier

    # Apply extract_features to every URL, build a new table of features
    feature_list = [extract_features(url) for url in df["url"]]
    features_df = pd.DataFrame(feature_list)

    # Add the label column back on (phishing or not)
    features_df["label"] = df["label"]

    # Save for the training step
    features_df.to_csv("features.csv", index=False)

    print("Features extracted!")
    print(features_df)