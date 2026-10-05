import pandas as pd
import numpy as np

df = pd.read_csv("dataset/squats_landmarks.csv")


def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    ba = a - b
    bc = c - b

    cosine_angle = np.dot(ba, bc) / (
        np.linalg.norm(ba) * np.linalg.norm(bc)
    )

    cosine_angle = np.clip(cosine_angle, -1.0, 1.0)

    angle = np.degrees(np.arccos(cosine_angle))

    return angle


df["knee_angle"] = df.apply(
    lambda row: calculate_angle(
        [row["hip_x"], row["hip_y"], row["hip_z"]],
        [row["knee_x"], row["knee_y"], row["knee_z"]],
        [row["ankle_x"], row["ankle_y"], row["ankle_z"]]
    ),
    axis=1
)

print(df[["frame", "knee_angle"]].head(20))

print("\nMinimum knee angle:", round(df["knee_angle"].min(), 2))
print("Maximum knee angle:", round(df["knee_angle"].max(), 2))
print("Average knee angle:", round(df["knee_angle"].mean(), 2))