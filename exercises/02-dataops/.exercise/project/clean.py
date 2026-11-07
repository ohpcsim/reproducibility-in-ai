"""Apply the cleaning policy in params.yaml to the raw delivery."""
from pathlib import Path

import pandas as pd
import yaml

policy = yaml.safe_load(open("params.yaml"))["clean"]
df = pd.read_csv("data/penguins.csv")

df = df.dropna(subset=["flipper_length_mm", "body_mass_g"])
if policy["drop_missing_sex"]:
    df = df.dropna(subset=["sex"])

Path("results").mkdir(exist_ok=True)
df.to_csv("results/clean.csv", index=False)
print(f"clean: kept {len(df)} rows")
