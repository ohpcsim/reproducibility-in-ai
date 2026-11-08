"""Drop penguins with no body mass or no sex, apply the repairs params.yaml turns on, and write results/clean.csv."""
from pathlib import Path

import pandas as pd
import yaml

params = yaml.safe_load(open("params.yaml"))["clean"]
raw = pd.read_csv("data/penguins.csv")
penguins = raw.dropna(subset=["body_mass_g", "sex"]).copy()
if params["convert_kg"]:
    in_kg = penguins["body_mass_g"] < 100
    penguins.loc[in_kg, "body_mass_g"] = (penguins.loc[in_kg, "body_mass_g"] * 1000).round()
if params["map_sex_labels"]:
    penguins["sex"] = penguins["sex"].replace({"M": "male", "F": "female"})

Path("results").mkdir(exist_ok=True)
penguins.to_csv("results/clean.csv", index=False)
print(f"clean: kept {len(penguins)} of {len(raw)} penguins")
