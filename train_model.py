import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import pickle

df = pd.read_csv("dataset.csv", names=["time", "rssi", "label"])

window_size = 10
features = []
labels = []

for i in range(len(df) - window_size):
    window = df["rssi"].iloc[i:i+window_size]

    mean = np.mean(window)
    var = np.var(window)
    diff = np.mean(np.diff(window))

    features.append([mean, var, diff])
    labels.append(df["label"].iloc[i])

X = np.array(features)
y = np.array(labels)

model = RandomForestClassifier(n_estimators=100)
model.fit(X, y)

with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

print("🔥 Model trained!")