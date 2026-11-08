"""Check results/clean.csv before anything reads it, and write results/validated.csv. A bad table stops here."""
import sys

import pandas as pd

penguins = pd.read_csv("results/clean.csv")
required = ["species", "bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g", "sex", "year"]
missing = [column for column in required if column not in penguins.columns]
if missing:
    sys.exit(f"validate: missing columns {', '.join(missing)}")
if penguins.empty:
    sys.exit("validate: no rows")

penguins.to_csv("results/validated.csv", index=False)
print(f"validate: {len(penguins)} rows pass")
