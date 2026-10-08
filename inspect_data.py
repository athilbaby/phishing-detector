import pandas as pd

# Load the real dataset
df = pd.read_csv("phishing_data.csv")

print("Shape (rows, columns):", df.shape)
print("\nColumn names:", list(df.columns))
print("\nFirst 5 rows:")
print(df.head())
print("\nLabel counts:")
# This shows how many of each label — change 'Label' if the column
# is named something else (we'll see from the output above)
print(df.iloc[:, -1].value_counts())