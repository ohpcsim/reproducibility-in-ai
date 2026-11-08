"""Stop the pipeline if the cleaned data isn't fit to use."""
import sys

import pandas as pd

REQUIRED = ["species", "body_mass_g", "sex"]

df = pd.read_csv("results/clean.csv")

missing = [column for column in REQUIRED if column not in df.columns]
if missing:
    sys.exit(f"validate: missing columns {missing}")
if df.empty:
    sys.exit("validate: no rows")

df.to_csv("results/validated.csv", index=False)
print(f"validate: {len(df)} rows passed")
