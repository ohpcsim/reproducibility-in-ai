# Model card: digits-clf

## Production status

- **Artifact:** digits-clf (`release.yaml`)
- **Registered version in prod:** `v1.1.0` (`release.yaml`, where `stage: prod`)
- **Pipeline lock file:** `dvc.lock` — the lock file that records the `split` and `train` stages, their parameters, and their outputs
- **Pipeline definition:** `dvc.yaml`

## What the model is for

The model classifies images of handwritten digits. `artifacts.yaml` describes it as a classifier of such images, and `sources.yaml` records the image size and dataset details below. It is the single model served from this repository (`README.md`).

## What it must not be used for

**unknown.** No file in this folder states a prohibited or out-of-scope use for this model, and `metrics.json`, `params.yaml`, `release.yaml` and `sources.yaml` contain no usage restrictions. This card does not invent one.

## Model and training

- A small neural network with one hidden layer (`params.yaml`; see `train.py`).
- Hidden layer width: 64 hidden units (`params.yaml`).
- Split seed: 2026 (random seed, integer; `params.yaml`).
- The pipeline runs the `split` stage and then the `train` stage, as recorded in `dvc.lock`.
- Outputs recorded in `dvc.lock`: `splits.json`, `model.pkl`, `metrics.json`.

## Data

- Dataset: Optical Recognition of Handwritten Digits (`sources.yaml`).
- Creators: E. Alpaydin and C. Kaynak (`sources.yaml`).
- Year: 1998 (year; `sources.yaml`).
- DOI: 10.24432/C50P49 (identifier; `sources.yaml`).
- Dataset page: https://archive.ics.uci.edu/dataset/80/optical+recognition+of+handwritten+digits (`sources.yaml`).
- License: CC BY 4.0 (`sources.yaml`).
- License text: https://creativecommons.org/licenses/by/4.0/ (`sources.yaml`).
- Images: 1797 images (`sources.yaml`).
- Image size: 8 by 8 pixels, i.e. 8 pixels per side (`sources.yaml`).
- Classes: 10 classes (`sources.yaml`).
- Pixel values: range 0 to 16 (`sources.yaml` does not name a unit for these pixel values).
- Loaded with: `sklearn.datasets.load_digits` (`sources.yaml`).
- Software: scikit-learn — https://scikit-learn.org/ (`sources.yaml`).

### Split sizes

| Split | Rows | Source |
| --- | --- | --- |
| Train | 1078 rows | `release.yaml` |
| Validation | 359 rows | `release.yaml` |
| Test | 360 rows | `release.yaml` |

## Performance

- **Validation accuracy: 0.989**, to three decimal places (fraction of the 359 validation rows classified correctly; a unitless proportion) — from `metrics.json`. It was measured on the **validation split** (`train.py` scores the fitted model on the validation rows; the row count above is from `release.yaml`).
- **Test accuracy: unknown.** No test-set score is recorded in `metrics.json`, `params.yaml`, `release.yaml` or `sources.yaml`. `score.py` computes a test score when run, but its result is not stored in any of those files.

## Numbers and their sources

Every numeral in this card, with its unit and the file it came from:

| Value | Unit / meaning | File |
| --- | --- | --- |
| v1.1.0 | version string (no unit) | `release.yaml` |
| 64 | hidden units (count) | `params.yaml` |
| 2026 | random seed (integer) | `params.yaml` |
| 1078 | rows (count) | `release.yaml` |
| 359 | rows (count) | `release.yaml` |
| 360 | rows (count) | `release.yaml` |
| 0.989 | fraction of validation rows correct (no unit) | `metrics.json` |
| 1797 | images (count) | `sources.yaml` |
| 8 by 8 | pixels (image side length) | `sources.yaml` |
| 10 | classes (count) | `sources.yaml` |
| 0 to 16 | pixel value range (unit not named in source) | `sources.yaml` |
| 1998 | year | `sources.yaml` |
| 10.24432/C50P49 | DOI identifier (no unit) | `sources.yaml` |
| CC BY 4.0 | license name including version (no unit) | `sources.yaml` |

All URLs in this card come from `sources.yaml`.

## Decisions

No `decisions.yaml` file exists in this folder, so there are no recorded decisions to include.
