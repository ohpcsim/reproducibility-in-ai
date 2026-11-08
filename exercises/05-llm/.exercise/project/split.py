"""Decide which rows are for training, validation and test, and record the lists in splits.json."""
import json

import numpy as np
import yaml
from sklearn.datasets import load_digits

params = yaml.safe_load(open("params.yaml"))["split"]
n = len(load_digits().target)
order = np.random.RandomState(params["seed"]).permutation(n).tolist()
first, second = int(0.6 * n), int(0.8 * n)

splits = {"train": sorted(order[:first]), "val": sorted(order[first:second]), "test": sorted(order[second:])}
with open("splits.json", "w") as out:
    json.dump(splits, out)
    out.write("\n")
print({name: len(rows) for name, rows in splits.items()})
