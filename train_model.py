import pandas as pd
import pickle

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report

# MODELS

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB


# =========================
# LOAD DATASET
# =========================

print("\nLoading Dataset...\n")

df = pd.read_csv("QR_phisingdatset.csv")

print("Dataset Loaded Successfully!\n")

print("Dataset Shape:", df.shape)

print("\nFirst 5 Rows:\n")

print(df.head())


# =========================
# FEATURES + LABELS
# =========================

X = df.drop("Result", axis=1)

y = df["Result"]


# =========================
# TRAIN TEST SPLIT
# =========================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


print("\nTraining Samples:", len(X_train))
print("Testing Samples:", len(X_test))


# =========================
# MODELS
# =========================

models = {

    "Logistic Regression": LogisticRegression(max_iter=1000),

    "Decision Tree": DecisionTreeClassifier(
        max_depth=10,
        random_state=42
    ),

    "Random Forest": RandomForestClassifier(
        n_estimators=200,
        max_depth=20,
        random_state=42
    ),

    "Naive Bayes": GaussianNB()

}


# =========================
# TRAINING + EVALUATION
# =========================

best_accuracy = 0
best_model = None
best_model_name = ""


print("\n==============================")
print("MODEL TRAINING STARTED")
print("==============================\n")


for name, model in models.items():

    print(f"\nTraining {name}...")

    # Train model
    model.fit(X_train, y_train)

    # Predictions
    y_pred = model.predict(X_test)

    # Accuracy
    accuracy = accuracy_score(y_test, y_pred)

    print(f"{name} Accuracy: {accuracy * 100:.2f}%")

    # Classification Report
    print("\nClassification Report:\n")

    print(classification_report(y_test, y_pred))

    # Best Model Selection
    if accuracy > best_accuracy:

        best_accuracy = accuracy
        best_model = model
        best_model_name = name


# =========================
# BEST MODEL
# =========================

print("\n==============================")
print("BEST MODEL SELECTED")
print("==============================\n")

print(f"Best Model: {best_model_name}")

print(f"Best Accuracy: {best_accuracy * 100:.2f}%")


# =========================
# SAVE BEST MODEL
# =========================

with open("models/model.pkl", "wb") as file:

    pickle.dump(best_model, file)


print("\nBest model saved successfully!")

print("\nSaved as: models/model.pkl")