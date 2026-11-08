"""Drop rows with no body mass or no sex, then apply the repairs that params.yaml turns on."""
from pathlib import Path

import pandas as pd
import yaml

policy = yaml.safe_load(open("params.yaml"))["clean"]
df = pd.read_csv("data/penguins.csv")
df = df.dropna(subset=["body_mass_g", "sex"])

if policy["convert_kg"]:
    kg = df["body_mass_g"] < 100
    df.loc[kg, "body_mass_g"] = (df.loc[kg, "body_mass_g"] * 1000).round()
if policy["map_sex_labels"]:
    df["sex"] = df["sex"].replace({"M": "male", "F": "female"})

Path("results").mkdir(exist_ok=True)
df.to_csv("results/clean.csv", index=False)
print(f"clean: kept {len(df)} rows")
