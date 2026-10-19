
import cv2
import mediapipe as mp
import pickle
import pandas as pd
import math
import time

# ---------------------------------
# 1. Load trained ML model
# ---------------------------------
with open("squat_model.pkl", "rb") as file:
    model = pickle.load(file)

print("Squat model loaded successfully!")

# ---------------------------------
# 2. Start MediaPipe Pose
# ---------------------------------
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

pose = mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# ---------------------------------
# 3. Open webcam
# ---------------------------------
cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

if not cap.isOpened():
    print("Camera could not be opened!")
    pose.close()
    raise SystemExit

print("Camera opened successfully!")
print("Press Q to finish your workout.")

# ---------------------------------
# 4. Required landmarks for ML model
# ---------------------------------
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

# ---------------------------------
# 5. Workout statistics
# ---------------------------------
rep_count = 0
squat_down = False

correct_frames = 0
incorrect_frames = 0

start_time = time.time()

# Adjustable squat-angle thresholds
DOWN_ANGLE = 120
STANDING_ANGLE = 160


# ---------------------------------
# 6. Calculate angle at the knee
# ---------------------------------
def calculate_angle(hip, knee, ankle):
    # Points use normalized MediaPipe x/y coordinates.
    # Angle is measured at the knee.
    angle = math.degrees(
        math.atan2(ankle[1] - knee[1], ankle[0] - knee[0])
        - math.atan2(hip[1] - knee[1], hip[0] - knee[0])
    )

    angle = abs(angle)

    if angle > 180:
        angle = 360 - angle

    return angle


def landmark_point(landmarks, landmark_id):
    landmark = landmarks[landmark_id.value]
    return (landmark.x, landmark.y)


# ---------------------------------
# 7. Main webcam loop
# ---------------------------------
try:
    while True:
        ret, frame = cap.read()

        if not ret:
            print("Failed to get webcam frame.")
            break

        # Mirror the webcam image for a more natural display.
        frame = cv2.flip(frame, 1)

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(rgb_frame)

        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark

            # ---------------------------------
            # 8. Extract 42 ML features
            # ---------------------------------
            features = []

            for name, landmark_id in required_landmarks.items():
                landmark = landmarks[landmark_id.value]

                features.extend([
                    landmark.x,
                    landmark.y,
                    landmark.z
                ])

            X_live = pd.DataFrame(
                [features],
                columns=model.feature_names_in_
            )

            # ---------------------------------
            # 9. Predict squat frame
            # ---------------------------------
            prediction = model.predict(X_live)[0]
            probabilities = model.predict_proba(X_live)[0]
            confidence = max(probabilities) * 100

            if bool(prediction):
                label = "MODEL: CORRECT"
                label_color = (0, 200, 0)
                correct_frames += 1
            else:
                label = "MODEL: INCORRECT"
                label_color = (0, 0, 255)
                incorrect_frames += 1

            # ---------------------------------
            # 10. Estimate knee angle
            # ---------------------------------
            left_ids = (
                mp_pose.PoseLandmark.LEFT_HIP,
                mp_pose.PoseLandmark.LEFT_KNEE,
                mp_pose.PoseLandmark.LEFT_ANKLE
            )

            right_ids = (
                mp_pose.PoseLandmark.RIGHT_HIP,
                mp_pose.PoseLandmark.RIGHT_KNEE,
                mp_pose.PoseLandmark.RIGHT_ANKLE
            )

            left_visibility = min(
                landmarks[left_ids[0].value].visibility,
                landmarks[left_ids[1].value].visibility,
                landmarks[left_ids[2].value].visibility
            )

            right_visibility = min(
                landmarks[right_ids[0].value].visibility,
                landmarks[right_ids[1].value].visibility,
                landmarks[right_ids[2].value].visibility
            )

            # Use whichever side is more visible.
            if left_visibility >= right_visibility:
                chosen_ids = left_ids
                side_visibility = left_visibility
            else:
                chosen_ids = right_ids
                side_visibility = right_visibility

            hip = landmark_point(landmarks, chosen_ids[0])
            knee = landmark_point(landmarks, chosen_ids[1])
            ankle = landmark_point(landmarks, chosen_ids[2])

            knee_angle = calculate_angle(hip, knee, ankle)

            # ---------------------------------
            # 11. Count completed squats
            # ---------------------------------
            if side_visibility >= 0.5:
                if knee_angle < DOWN_ANGLE:
                    squat_down = True

                elif squat_down and knee_angle > STANDING_ANGLE:
                    rep_count += 1
                    squat_down = False

            # Draw pose skeleton.
            mp_drawing.draw_landmarks(
                frame,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS
            )

            # Show prediction and angle.
            cv2.putText(
                frame, label, (25, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8, label_color, 2
            )

            cv2.putText(
                frame, f"Model confidence: {confidence:.1f}%",
                (25, 75), cv2.FONT_HERSHEY_SIMPLEX,
                0.6, (255, 255, 255), 2
            )

            cv2.putText(
                frame, f"Knee angle: {knee_angle:.1f}",
                (25, 110), cv2.FONT_HERSHEY_SIMPLEX,
                0.6, (255, 255, 0), 2
            )

        else:
            cv2.putText(
                frame, "BODY NOT DETECTED",
                (25, 40), cv2.FONT_HERSHEY_SIMPLEX,
                0.8, (0, 0, 255), 2
            )

        # ---------------------------------
        # 12. Timer and workout dashboard
        # ---------------------------------
        elapsed_seconds = int(time.time() - start_time)
        minutes = elapsed_seconds // 60
        seconds = elapsed_seconds % 60

        cv2.putText(
            frame, f"Reps: {rep_count}",
            (25, 155), cv2.FONT_HERSHEY_SIMPLEX,
            0.8, (0, 255, 255), 2
        )

        cv2.putText(
            frame, f"Workout time: {minutes:02d}:{seconds:02d}",
            (25, 190), cv2.FONT_HERSHEY_SIMPLEX,
            0.65, (255, 255, 255), 2
        )

        cv2.putText(
            frame, f"Correct-classified frames: {correct_frames}",
            (25, 225), cv2.FONT_HERSHEY_SIMPLEX,
            0.55, (0, 200, 0), 2
        )

        cv2.putText(
            frame, f"Incorrect-classified frames: {incorrect_frames}",
            (25, 255), cv2.FONT_HERSHEY_SIMPLEX,
            0.55, (0, 0, 255), 2
        )

        cv2.imshow("AI Gym Trainer - Workout Dashboard", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

finally:
    cap.release()
    cv2.destroyAllWindows()
    pose.close()

    # ---------------------------------
    # 13. Final workout summary
    # ---------------------------------
    total_frames = correct_frames + incorrect_frames
    elapsed_seconds = int(time.time() - start_time)

    print("\n========== WORKOUT SUMMARY ==========")
    print(f"Completed reps: {rep_count}")
    print(
        f"Workout duration: "
        f"{elapsed_seconds // 60:02d}:{elapsed_seconds % 60:02d}"
    )
    print(f"Frames classified as correct: {correct_frames}")
    print(f"Frames classified as incorrect: {incorrect_frames}")

    if total_frames > 0:
        print(
            "Percentage of frames classified as correct: "
            f"{correct_frames / total_frames * 100:.1f}%"
        )

    print("=====================================")
