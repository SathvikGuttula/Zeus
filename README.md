# Zeus
📡 WiFi-Based Suspicious Activity Detection System

A non-intrusive hostel monitoring system that uses WiFi signal fluctuations (RSSI) and machine learning to detect human activity patterns and flag potentially suspicious behavior — without using cameras inside private spaces.

🚀 Overview

This project demonstrates how WiFi signals can be used as a sensing medium to detect:

Human presence
Movement patterns
Unusual / repetitive activity

Instead of relying on surveillance cameras, the system analyzes WiFi signal disturbances caused by human motion.

🧠 How It Works

WiFi signals change when a human body interacts with them due to:

Reflection
Absorption
Scattering

We capture these changes using RSSI (Received Signal Strength Indicator) and analyze them over time.

📊 Signal Representation

σ
2
=
N
1
	​

∑(x
i
	​

−μ)
2

Variance of the signal helps estimate movement intensity.

🔧 Features
📡 Real-time WiFi signal monitoring
🤖 Machine Learning-based classification
🌡️ Activity intensity detection
🌐 Web dashboard (live graph + heatmap)
🧍 Skeleton visualization (for demo purposes)
🚨 Alert system for suspicious behavior
🏗️ System Architecture
WiFi RSSI → Feature Extraction → ML Model → Prediction
                                    ↓
                             Dashboard / Alerts
📁 Project Structure
wifi_detection_project/
│
├── collect_data.py        # Collect RSSI data
├── train_model.py         # Train ML model
├── detect.py              # Real-time detection
├── wifi_skeleton_system.py # Visualization system
├── app.py                 # Web dashboard
├── dataset.csv            # Collected data
├── model.pkl              # Trained model
├── scaler.pkl             # Feature scaler
└── templates/
    └── index.html         # Dashboard UI
⚙️ Installation
1. Clone the repository
git clone https://github.com/your-username/wifi-activity-detection.git
cd wifi-activity-detection
2. Install dependencies
pip install numpy pandas scikit-learn matplotlib flask opencv-python mediapipe
📡 Setup (Important)

For best results, use a controlled WiFi environment:

[ Phone Hotspot ] ← 1–2m → [ Person ] ← 1–2m → [ Laptop ]
Use your phone as hotspot
Keep devices fixed
Stand between transmitter and receiver
🧪 Usage
🔹 Step 1: Collect Data
python collect_data.py

Label data as:

1 → No activity
2 → Normal movement
3 → Suspicious activity
🔹 Step 2: Train Model
python train_model.py

This generates:

model.pkl
scaler.pkl
🔹 Step 3: Run Detection
python detect.py
🔹 Step 4: Run Visualization System
python wifi_skeleton_system.py
🔹 Step 5: Run Web Dashboard
python app.py

Open:

http://localhost:5000
📊 Machine Learning
Features used:
Mean signal strength
Variance
Standard deviation
Signal range
Signal difference
Zero-crossing rate
Model:
Random Forest / Gradient Boosting
🎯 Detection Classes
Label	Description
1	No activity
2	Normal movement
3	Suspicious / repetitive activity
⚠️ Limitations
❌ Cannot directly detect smoking/drinking
❌ No exact location tracking
❌ Accuracy depends on environment
❌ Sensitive to noise and interference
🧠 Key Insight

This system does not “see” people — it detects patterns in signal disturbance.

🔮 Future Improvements
Use CSI (Channel State Information) instead of RSSI
Multi-device sensing for spatial tracking
Deep learning models (LSTM / CNN)
Improved heatmap visualization
Real-time mobile alerts
🛡️ Privacy Advantage
No cameras inside private rooms
Non-intrusive monitoring
Privacy-preserving alternative
📸 Demo

(Add screenshots here — dashboard, skeleton view, graphs)

🧑‍💻 Author

Sathvik Guttula

⭐ Acknowledgements
RF sensing research
WiFi-based human activity recognition studies
Open-source ML libraries
📜 License

This project is for educational purposes only.

💥 Final Note

This project demonstrates how everyday WiFi signals can be repurposed as a sensing tool, opening possibilities for low-cost, privacy-aware monitoring systems.
