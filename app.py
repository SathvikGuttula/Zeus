from flask import Flask, render_template
from flask_socketio import SocketIO
import numpy as np
import pickle
import subprocess
import time
import threading
import eventlet
eventlet.monkey_patch()
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Load model
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

buffer = []

def get_rssi():
    try:
        result = subprocess.check_output("netsh wlan show interfaces", shell=True).decode()
        for line in result.split("\n"):
            if "Signal" in line:
                return int(line.split(":")[1].strip().replace("%", ""))
    except:
        return None

def background_task():
    while True:
        rssi = get_rssi()

        if rssi is not None:
            buffer.append(rssi)

        if len(buffer) >= 10:
            window = buffer[-10:]

            mean = np.mean(window)
            var = np.var(window)
            diff = np.mean(np.diff(window))

            features = np.array([[mean, var, diff]])
            prediction = int(model.predict(features)[0])

            # Activity intensity (for heatmap feel)
            intensity = float(var)

            socketio.emit("update", {
                "rssi": rssi,
                "prediction": prediction,
                "intensity": intensity
            })

        time.sleep(1)

@app.route("/")
def index():
    return render_template("index.html")

threading.Thread(target=background_task).start()

if __name__ == "__main__":
    app.run(debug=True)