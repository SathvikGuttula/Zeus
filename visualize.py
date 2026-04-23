import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("dataset.csv", names=["time", "rssi", "label"])

plt.plot(df["rssi"])
plt.title("WiFi Signal Variation")
plt.xlabel("Time")
plt.ylabel("RSSI")
plt.show()