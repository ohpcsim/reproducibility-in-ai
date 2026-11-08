#!/usr/bin/env python3
"""Check committed versions, prod, a clean rebuild and every model in the bucket.

Run from project/: python ../check.py. --short runs the same full check.
All rebuilds and restores use throwaway clones.
"""
import json
import math
import os
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent / "scripts"))
from restore import PROJECT, restore, run

results = []


def report(ok, message):
    results.append(ok)
    word = "PASS" if ok else "FAIL"
    if sys.stdout.isatty() or os.environ.get("CLICOLOR_FORCE"):
        word = f"\033[{32 if ok else 31}m{word}\033[0m"
    print(f"{word}  {message}", flush=True)


def show(tag, path):
    return run("git", "show", f"{tag}:{path}", cwd=PROJECT).stdout


def registered():
    versions = {}
    tags = run("git", "tag", "--list", "penguin-sex-clf@*", cwd=PROJECT).stdout.split()
    for tag in tags:
        accuracy = json.loads(show(tag, "model_metrics.json"))["val_accuracy"]
        c = yaml.safe_load(show(tag, "params.yaml"))["train"]["C"]
        if not isinstance(accuracy, (int, float)) or not math.isfinite(accuracy):
            raise ValueError(f"{tag}: val_accuracy must be a finite number")
        versions[tag.split("@", 1)[1]] = {"accuracy": accuracy, "C": c}
    return versions


def check_rebuild(prod, recorded):
    tag = f"penguin-sex-clf@{prod}"
    try:
        with tempfile.TemporaryDirectory() as tmp:
            clone = restore(tag, Path(tmp))
            run("dvc", "repro", "--force", cwd=clone)
            again = json.loads((clone / "model_metrics.json").read_text())["val_accuracy"]
        ok = 0.65 <= again <= 0.95 and abs(again - recorded) <= 0.01
        report(ok, "Prod rebuild matches its recorded validation accuracy within 0.01, between 0.65 and 0.95" if ok else
               "Prod rebuild has an unexpected accuracy. Check train.py and the committed model_metrics.json.")
    except (subprocess.CalledProcessError, OSError, ValueError, KeyError) as error:
        report(False, f"Cannot restore and rebuild {tag}. Run dvc push --all-tags, then check dvc repro --force. {error}")


def check_all_versions(versions):
    missing = []
    for version in versions:
        try:
            with tempfile.TemporaryDirectory() as tmp:
                restore(f"penguin-sex-clf@{version}", Path(tmp))
        except (subprocess.CalledProcessError, OSError):
            missing.append(version)
    report(bool(versions) and not missing, "Every registered version restores from the bucket into its own empty folder" if versions and not missing else
           "Register the versions and run dvc push --all-tags. Missing: " + (", ".join(missing) or "no registered versions"))


def main():
    if not (PROJECT / ".git").is_dir():
        print("FAIL  Run python scripts/setup_project.py from the exercise folder first.")
        return 1
    try:
        versions = registered()
        distinct = {v["C"] for v in versions.values()}
        report(len(versions) >= 2 and len(distinct) >= 2,
               "At least two versions have different committed train.C values" if len(versions) >= 2 and len(distinct) >= 2 else
               "Register v1.0.0, train and commit a different C, then register v1.1.0 (steps 1 and 2).")
        prod = run("gto", "show", "penguin-sex-clf#prod", "--version", cwd=PROJECT).stdout.strip() if versions else ""
        best = max((v["accuracy"] for v in versions.values()), default=None)
        ok = prod in versions and versions[prod]["accuracy"] == best
        report(ok, "Prod is a registered version with the highest validation accuracy" if ok else
               "Compare model_metrics.json, then use gto assign penguin-sex-clf --version <best> --stage prod (step 3).")
        if prod in versions:
            check_rebuild(prod, versions[prod]["accuracy"])
        else:
            report(False, "Assign a registered version to prod before checking its clean rebuild.")
        check_all_versions(versions)
    except (subprocess.CalledProcessError, OSError, ValueError, KeyError, TypeError) as error:
        report(False, f"Cannot read the committed registry record. Check params.yaml and model_metrics.json at each version tag. {error}")
    print(f"\n{sum(results)} of {len(results)} parts pass.")
    if all(results):
        print("You're done. Prod is the registered version with the best validation score, and every registered model comes back from the bucket.")
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
