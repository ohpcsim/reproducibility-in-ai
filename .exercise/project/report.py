"""Male minus female body mass per species, in grams, with the statistic params.yaml names. Writes metrics.json."""
import json

import pandas as pd
import yaml

statistic = yaml.safe_load(open("params.yaml"))["report"]["statistic"]
penguins = pd.read_csv("results/validated.csv")
mass = penguins.groupby(["species", "sex"])["body_mass_g"].agg(statistic)

metrics = {f"dimorphism_g_{species.lower()}": round(float(mass[species, "male"] - mass[species, "female"]), 1)
           for species in sorted(penguins["species"].unique())}
metrics["n_rows"] = len(penguins)
with open("metrics.json", "w") as out:
    json.dump(metrics, out, indent=2)
    out.write("\n")
print(json.dumps(metrics, indent=2))
