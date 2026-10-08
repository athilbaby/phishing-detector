# 🛡️ Phishing URL Detector

A machine-learning web application that classifies URLs as **phishing** or **legitimate**, trained on ~549,000 real-world URLs. Built with Python, scikit-learn, and Flask.

## Overview

Phishing attacks rely on deceptive URLs to trick users into giving up credentials. This project detects them using a Random Forest classifier that analyses the *structure* of a URL — no need to visit the (potentially dangerous) site.

## How it works

1. **Feature engineering** — each URL is converted into 9 numeric features that encode security signals (URL length, digit count, suspicious keywords, presence of an IP address, number of subdomains, etc.).
2. **Model** — a Random Forest classifier trained on ~549,000 labelled URLs from a public Kaggle dataset.
3. **Web app** — a Flask interface where you paste a URL and get a verdict with a confidence score.

## Results

| Metric | Value |
|---|---|
| Accuracy | ~83% |
| Phishing recall | 0.76 |

I deliberately applied **class balancing** to prioritise *catching phishing* over raw accuracy. In a security context, a missed phishing site (a user gets compromised) is far more costly than a false alarm on a legitimate site (a dismissible warning). This raised phishing recall from 0.64 to 0.76 — catching ~6,000 more threats in the test set — at the acceptable cost of more false positives.

**Most important features:** URL length, digit count, and suspicious-word count proved the strongest signals.

## Tech stack

- Python
- pandas (data processing)
- scikit-learn (Random Forest model)
- Flask (web interface)

## Running locally

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/phishing-detector.git
cd phishing-detector

# Set up a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt

# Download the dataset from Kaggle ("phishing site urls"),
# rename it to phishing_data.csv, then:
python process_data.py       # extract features
python train.py              # train the model
python app.py                # launch the web app
```

Then open `http://127.0.0.1:5000` in your browser.

## Dataset

Phishing Site URLs dataset (Kaggle) — ~549,000 labelled URLs. Not included in this repo due to size; download separately.

## Author

Athil Baby — MSc Cyber Security, National College of Ireland

## Disclaimer

Educational project. Not intended as a production security tool.