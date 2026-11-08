"""Count the selected earthquakes per 0.1 of magnitude, and write results/counts.csv."""
import pandas as pd

selected = pd.read_csv("results/subset.csv")
counts = selected["mag"].round(1).value_counts().sort_index()
counts.rename_axis("magnitude").reset_index(name="count").to_csv("results/counts.csv", index=False)
print(f"count: {len(counts)} magnitude bins, {int(counts.sum())} earthquakes")
