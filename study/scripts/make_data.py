"""Generate the synthetic dataset for this study.

Provenance: synthetic, y = 2.5 * x + 1.0 + noise, seed 20261110.
Run once; the outputs are tracked by DVC, not Git.
"""
import csv
import pathlib
import random

rng = random.Random(20261110)
for split, n in (("train", 80), ("val", 20)):
    out = pathlib.Path("data", split)
    out.mkdir(parents=True, exist_ok=True)
    with open(out / "data.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["x", "y"])
        for _ in range(n):
            x = rng.uniform(0, 10)
            w.writerow([f"{x:.6f}", f"{2.5 * x + 1.0 + rng.gauss(0, 0.5):.6f}"])
