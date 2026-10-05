import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("dataset/squats_landmarks.csv")

plt.plot(df["frame"], df["knee_y"])

plt.xlabel("Frame")
plt.ylabel("Knee Y")
plt.title("Squat Movement")

plt.show()