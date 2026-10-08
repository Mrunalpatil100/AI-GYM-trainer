import cv2
import mediapipe as mp
import pickle
import pandas as pd

# -----------------------------
# 1. Load trained ML model
# -----------------------------
with open("squat_model.pkl", "rb") as file:
    model = pickle.load(file)

print("✅ Squat model loaded successfully!")

# -----------------------------
# 2. Start MediaPipe Pose
# -----------------------------
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

pose = mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# -----------------------------
# 3. Open webcam
# -----------------------------
cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

if not cap.isOpened():
    print("❌ Camera could not be opened")
    exit()

print("✅ Camera opened successfully")
print("Press Q to quit")

# -----------------------------
# 4. Required landmarks
# -----------------------------
required_landmarks = {
    "LeftShoulder": mp_pose.PoseLandmark.LEFT_SHOULDER,
    "RightShoulder": mp_pose.PoseLandmark.RIGHT_SHOULDER,
    "LeftElbow": mp_pose.PoseLandmark.LEFT_ELBOW,
    "RightElbow": mp_pose.PoseLandmark.RIGHT_ELBOW,
    "LeftWrist": mp_pose.PoseLandmark.LEFT_WRIST,
    "RightWrist": mp_pose.PoseLandmark.RIGHT_WRIST,
    "LeftKnee": mp_pose.PoseLandmark.LEFT_KNEE,
    "RightKnee": mp_pose.PoseLandmark.RIGHT_KNEE,
    "LeftAnkle": mp_pose.PoseLandmark.LEFT_ANKLE,
    "RightAnkle": mp_pose.PoseLandmark.RIGHT_ANKLE,
    "LeftFootIndex": mp_pose.PoseLandmark.LEFT_FOOT_INDEX,
    "RightFootIndex": mp_pose.PoseLandmark.RIGHT_FOOT_INDEX,
    "LeftHip": mp_pose.PoseLandmark.LEFT_HIP,
    "RightHip": mp_pose.PoseLandmark.RIGHT_HIP,
}

# -----------------------------
# 5. Start webcam loop
# -----------------------------
while True:

    ret, frame = cap.read()

    if not ret:
        print("❌ Failed to get frame")
        break

    # Convert BGR → RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect pose
    results = pose.process(rgb_frame)

    if results.pose_landmarks:

        landmarks = results.pose_landmarks.landmark

        # -----------------------------
        # 6. Extract 42 features
        # -----------------------------
        features = []

        for name, landmark_id in required_landmarks.items():

            landmark = landmarks[landmark_id.value]

            features.extend([
                landmark.x,
                landmark.y,
                landmark.z
            ])

        # -----------------------------
        # 7. Put features into DataFrame
        # -----------------------------
        X_live = pd.DataFrame(
            [features],
            columns=model.feature_names_in_
        )

        # -----------------------------
        # 8. Make prediction
        # -----------------------------
        prediction = model.predict(X_live)[0]

        # Get confidence
        probabilities = model.predict_proba(X_live)[0]
        confidence = max(probabilities) * 100

        # -----------------------------
        # 9. Display prediction
        # -----------------------------
        if prediction:
            label = "CORRECT SQUAT"
        else:
            label = "INCORRECT SQUAT"

        cv2.putText(
            frame,
            label,
            (30, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0) if prediction else (0, 0, 255),
            3
        )

        cv2.putText(
            frame,
            f"Confidence: {confidence:.1f}%",
            (30, 90),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2
        )

        # Draw pose landmarks
        mp_drawing.draw_landmarks(
            frame,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS
        )

    # -----------------------------
    # 10. Show webcam
    # -----------------------------
    cv2.imshow("AI Gym Trainer - Squat", frame)

    # Press Q to quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# -----------------------------
# 11. Cleanup
# -----------------------------
cap.release()
cv2.destroyAllWindows()
pose.close()