"""How much heavier is a penguin per mm of flipper, within a species?"""
import json

import pandas as pd

df = pd.read_csv("results/validated.csv")


def slope(table):
    x = table["flipper_length_mm"] - table["flipper_length_mm"].mean()
    y = table["body_mass_g"] - table["body_mass_g"].mean()
    return (x * y).sum() / (x * x).sum()


# Center each species on its own mean, so the slope compares penguins within a species.
centered = df.copy()
for column in ["flipper_length_mm", "body_mass_g"]:
    centered[column] = df[column] - df.groupby("species")[column].transform("mean")

metrics = {"slope_g_per_mm": round(float(slope(centered)), 3), "n_rows": len(df)}
with open("metrics.json", "w") as out:
    json.dump(metrics, out, indent=2)
    out.write("\n")

with open("results/report.md", "w") as out:
    out.write("| species | rows | slope (g/mm) |\n|---|---|---|\n")
    for species, table in df.groupby("species"):
        out.write(f"| {species} | {len(table)} | {slope(table):.1f} |\n")
    out.write(f"| within species | {len(df)} | {metrics['slope_g_per_mm']:.1f} |\n")
print(open("results/report.md").read())
