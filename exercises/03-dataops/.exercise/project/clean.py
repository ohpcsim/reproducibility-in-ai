"""Drop penguins with no body mass or no sex, and write results/clean.csv."""
from pathlib import Path

import pandas as pd

raw = pd.read_csv("data/penguins.csv")
penguins = raw.dropna(subset=["body_mass_g", "sex"])

Path("results").mkdir(exist_ok=True)
penguins.to_csv("results/clean.csv", index=False)
print(f"clean: kept {len(penguins)} of {len(raw)} penguins")
