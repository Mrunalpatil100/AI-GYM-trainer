import pickle

# Load the saved model
with open("squat_model.pkl", "rb") as file:
    model = pickle.load(file)

print("Saved model loaded successfully!")
print("Model type:", type(model))
print("\nNumber of features:", model.n_features_in_)
print("\nFeature names:")
print(model.feature_names_in_)