# Palmer penguins

`analyze.py` reads `data/penguins.csv`, the 2007 field season, and computes how much heavier a penguin is per mm of flipper, within a species. It prints the slope in g/mm and writes it to `metrics.json`.

```bash
python analyze.py
```

- `environment.yml` lists the packages for conda.
- `pyproject.toml` lists the packages for uv.

Data: Palmer penguins, CC0 1.0. Horst AM, Hill AP, Gorman KB (2020), doi:10.5281/zenodo.3960218. Gorman KB, Williams TD, Fraser WR (2014), PLoS ONE 9(3):e90081.
