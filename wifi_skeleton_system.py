import cv2
import mediapipe as mp
import numpy as np
import pickle
import subprocess
import time

# Load ML model
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

# Mediapipe setup
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# WiFi RSSI function
def get_rssi():
    try:
        result = subprocess.check_output("netsh wlan show interfaces", shell=True).decode()
        for line in result.split("\n"):
            if "Signal" in line:
                return int(line.split(":")[1].strip().replace("%", ""))
    except:
        return None

buffer = []

cap = cv2.VideoCapture(0)

with mp_pose.Pose() as pose:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # --- WIFI PART ---
        rssi = get_rssi()
        prediction = 1  # default

        if rssi is not None:
            buffer.append(rssi)

        if len(buffer) >= 10:
            window = buffer[-10:]

            mean = np.mean(window)
            var = np.var(window)
            diff = np.mean(np.diff(window))

            features = np.array([[mean, var, diff]])
            prediction = int(model.predict(features)[0])

        # --- CAMERA PART ---
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(image)

        # Black background
        black = np.zeros_like(frame)

        if results.pose_landmarks:
            # Color logic based on WiFi prediction
            if prediction == 1:
                color1 = (100, 100, 100)  # grey (no activity)
                color2 = (100, 100, 100)
                status = "No Activity"
            elif prediction == 2:
                color1 = (0, 255, 0)  # green
                color2 = (255, 0, 255)
                status = "Normal Activity"
            else:
                color1 = (0, 0, 255)  # RED ALERT
                color2 = (0, 255, 255)
                status = "🚨 Suspicious Activity!"
                if int(time.time()) % 2 == 0:
                    color1 = (0,0,255)
                else:
                    color1 = (255,255,255)
            mp_drawing.draw_landmarks(
                black,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                mp_drawing.DrawingSpec(color=color1, thickness=2),
                mp_drawing.DrawingSpec(color=color2, thickness=2)
            )

        # Show status text
        cv2.putText(black, status, (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)

        cv2.imshow("WiFi Skeleton System", black)

        if cv2.waitKey(1) & 0xFF == 27:
            break

        time.sleep(1)

cap.release()
cv2.destroyAllWindows()