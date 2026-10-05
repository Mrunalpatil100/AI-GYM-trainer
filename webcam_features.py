import cv2
import mediapipe as mp

# Start MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

# Open webcam
cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

while True:
    ret, frame = cap.read()

    if not ret:
        print("❌ Could not read camera")
        break

    # Convert BGR → RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect pose
    results = pose.process(rgb_frame)

    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark

        # MediaPipe landmark numbers
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

        # Extract X, Y, Z
        features = []

        for name, landmark_id in required_landmarks.items():
            landmark = landmarks[landmark_id.value]

            features.extend([
                landmark.x,
                landmark.y,
                landmark.z
            ])

        print("Number of features:", len(features))
        print(features)

        # Stop after one frame
        break

cap.release()