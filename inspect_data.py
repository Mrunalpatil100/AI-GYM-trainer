import pandas as pd

df = pd.read_csv("dataset/squats_landmarks.csv")

print(df[["frame", "knee_y"]].iloc[::10])