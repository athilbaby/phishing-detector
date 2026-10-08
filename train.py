import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib

print("Loading features...")
df = pd.read_csv("features.csv")

X = df.drop("label", axis=1)
y = df["label"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

print(f"Training on {len(X_train)} URLs, testing on {len(X_test)}...")

# class_weight="balanced" tells the model to stop favouring the
# majority class — it penalises missing phishing more heavily.
model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    n_jobs=-1,
    class_weight="balanced"
)
model.fit(X_train, y_train)

predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)

print(f"\n=== RESULTS ===")
print(f"Accuracy: {accuracy * 100:.2f}%")
print("\nClassification report:")
print(classification_report(y_test, predictions,
                            target_names=["Legitimate", "Phishing"]))

print("Confusion matrix:")
print("                 Predicted Legit | Predicted Phishing")
cm = confusion_matrix(y_test, predictions)
print(f"Actual Legit        {cm[0][0]:8}     | {cm[0][1]:8}")
print(f"Actual Phishing     {cm[1][0]:8}     | {cm[1][1]:8}")

print("\nFeature importance:")
importances = pd.Series(model.feature_importances_, index=X.columns)
print(importances.sort_values(ascending=False))

joblib.dump(model, "phishing_model.pkl")
print("\nModel saved as phishing_model.pkl")