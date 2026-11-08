# Sexual dimorphism in Palmer penguins

How much heavier is a male penguin than a female of the same species? We report the difference of the mean body masses, in grams, per species, for the 2007 field season.

Run clean.py, validate.py, report.py in this order:

1. `python clean.py` drops penguins with no body mass or no sex and writes `results/clean.csv`.
2. `python validate.py` checks that the columns and rows are there, and writes `results/validated.csv`.
3. `python report.py` computes the difference per species with the statistic `params.yaml` names, and writes `metrics.json`.

After a change to `params.yaml`, rerun the steps that need it.

Data: palmerpenguins (Horst, Hill and Gorman 2020, doi:10.5281/zenodo.3960218), CC0, from Gorman, Williams and Fraser (2014), PLOS ONE 9(3): e90081. Collected by Palmer Station LTER with NSF support.
