"""Keep the earthquakes params.yaml asks for, and write results/subset.csv."""
from pathlib import Path

import pandas as pd
import yaml

params = yaml.safe_load(open("params.yaml"))
catalog = pd.read_csv("data/earthquakes.csv")
keep = (catalog["type"] == "earthquake") & (catalog["mag"] >= params["min_magnitude"]) & (catalog["depth"] <= params["max_depth_km"])

Path("results").mkdir(exist_ok=True)
catalog[keep].to_csv("results/subset.csv", index=False)
print(f"subset: kept {int(keep.sum())} of {len(catalog)} earthquakes")
