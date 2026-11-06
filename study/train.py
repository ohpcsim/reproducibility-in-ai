"""Fit y = a*x + b by least squares on data/train, score RMSE on data/val."""
import csv
import json
import pathlib

import numpy as np


def load(split):
    with open(pathlib.Path("data", split, "data.csv")) as f:
        rows = list(csv.DictReader(f))
    return np.array([float(r["x"]) for r in rows]), np.array([float(r["y"]) for r in rows])


x, y = load("train")
a, b = np.polyfit(x, y, 1)
xv, yv = load("val")
rmse = float(np.sqrt(np.mean((a * xv + b - yv) ** 2)))

pathlib.Path("model").mkdir(exist_ok=True)
pathlib.Path("model/model.json").write_text(json.dumps({"a": round(float(a), 6), "b": round(float(b), 6)}, indent=2) + "\n")
pathlib.Path("metrics.json").write_text(json.dumps({"val_rmse": round(rmse, 6), "a": round(float(a), 6), "b": round(float(b), 6)}, indent=2) + "\n")
