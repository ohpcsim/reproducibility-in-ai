"""Fit the b-value from each start magnitude, so a person can see where the catalog is complete.

It reads the raw catalog and the depth limit, not the selection, so it sees below min_magnitude.
It writes completeness.md and prints it.
"""
import math

import pandas as pd
import yaml

params = yaml.safe_load(open("params.yaml"))
catalog = pd.read_csv("data/earthquakes.csv")
shallow = (catalog["type"] == "earthquake") & (catalog["depth"] <= params["max_depth_km"])
magnitudes = catalog.loc[shallow, "mag"].round(1)

lines = ["| start magnitude | earthquakes | b-value | uncertainty |", "|---|---|---|---|"]
for tenths in range(40, 56):
    start = tenths / 10
    kept = magnitudes[magnitudes >= start]
    b = math.log10(math.e) / (kept.mean() - (start - 0.05))
    lines.append(f"| {start:.1f} | {len(kept)} | {b:.2f} | {b / math.sqrt(len(kept)):.2f} |")

table = "\n".join(lines) + "\n"
open("completeness.md", "w").write(table)
print(table, end="")
