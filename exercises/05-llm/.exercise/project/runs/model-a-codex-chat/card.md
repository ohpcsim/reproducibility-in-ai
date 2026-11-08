# Model card: digits-clf

The production model is `digits-clf`, registered version `v1.1.0` (unit: registered version identifier; source: `release.yaml`), with stage `prod` (source: `release.yaml`).

The model is for classifying images of handwritten digits (sources: `README.md`, `artifacts.yaml`). It uses an `MLPClassifier` trained on the training rows (source: `train.py`). Per the review decision supplied by the user, this model is for teaching only. It must not be used to make a decision about a real person or to read real documents.

| Item | Value | Unit | Source |
| --- | --- | --- | --- |
| Validation accuracy | 0.989 | Fraction of correctly classified validation rows, dimensionless | `metrics.json`, key `val_accuracy`; measurement code in `train.py` |
| Train split size | 1078 | Rows | `release.yaml`, `split_sizes.train` |
| Validation split size | 359 | Rows | `release.yaml`, `split_sizes.val` |
| Test split size | 360 | Rows | `release.yaml`, `split_sizes.test` |
| Hidden layer width | 64 | Hidden units | `params.yaml`, `train.hidden` |

The validation accuracy was measured on the validation rows identified by `splits.json`, using the data and target labels returned by `sklearn.datasets.load_digits`; training uses the separate training rows (source: `train.py`). The dataset is named Optical Recognition of Handwritten Digits in `sources.yaml`. Test accuracy: unknown. Whether the supplied validation metric was measured on the registered production artifact: unknown; `metrics.json` does not identify a registered version.

The pipeline lock file is `dvc.lock`. It records the split and train stages, their dependencies, parameters, and outputs (source: `dvc.lock`).

Dataset URL: https://archive.ics.uci.edu/dataset/80/optical+recognition+of+handwritten+digits (source: `sources.yaml`, `dataset.url`).

Per the review decision supplied by the user, `candidate-v2` was refused because its training rows overlap its validation and test rows. This candidate name is the identifier supplied in that review decision.

Additional use restrictions, subgroup performance, and deployment limitations: unknown. No `decisions.yaml` is present in this folder; the review decisions above were supplied directly by the user.
