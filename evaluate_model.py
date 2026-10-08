import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# 1. Load the dataset
df = pd.read_csv("dataset/rehab246_squat_positions_standardized.csv")

# 2. Separate features and target
X = df.drop(columns=[
    "is_correct",
    "movement",
    "subject_id",
    "repetition",
    "source_file",
    "frame",
    "timestamp_offset_ms"
])

y = df["is_correct"]

# 3. Create the SAME test split used during training
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# 4. Load our already-trained model
with open("squat_model.pkl", "rb") as file:
    model = pickle.load(file)

print("Trained model loaded successfully!")

# 5. Test the model
y_pred = model.predict(X_test)

# 6. Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)

print("\n===== MODEL TESTING =====")
print("Testing samples:", len(X_test))
print("Correct predictions:", (y_pred == y_test).sum())
print("Incorrect predictions:", (y_pred != y_test).sum())
print("Test Accuracy:", round(accuracy * 100, 2), "%")