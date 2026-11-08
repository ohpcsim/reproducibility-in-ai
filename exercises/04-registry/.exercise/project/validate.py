"""Stop the pipeline if the cleaned data isn't fit to use."""
import sys

import pandas as pd

REQUIRED = ["species", "body_mass_g", "sex"]
SPECIES = ["Adelie", "Chinstrap", "Gentoo"]

df = pd.read_csv("results/clean.csv")

missing = [column for column in REQUIRED if column not in df.columns]
if missing:
    sys.exit(f"validate: missing columns {missing}")
if df.empty:
    sys.exit("validate: no rows")

light_or_heavy = ~df["body_mass_g"].between(2000, 7000)
if light_or_heavy.any():
    sys.exit(f"validate: {light_or_heavy.sum()} rows have body_mass_g outside 2000 to 7000 g")
unknown_sex = ~df["sex"].isin(["male", "female"])
if unknown_sex.any():
    sys.exit(f"validate: {unknown_sex.sum()} rows have sex other than male or female: {sorted(df.loc[unknown_sex, 'sex'].unique())}")
unknown_species = ~df["species"].isin(SPECIES)
if unknown_species.any():
    sys.exit(f"validate: {unknown_species.sum()} rows have an unknown species: {sorted(df.loc[unknown_species, 'species'].unique())}")

df.to_csv("results/validated.csv", index=False)
print(f"validate: {len(df)} rows passed")
