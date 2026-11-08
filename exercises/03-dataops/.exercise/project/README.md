# Palmer penguins: how much heavier are the males?

`metrics.json` holds male mean body mass minus female mean body mass, per species, in grams.

- `clean.py` drops rows with no body mass or no sex.
- `validate.py` stops the pipeline if the cleaned data is missing a column or has no rows.
- `report.py` writes `metrics.json`.

The pipeline runs `clean`, `validate` and `report` in that order. Data: `data/penguins.csv`.
