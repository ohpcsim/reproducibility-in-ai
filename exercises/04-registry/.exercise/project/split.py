"""Record row positions in the validated table by field season."""
import json

import pandas as pd

df = pd.read_csv("results/validated.csv")
splits = {"train": df.index[df["year"] < 2009].tolist(),
          "val": df.index[df["year"] == 2009].tolist()}
with open("splits.json", "w") as out:
    json.dump(splits, out, indent=2)
    out.write("\n")
print({name: len(rows) for name, rows in splits.items()})
