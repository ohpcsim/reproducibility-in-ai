# Palmer penguins: body mass against flipper length

We report how much heavier a penguin is per mm of flipper, within a species.

- `clean.py` applies the cleaning policy in `params.yaml`.
- `validate.py` stops the pipeline if the cleaned data isn't fit to analyze.
- `report.py` writes `metrics.json` and `results/report.md`.

Data: `data/penguins.csv`, tracked by DVC.
