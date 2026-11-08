"""Body mass by species and sex, from results/validated.csv. Writes figures/body_mass.svg, which README.md shows."""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

# Same data, same environment, same bytes: fixed IDs and no date in the file.
plt.rcParams["svg.hashsalt"] = "penguins"

penguins = pd.read_csv("results/validated.csv")
species = sorted(penguins["species"].unique())
fig, ax = plt.subplots(figsize=(6, 4))
summary = []
for offset, sex, color in ((-0.2, "female", "#c05a00"), (0.2, "male", "#2a6fb0")):
    masses = [penguins.loc[(penguins["species"] == name) & (penguins["sex"] == sex), "body_mass_g"] for name in species]
    boxes = ax.boxplot(masses, positions=[i + offset for i in range(len(species))], widths=0.35, patch_artist=True,
                       medianprops={"color": "black"})
    for box in boxes["boxes"]:
        box.set(facecolor=color, alpha=0.6)
    ax.plot([], [], "s", color=color, alpha=0.6, label=sex)
    summary += [f"{name} {sex}: {len(mass)} penguins, median {mass.median():.1f} g" for name, mass in zip(species, masses)]
ax.set_xticks(range(len(species)), species)
ax.set_xlabel("Species")
ax.set_ylabel("Body mass (g)")
ax.set_title(f"Body mass by species and sex, {len(penguins)} penguins")
ax.legend(title="Sex")
fig.tight_layout()

Path("figures").mkdir(exist_ok=True)
# The description records what the figure shows, in words, so a reader or a check can read it from the file.
fig.savefig("figures/body_mass.svg", metadata={"Date": None, "Description": "Body mass by species and sex. " + "; ".join(sorted(summary))})
print(f"plot: wrote figures/body_mass.svg from {len(penguins)} penguins")
