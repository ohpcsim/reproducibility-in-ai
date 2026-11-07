"""Fit the trend and write the numbers the group publishes to metrics.json."""
import json

import pandas as pd
import yaml

import trend

params = yaml.safe_load(open("params.yaml"))
table = pd.read_csv("data/co2_mm_mlo.csv", comment="#")
metrics = trend.summarize(table["decimal date"].to_numpy(), table["average"].to_numpy(), params)

with open("metrics.json", "w") as out:
    json.dump(metrics, out, indent=2)
    out.write("\n")
print(json.dumps(metrics, indent=2))
