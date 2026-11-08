#!/usr/bin/env python3
"""Deliver the 2008 and 2009 field seasons into project/data/penguins.csv.

The rows are real. Someone at the field station also recorded forty flipper
lengths in inches, and twelve rows arrived twice.
"""
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parents[1]

df = pd.read_csv(HERE / ".exercise" / "data" / "penguins.csv")
new = df[(df["year"] > 2007) & df["flipper_length_mm"].notna()]

inches = new.sample(40, random_state=2009).index
df.loc[inches, "flipper_length_mm"] = (df.loc[inches, "flipper_length_mm"] / 25.4).round(2)
repeats = df.loc[new.sample(12, random_state=2008).index]
delivery = pd.concat([df, repeats], ignore_index=True)

delivery.to_csv(HERE / "project" / "data" / "penguins.csv", index=False)
print(f"Delivered {len(delivery)} rows to project/data/penguins.csv, covering 2007 to 2009.")
