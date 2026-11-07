# Digit classifier

We serve one model: a small neural network that reads handwritten digits.

- `split.py` writes `splits.json`, the lists of training, validation and test rows.
- `train.py` trains on the training rows and writes `model.pkl` and `metrics.json`.
- `score.py` serves whatever the registry marks as prod, and scores it on the test rows.

The registry is `gto`. Try `gto show`.
