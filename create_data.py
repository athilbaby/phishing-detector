import pandas as pd

# A small starter dataset: real-looking examples of both classes.
# label: 1 = phishing, 0 = legitimate
data = {
    "url": [
        "https://www.google.com",
        "https://www.paypal.com/signin",
        "https://github.com/login",
        "https://www.amazon.com",
        "https://www.wikipedia.org",
        "https://www.microsoft.com",
        "https://www.bankofireland.com",
        "https://www.netflix.com/browse",
        "http://paypal-secure-login.verify-account.xyz-123.ru/login",
        "http://192.168.1.1/amazon/signin/update.php",
        "http://secure-paypaI-account.com/webscr?cmd=login",
        "http://free-gift-card.winner-prize.tk/claim",
        "http://bankofireland.account-verify.ml/login.html",
        "http://appleid.apple.com-verify.suspicious.ru/signin",
        "http://facebook-security-check.gq/recover",
        "http://update-your-account.netflix-billing.cf/login",
    ],
    "label": [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
}

df = pd.DataFrame(data)       # build a table from the dictionary
df.to_csv("urls.csv", index=False)   # save it to a file

print("Dataset created!")
print(df)