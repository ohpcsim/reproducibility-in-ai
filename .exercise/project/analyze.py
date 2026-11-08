"""How much heavier is a penguin per mm of flipper, within a species? Writes metrics.json."""
import json

import pandas as pd

df = pd.read_csv("data/penguins.csv").dropna(subset=["flipper_length_mm", "body_mass_g"])

# Center each species on its own mean, so the slope compares penguins within a species.
x = df["flipper_length_mm"] - df.groupby("species")["flipper_length_mm"].transform("mean")
y = df["body_mass_g"] - df.groupby("species")["body_mass_g"].transform("mean")
metrics = {"slope_g_per_mm": round(float((x * y).sum() / (x * x).sum()), 3), "n_rows": len(df)}

with open("metrics.json", "w") as out:
    json.dump(metrics, out, indent=2)
    out.write("\n")
print(json.dumps(metrics, indent=2))
