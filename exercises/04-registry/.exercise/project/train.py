"""Train the digit classifier on the training rows and score it on the validation rows."""
import json
import os
import pickle

# One thread gives the same result from run to run.
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"

import yaml
from sklearn.datasets import load_digits
from sklearn.neural_network import MLPClassifier

params = yaml.safe_load(open("params.yaml"))["train"]
splits = json.load(open("splits.json"))
digits = load_digits()
X, y = digits.data / 16, digits.target

model = MLPClassifier(hidden_layer_sizes=(params["hidden"],), max_iter=1000, random_state=0)
model.fit(X[splits["train"]], y[splits["train"]])

with open("model.pkl", "wb") as out:
    pickle.dump(model, out)

metrics = {"val_accuracy": round(float(model.score(X[splits["val"]], y[splits["val"]])), 3)}
with open("metrics.json", "w") as out:
    json.dump(metrics, out, indent=2)
    out.write("\n")
print(metrics)
