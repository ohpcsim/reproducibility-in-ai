"""Serve whatever the registry marks as prod, and score it on the test rows."""
import json
import os
import pickle
import subprocess
import sys
import tempfile

os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"

from sklearn.datasets import load_digits


def run(*args):
    return subprocess.run(args, capture_output=True, text=True)


version = run("gto", "show", "digits-clf#prod", "--version").stdout.strip()
if not version:
    sys.exit("score: nothing is in prod. Use gto assign.")
tag = f"digits-clf@{version}"

with tempfile.TemporaryDirectory() as tmp:
    path = os.path.join(tmp, "model.pkl")
    got = run("dvc", "get", ".", "model.pkl", "--rev", tag, "--out", path)
    if got.returncode != 0:
        sys.exit(f"score: prod is {version}, but I can't get its model from the cache or the bucket.")
    with open(path, "rb") as model_file:
        model = pickle.load(model_file)

test = json.loads(run("git", "show", f"{tag}:splits.json").stdout)["test"]
digits = load_digits()
print(f"prod is {version}. Accuracy on the {len(test)} test rows: {model.score(digits.data[test] / 16, digits.target[test]):.3f}")
