# How many magnitude 5 earthquakes for each magnitude 6?

We report the Gutenberg-Richter b-value of the 2024 catalog. Each step down in magnitude multiplies the number of earthquakes by 10^b.

Run these in this order:

1. `python subset.py` keeps the earthquakes `params.yaml` asks for and writes `results/subset.csv`.
2. `python count.py` counts them per 0.1 of magnitude and writes `results/counts.csv`.
3. `python fit.py` fits the b-value and writes `metrics.json`.

After a change to `params.yaml`, rerun the steps that need it.

Data: `data/earthquakes.csv`, from the USGS ANSS Comprehensive Earthquake Catalog.
