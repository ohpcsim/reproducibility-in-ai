# Model Card — digits-clf

## Production status

| Field | Value | Source |
| --- | --- | --- |
| Artifact | digits-clf | release.yaml |
| Registered version in production | v1.1.0 | release.yaml |
| Stage | prod | release.yaml |
| Previous version | v1.0.0 | release.yaml |
| Pipeline lock file | dvc.lock | dvc.lock (lock file recording the pipeline) |

## What the model is for

Per `decisions.yaml` (id: `intended-use`):

> This model is for teaching only. It must not be used to make a decision about a real person or to read real documents.

The model classifies 8 by 8 pixel images of handwritten digits into 10 classes (`sources.yaml`: `image_size` = 8 by 8 pixels, `classes` = 10 classes).

## What it must not be used for

Per `decisions.yaml` (id: `intended-use`), the model:

- must not be used to make a decision about a real person; and
- must not be used to read real documents.

Its use is limited to teaching only.

## Model and pipeline

| Field | Value | Source |
| --- | --- | --- |
| Model artifact file | model.pkl | artifacts.yaml |
| Hidden layer | one hidden layer | params.yaml (`train.hidden` comment) |
| Hidden units | 64 hidden units | params.yaml |
| Split random seed | 2026 (unitless) | params.yaml |
| Pipeline stages | split and train | dvc.lock |
| Model algorithm / family | unknown | not stated in metrics.json, params.yaml, release.yaml or sources.yaml |

The pipeline is recorded in the lock file `dvc.lock`. Its `split` stage writes `splits.json`; its `train` stage writes `model.pkl` and `metrics.json`.

## Data

| Field | Value | Source |
| --- | --- | --- |
| Dataset | Optical Recognition of Handwritten Digits | sources.yaml |
| Creators | E. Alpaydin and C. Kaynak | sources.yaml |
| Year | 1998 (year) | sources.yaml |
| DOI | 10.24432/C50P49 (identifier, no unit) | sources.yaml |
| License | CC BY 4.0 (license version identifier) | sources.yaml |
| Images | 1797 images | sources.yaml |
| Image size | 8 by 8 pixels | sources.yaml |
| Classes | 10 classes | sources.yaml |
| Pixel values | 0 to 16 (unitless pixel values) | sources.yaml |
| Loaded with | sklearn.datasets.load_digits | sources.yaml |
| Software | scikit-learn | sources.yaml |

### Split sizes

| Split | Rows | Source |
| --- | --- | --- |
| Train | 1078 rows | release.yaml |
| Validation | 359 rows | release.yaml |
| Test | 360 rows | release.yaml |

## Evaluation

| Field | Value | Source |
| --- | --- | --- |
| Validation accuracy | 0.989 (proportion, unitless) | metrics.json |
| Measured on | the validation split, 359 rows | release.yaml |
| Test accuracy | unknown | not recorded in metrics.json, params.yaml, release.yaml or sources.yaml |

The validation accuracy is `0.989`, reported to three decimal places as recorded in `metrics.json`. It was measured on the validation split, which contains 359 rows according to `release.yaml`.

## Decisions

From `decisions.yaml`:

- **intended-use:** This model is for teaching only. It must not be used to make a decision about a real person or to read real documents.
- **refused-candidate:** We refused candidate-v2, because its training rows overlap its validation and test rows.

## URLs

| URL | Source |
| --- | --- |
| https://archive.ics.uci.edu/dataset/80/optical+recognition+of+handwritten+digits | sources.yaml (`dataset.url`) |
| https://creativecommons.org/licenses/by/4.0/ | sources.yaml (`dataset.license_url`) |
| https://scikit-learn.org/ | sources.yaml (`software.scikit_learn`) |

## Not stated in the source files

- Model license: unknown
- Model architecture / algorithm family: unknown
- Test accuracy: unknown
- Model owners or contact: unknown
- Limitations beyond the intended-use restrictions in `decisions.yaml`: unknown
