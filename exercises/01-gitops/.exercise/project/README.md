# Mauna Loa CO2 growth rate

We publish one number: how fast CO2 is rising now, in ppm per year.

- `params.yaml` holds the years and the polynomial degree.
- `analyze.py` fits the trend and writes `metrics.json`.
- `check_fresh.py` says whether `metrics.json` matches a rerun.
- `holdout.py` compares degrees on years the fit did not see.
- `hooks/pre-commit` runs `check_fresh.py` before each commit, once you install it.

Data: `data/co2_mm_mlo.csv`, from NOAA Global Monitoring Laboratory.
