"""Sexual dimorphism: male minus female mean body mass, per species, in grams. Writes metrics.json."""
import json

import pandas as pd

df = pd.read_csv("data/penguins.csv").dropna(subset=["body_mass_g", "sex"])
means = df.groupby(["species", "sex"])["body_mass_g"].mean().unstack()
metrics = {f"dimorphism_g_{species.lower()}": round(float(row["male"] - row["female"]), 1) for species, row in means.iterrows()}
metrics["n_rows"] = len(df)

with open("metrics.json", "w") as out:
    json.dump(metrics, out, indent=2)
    out.write("\n")
print(json.dumps(metrics, indent=2))
