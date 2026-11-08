# Model card: digits-clf

Every number and URL below comes from `metrics.json`, `params.yaml`, `release.yaml` or `sources.yaml`, as noted. Anything those files do not state is marked **unknown**.

## Model details

| Item | Value | Unit | Source |
|---|---|---|---|
| Artifact name | `digits-clf` | — | `release.yaml` (`artifact`) |
| Registered version in prod | `v1.1.0` | version tag | `release.yaml` (`registered_version`, `stage: prod`) |
| Previous version | `v1.0.0` | version tag | `release.yaml` (`previous_version`) |
| Model type | Small neural network: one hidden layer, scikit-learn `MLPClassifier` | — | `train.py` (architecture; not one of the four named files, so no numbers are taken from it) |
| Hidden units in the hidden layer | 64 | neurons | `params.yaml` (`train.hidden`) |
| Serialized model file | `model.pkl` | file | `artifacts.yaml`, `dvc.yaml` |
| Pipeline lock file | `dvc.lock` | file | `dvc.lock` (records the `split` and `train` stages) |
| Registry | `gto` | — | `README.md` |

Note: the folder does not include the registry state. The prod assignment of `v1.1.0` is taken from `release.yaml`. Whether the registry currently agrees is **unknown** from these files.

## Intended use

Classifying 8x8 pixel images of handwritten digits into one of 10 classes (`sources.yaml`: `images: 1797`, `image_size: 8 by 8 pixels`, `classes: 10`).

Described in `README.md`: the served model is a small neural network that reads handwritten digits. `score.py` serves whatever the registry marks as prod and scores it on the test rows.

## Out-of-scope use

The files in this folder contain no list of prohibited uses. Formal out-of-scope uses: **unknown**.

What the files do establish about the limits of the evidence:

- The model was trained and validated only on the UCI Optical Recognition of Handwritten Digits data (`sources.yaml`). It has no evidence in these files for other image sizes, other pixel scales, other datasets, or other handwriting sources.
- Its only reported quality number is a validation accuracy (below). No accuracy on any other data is recorded in these files.

The owner should confirm the out-of-scope list before the model is used for anything beyond the intended use above.

## Training data

- Dataset: Optical Recognition of Handwritten Digits (`sources.yaml`, `dataset.name`)
- Creators: E. Alpaydin and C. Kaynak, 1998 (`sources.yaml`)
- Images: 1797 (unit: images) (`sources.yaml`, `dataset.images`)
- Image size: 8 by 8 pixels (`sources.yaml`, `dataset.image_size`)
- Pixel values: 0 to 16 (unit: intensity levels) (`sources.yaml`, `dataset.pixel_values`)
- Classes: 10 (`sources.yaml`, `dataset.classes`)
- Loaded with: `sklearn.datasets.load_digits` (`sources.yaml`, `dataset.loaded_with`)
- DOI: 10.24432/C50P49 (`sources.yaml`, `dataset.doi`)
- Dataset URL: https://archive.ics.uci.edu/dataset/80/optical+recognition+of+handwritten+digits (`sources.yaml`, `dataset.url`)
- Dataset license: CC BY 4.0 (`sources.yaml`, `dataset.license`), https://creativecommons.org/licenses/by/4.0/ (`sources.yaml`, `dataset.license_url`)
- Software: scikit-learn, https://scikit-learn.org/ (`sources.yaml`, `software.scikit_learn`)

## Data splits

Row counts are from `release.yaml` (`split_sizes`). Unit: image rows.

| Split | Rows | Source |
|---|---|---|
| Train | 1078 | `release.yaml` (`split_sizes.train`) |
| Validation | 359 | `release.yaml` (`split_sizes.val`) |
| Test | 360 | `release.yaml` (`split_sizes.test`) |

The split is made with a random seed of 2026 (unit: integer seed) from `params.yaml` (`split.seed`). The row lists are stored in `splits.json`.

## Evaluation

- Validation accuracy: **0.989** (unit: fraction of correctly classified rows, from 0 to 1) (`metrics.json`, `val_accuracy`)
- Measured on: the **validation split**, 359 image rows (`release.yaml`, `split_sizes.val`). `train.py` computes this score on the validation rows after training on the training rows.
- Test accuracy: **unknown**. `score.py` prints a test accuracy when run, but no value is recorded in these files.
- Whether the `metrics.json` in this folder was produced by the `v1.1.0` run is **unknown** from these files alone. `dvc.lock` records the current hash of `metrics.json`, but not the version tag.

## Training procedure

- Lock file recording the pipeline: `dvc.lock`
- Pipeline stages (from `dvc.lock`): `split` (`python split.py`) and `train` (`python train.py`)
- Training parameter: hidden units = 64 (`params.yaml`, `train.hidden`)
- Split parameter: seed = 2026 (`params.yaml`, `split.seed`)
- Other training settings are in `train.py` only and are not recorded in the four named files, so they are not stated here.

## Decisions

No `decisions.yaml` exists in this folder, so there are no recorded decisions to follow or include.

## Limitations and unknowns

- Test accuracy: **unknown** (see Evaluation).
- Prohibited uses: **unknown** (see Out-of-scope use).
- Registry state: not in this folder (`gto` is referenced in `README.md` and `score.py`, but its state is not recorded here).
- Fairness, robustness, and error analysis: **unknown**. The files record no such analysis.
