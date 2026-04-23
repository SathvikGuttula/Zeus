import time
import csv
import subprocess

import time
import subprocess
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# 1. Improved get_rssi with dBm conversion
def get_rssi():
    try:
        result = subprocess.check_output("netsh wlan show interfaces", shell=True).decode()
        for line in result.split("\n"):
            if "Signal" in line:
                percent = int(line.split(":")[1].strip().replace("%", ""))
                # Convert % to dBm: 100% -> -50dBm, 0% -> -100dBm
                return (percent / 2) - 100
    except:
        return None

# 2. Setup Plot
fig, ax = plt.subplots()
x_data, y_data = [], []
line, = ax.plot([], [], lw=2, color='blue')

ax.set_ylim(-100, -30) # dBm range
ax.set_xlim(0, 60)      # Show last 60 seconds
ax.set_title("Live Wi-Fi Signal Strength")
ax.set_ylabel("Signal Strength (dBm)")
ax.set_xlabel("Time (s)")
ax.grid(True, linestyle='--', alpha=0.6)

# 3. Animation Update Function
def update(frame):
    rssi = get_rssi()
    if rssi is not None:
        y_data.append(rssi)
        x_data.append(len(y_data))
        
        # Keep only the last 60 data points on screen
        line.set_data(x_data[-60:], y_data[-60:])
        ax.set_xlim(max(0, len(y_data) - 60), len(y_data))
        
    return line,

# 4. Run Live Graph
ani = FuncAnimation(fig, update, interval=1000) # Updates every 1 second
plt.show()

def collect(label, duration=120):
    data = []
    start = time.time()

    while time.time() - start < duration:
        rssi = get_rssi()
        if rssi is not None:
            timestamp = time.time()
            data.append([timestamp, rssi, label])
            print(f"{timestamp}, {rssi}, {label}")
        time.sleep(1)

    return data

if __name__ == "__main__":
    print("1 = no activity, 2 = normal, 3 = suspicious")
    label = int(input("Enter label: "))

    data = collect(label, 120)

    with open("dataset.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(data)

    print("✅ Data saved!")