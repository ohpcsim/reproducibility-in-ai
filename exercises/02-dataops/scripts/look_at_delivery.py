#!/usr/bin/env python3
"""Print a summary of the delivered data, and how many rows arrived twice."""
from pathlib import Path

import pandas as pd

delivery = pd.read_csv(Path(__file__).resolve().parents[1] / "project" / "data" / "penguins.csv")
print(delivery[["flipper_length_mm", "body_mass_g"]].describe().round(1))
print("repeated rows:", delivery.duplicated().sum())
