import time
import numpy as np
import pickle
import subprocess

def get_rssi():
    try:
        result = subprocess.check_output("netsh wlan show interfaces", shell=True).decode()
        for line in result.split("\n"):
            if "Signal" in line:
                return int(line.split(":")[1].strip().replace("%", ""))
    except:
        return None

with open("model.pkl", "rb") as f:
    model = pickle.load(f)

buffer = []
import requests

TOKEN = "8177714274:AAHPMqWUlW0QIgGRVBQTMEzy616OHqp5hGU"
CHAT_ID = "8648853699"

def send_alert(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})
while True:
    rssi = get_rssi()

    if rssi is not None:
        buffer.append(rssi)
        print(f"RSSI: {rssi}")

    if len(buffer) >= 10:
        window = buffer[-10:]

        mean = np.mean(window)
        var = np.var(window)
        diff = np.mean(np.diff(window))

        features = np.array([[mean, var, diff]])
        prediction = model.predict(features)[0]

        if prediction == 3 and var > 1:
            print("🚨 ALERT!")
        elif prediction == 2:
            print("👤 Normal Activity")
        else:
            print("😴 No Activity")
    
    time.sleep(1)

