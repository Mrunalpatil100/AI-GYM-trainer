import pandas as pd
from sklearn.model_selection import train_test_split

# 1. Load the labeled dataset
df = pd.read_csv("dataset/rehab246_squat_positions_standardized.csv")

print("Dataset loaded successfully!")

# 2. Check the dataset
print("\nDataset shape:")
print(df.shape)

# 3. Create X and y
# X = body/pose features
# y = correct or incorrect squat

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

print("\nX shape:", X.shape)
print("y shape:", y.shape)

# 4. Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("\nTraining data:", X_train.shape)
print("Testing data:", X_test.shape)
from sklearn.ensemble import RandomForestClassifier

# 5. Create the model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

# 6. Train the model
print("\nTraining model...")

model.fit(X_train, y_train)

print("Model training completed!")
# 5. Test the model on unseen data
y_pred = model.predict(X_test)

print("\nModel testing completed!")

print("First 10 predictions:")
print(y_pred[:10])

print("\nActual values:")
print(y_test.values[:10])
from sklearn.metrics import accuracy_score

accuracy = accuracy_score(y_test, y_pred)

print("\nModel Accuracy:", round(accuracy * 100, 2), "%")
import pickle

# Save the trained model
with open("squat_model.pkl", "wb") as file:
    pickle.dump(model, file)

print("\nModel saved successfully!")


