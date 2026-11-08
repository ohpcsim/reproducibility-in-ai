"""Write metrics.json: male minus female body mass, per species, in grams."""
import json

import pandas as pd
import yaml

statistic = yaml.safe_load(open("params.yaml"))["report"]["statistic"]
df = pd.read_csv("results/validated.csv")

mass = df.groupby(["species", "sex"])["body_mass_g"].agg(statistic).unstack()
gap = mass["male"] - mass["female"]
metrics = {f"dimorphism_g_{species.lower()}": round(float(grams), 1) for species, grams in gap.items()}
metrics["n_rows"] = len(df)

with open("metrics.json", "w") as out:
    json.dump(metrics, out, indent=2)
    out.write("\n")
print(json.dumps(metrics))
