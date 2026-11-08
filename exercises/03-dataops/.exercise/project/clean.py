"""Drop rows with no body mass or no sex."""
from pathlib import Path

import pandas as pd

df = pd.read_csv("data/penguins.csv")
df = df.dropna(subset=["body_mass_g", "sex"])

Path("results").mkdir(exist_ok=True)
df.to_csv("results/clean.csv", index=False)
print(f"clean: kept {len(df)} rows")
