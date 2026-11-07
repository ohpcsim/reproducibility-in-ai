# Model card: digits-clf

## Production version

Registered version in production: **v1.1.0** (`registered_version` in `release.yaml`; `stage: prod`).

Pipeline lock file: **dvc.lock**.

## Intended use

**For:** Classifying 8-by-8-pixel images of handwritten digits (dataset described in `sources.yaml`; artifact description in this repository).

**Must not be used for:** unknown.

## Dataset

- Name: Optical Recognition of Handwritten Digits (`sources.yaml`)
- Creators: E. Alpaydin and C. Kaynak (`sources.yaml`)
- Year: 1998 years CE (`sources.yaml`)
- DOI: 10.24432/C50P49 (`sources.yaml`)
- URL: https://archive.ics.uci.edu/dataset/80/optical+recognition+of+handwritten+digits (`sources.yaml`)
- License: CC BY 4.0; license URL https://creativecommons.org/licenses/by/4.0/ (`sources.yaml`)
- Images: 1797 images (`sources.yaml`)
- Image size: 8 by 8 pixels (`sources.yaml`)
- Classes: 10 classes (`sources.yaml`)
- Pixel values: 0 to 16 (pixel intensity units) (`sources.yaml`)
- Loaded with: sklearn.datasets.load_digits (`sources.yaml`)
- Software URL: https://scikit-learn.org/ (`sources.yaml`)

## Splits

Row counts from `release.yaml` (`split_sizes`):

| Split      | Rows | Unit | Source        |
|------------|------|------|---------------|
| train      | 1078 | rows | release.yaml  |
| validation | 359  | rows | release.yaml  |
| test       | 360  | rows | release.yaml  |

## Training parameters

- Split seed: 2026 (seed value) (`params.yaml`)
- Hidden units in the network's one hidden layer: 64 hidden units (`params.yaml`)

## Metrics

- Validation accuracy: **0.989** (accuracy, dimensionless fraction on \[0, 1\]) (`metrics.json`, field `val_accuracy`)
- Measured on: the validation split (`val`; 359 rows from `release.yaml`)

## Other versions

- Previous version: v1.0.0 (`release.yaml`)
