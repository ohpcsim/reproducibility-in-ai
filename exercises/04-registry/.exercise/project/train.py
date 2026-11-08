"""Train on 2007 and 2008, then report accuracy on 2009."""
import json
import os
import pickle

os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"

import pandas as pd
import yaml
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

df = pd.read_csv("results/validated.csv")
splits = json.load(open("splits.json"))
params = yaml.safe_load(open("params.yaml"))
measurements = ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"]
X = pd.concat([df[measurements], pd.get_dummies(df["species"], prefix="species")], axis=1)
y = df["sex"]
model = make_pipeline(StandardScaler(), LogisticRegression(C=params["train"]["C"], max_iter=1000))
model.fit(X.iloc[splits["train"]], y.iloc[splits["train"]])
with open("model.pkl", "wb") as out:
    pickle.dump(model, out)
metrics = {"val_accuracy": round(float(model.score(X.iloc[splits["val"]], y.iloc[splits["val"]])), 3)}
with open("model_metrics.json", "w") as out:
    json.dump(metrics, out, indent=2)
    out.write("\n")
print(metrics)
