---
title: "The project: the Palmer penguins dataset"
---

- The workshop's exercises use one project, a study of Palmer penguins, and add a capability in each exercise.
- This page says what the data is, what the project computes, what each exercise adds and why we chose it.
- [Literate Science Results: sexual dimorphism in Palmer penguins](results/results.ipynb) runs the finished project and shows its table, a figure and the classifier's accuracy.

## The data

- 344 adult Adelie, Chinstrap and Gentoo penguins, measured on Biscoe, Dream and Torgersen islands near Palmer Station, Antarctica. ([Gorman, Williams and Fraser 2014](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0090081))
- The field work covered three breeding seasons, the austral summers of 2007/08, 2008/09 and 2009/10. The `year` column says 2007, 2008 and 2009. ([the study](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0090081))
- Kristen Gorman and the Palmer Station Long Term Ecological Research program collected them, with NSF support. ([palmerpenguins](https://allisonhorst.github.io/palmerpenguins/))
- They collected them for a 2014 PLOS ONE study, "Ecological Sexual Dimorphism and Environmental Variability within a Community of Antarctic Penguins (Genus *Pygoscelis*)", on how males and females differ in size and foraging. ([the study](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0090081))
- Each penguin's sex comes from a DNA test of a blood sample, not from its measurements. ([the study](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0090081))
- The table has 344 rows and 8 columns: species, island, bill length, bill depth, flipper length, body mass, sex and year. ([the package's introduction](https://allisonhorst.github.io/palmerpenguins/articles/intro.html))
- By species, there are 152 Adelie, 68 Chinstrap and 124 Gentoo. By year, 110 in 2007, 114 in 2008 and 120 in 2009.
- 2 rows have no measurements and 11 have no sex, so 333 rows are complete.
- The file is 15 KB.

## The study

- The project asks one question: how much heavier is a male penguin than a female of the same species?
- The number is male mean body mass minus female mean body mass, per species, in grams. Rows with no body mass or no sex are left out.

| Data | Rows | Adelie | Chinstrap | Gentoo |
|---|---|---|---|---|
| 2007 | 103 | 648.9 g | 250.0 g | 934.2 g |
| 2007 to 2009 | 333 | 674.7 g | 411.8 g | 805.1 g |

- In 2007 that's 22 males and 22 females for Adelie, 13 and 13 for Chinstrap, and 17 and 16 for Gentoo.
- It describes breeding adults with a recorded sex. It doesn't say why the species differ.
- Exercise 4 adds a classifier. It predicts a penguin's recorded sex from bill length, bill depth, flipper length, body mass and species.
- It's logistic regression on standardized measurements, trained on 2007 and 2008 (216 rows) and checked on 2009 (117 rows).
- Its validation accuracy is 0.846 at `C: 0.01` and 0.889 at `C: 1`.
- The study fit the same kind of model, logistic regression, one species at a time, and checked it on birds it hadn't fit. It reports 88.64 percent for Adelie, 94.44 percent for Chinstrap and 89.47 percent for Gentoo. ([the study](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0090081), Table 1)
- The classifier is a classroom example checked against a known label. It doesn't replace the DNA test.

## What each exercise adds

- The links open the Linux copies. Your track's menu has your machine's copy.
- [Exercise 1, Software environments](exercises/01-environments/environments-linux.ipynb): one script computes the 2007 table, and you declare and lock its environment with conda and with uv.
- [Exercise 2, Workflows](exercises/02-workflows/workflows-linux.ipynb): you start with a Snakemake or Nextflow workflow that computes the same table, then add a step that draws the README's figure. Git holds the code, and one command builds the numbers and the figure from the raw data.
- [Exercise 3, Versioning data](exercises/03-dataops/dataops-linux.ipynb): you version the data with DVC and store it in a bucket. You add the 2008 and 2009 seasons as a new version, then restore the 2007 data, table and figure.
- [Exercise 4, Model registry](exercises/04-registry/registry-linux.ipynb): you train the sex classifier at two values of `C`, register both versions with GTO, promote the better one and restore every version from the bucket.

## Why this example

- Gorman, Williams and Fraser measured the penguins over three austral summers from 2007/08, and published in PLOS ONE in 2014. ([the study](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0090081))
- Allison Horst, Alison Hill and Kristen Gorman released the data as the palmerpenguins R package in 2020. ([palmerpenguins](https://allisonhorst.github.io/palmerpenguins/))
- Zenodo archives that release, v0.1.0 of July 25, 2020, at doi:10.5281/zenodo.3960218.
- It's on CRAN, and there are versions for Python and Julia. ([Horst, Hill and Gorman, The R Journal, 2022](https://journal.r-project.org/articles/RJ-2022-020/))
- seaborn loads it with `load_dataset("penguins")`. ([seaborn](https://seaborn.pydata.org/generated/seaborn.load_dataset.html))
- `pip install palmerpenguins` installs a Python package of it. ([PyPI](https://pypi.org/project/palmerpenguins/))
- The authors' goal: "The goal of palmerpenguins is to provide a great dataset for data exploration & visualization, as an alternative to `iris`." ([palmerpenguins](https://allisonhorst.github.io/palmerpenguins/))
- Their reason, in The R Journal: "`iris` is burdened by a history in eugenics research". They add that it lacks metadata, and that two of its five variables, sepal width and sepal length, aren't intuitive for most people who aren't botanists. ([Horst, Hill and Gorman 2022](https://journal.r-project.org/articles/RJ-2022-020/))
- This workshop uses it because the file is 15 KB and every step runs in seconds on a CPU.
- Its three seasons arrive like data deliveries, which Exercise 3 needs.
- It has missing values, a question from a published study, and published classifier accuracy to compare with.

## License and citation

- The package says the data is "available by CC-0 license in accordance with the Palmer Station LTER Data Policy", and its [LICENSE.md](https://github.com/allisonhorst/palmerpenguins/blob/main/LICENSE.md) is CC0 1.0 Universal. ([palmerpenguins](https://allisonhorst.github.io/palmerpenguins/))
- The [Palmer LTER data page](https://pallter.marine.rutgers.edu/data/) now says its data is generally provided under Creative Commons Attribution 4.0, and asks you to cite the datasets.
- The workshop uses the package's copy, so CC0 applies. The citation below credits the study and the package either way.
- Cite it as: Data: palmerpenguins (Horst, Hill and Gorman 2020, doi:10.5281/zenodo.3960218), CC0, from Gorman, Williams and Fraser (2014), PLOS ONE 9(3): e90081. Collected by Palmer Station LTER with NSF support.
