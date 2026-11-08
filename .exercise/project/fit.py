"""Fit the Gutenberg-Richter b-value to the counts, and write metrics.json."""
import json
import math

import pandas as pd

counts = pd.read_csv("results/counts.csv")
n = int(counts["count"].sum())
lowest = float(counts["magnitude"].min())
mean = float((counts["magnitude"] * counts["count"]).sum()) / n
# Maximum likelihood (Aki 1965), with Utsu's correction for bins 0.1 wide.
b = math.log10(math.e) / (mean - (lowest - 0.05))

metrics = {
    "b_value": round(b, 3),
    "b_uncertainty": round(b / math.sqrt(n), 3),
    "quakes_per_unit_magnitude": round(10 ** b, 1),
    "n_earthquakes": n,
    "lowest_magnitude": lowest,
}
with open("metrics.json", "w") as out:
    json.dump(metrics, out, indent=2)
    out.write("\n")
print(json.dumps(metrics, indent=2))
