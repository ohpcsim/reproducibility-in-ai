# Sexual dimorphism in Palmer penguins

How much heavier is a male penguin than a female of the same species? We report the difference of the mean body masses, in grams, per species, for the 2007 field season.

![Body mass by species and sex](figures/body_mass.svg)

## Rebuild the results

```bash
snakemake --cores 1
```

- The workflow reads `data/penguins.csv` and writes `metrics.json`, the difference per species, and `figures/body_mass.svg`, the figure above. Neither is in Git. The workflow builds them.
- `params.yaml` sets the statistic: `mean` or `median`.
- `clean.py` drops penguins with no body mass or no sex. `validate.py` checks the columns and rows. `report.py` writes `metrics.json`. `plot.py` draws the figure.

Data: palmerpenguins (Horst, Hill and Gorman 2020, doi:10.5281/zenodo.3960218), CC0, from Gorman, Williams and Fraser (2014), PLOS ONE 9(3): e90081. Collected by Palmer Station LTER with NSF support.
