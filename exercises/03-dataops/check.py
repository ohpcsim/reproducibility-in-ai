#!/usr/bin/env python3
"""Check your work. Each part prints PASS or FAIL with what to do next. It reads what you committed.

It works in a throwaway clone with an empty DVC cache, so it can't damage your project,
and it gets every data version from your bucket.

Run it from project/: python ../check.py
python ../check.py --short runs the same check.
"""
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
PROJECT = HERE / "project"
BUCKET = HERE / "osn-bucket"
POINTER = "data/penguins.csv.dvc"

results = []


def mark(ok):
    word, color = ("PASS", 32) if ok else ("FAIL", 31)
    return f"\033[{color}m{word}\033[0m" if sys.stdout.isatty() or os.environ.get("CLICOLOR_FORCE") else word


def report(ok, message):
    results.append(ok)
    print(f"{mark(ok)}  {message}", flush=True)
    return ok


def run(*args, cwd=PROJECT):
    return subprocess.run(args, cwd=cwd, capture_output=True, text=True)


def headline(df):
    """The headline from the data itself: male minus female mean body mass, per species, and the row count."""
    df = df.dropna(subset=["body_mass_g", "sex"])
    mass = df.groupby(["species", "sex"])["body_mass_g"].mean().unstack()
    gap = mass["male"] - mass["female"]
    numbers = {f"dimorphism_g_{species.lower()}": round(float(grams), 1) for species, grams in gap.items()}
    numbers["n_rows"] = len(df)
    return numbers


def matches(metrics, data):
    return all(isinstance(metrics.get(key), (int, float)) and abs(metrics[key] - value) < 0.051
               for key, value in headline(data).items())


def restore(clone, commit):
    """Check out one commit in the clone and pull its data from the bucket. Returns the data, or None."""
    run("git", "checkout", "--quiet", "--force", commit, cwd=clone)
    if run("dvc", "pull", "--quiet", POINTER, cwd=clone).returncode != 0:
        return None
    try:
        return pd.read_csv(clone / "data" / "penguins.csv")
    except OSError:
        return None


def metrics_at(commit):
    try:
        return json.loads(run("git", "show", f"{commit}:metrics.json").stdout)
    except ValueError:
        return {}


def check_tracked():
    tracked = run("git", "ls-tree", "-r", "--name-only", "HEAD").stdout.split()
    if POINTER not in tracked:
        return report(False, "Your last commit has no data/penguins.csv.dvc, so DVC doesn't track the data yet. Do step 1.")
    if "data/penguins.csv" in tracked:
        return report(False, "Your last commit has the DVC pointer, and the data file is still in Git too. "
                             "Run git rm --cached data/penguins.csv, and commit.")
    return report(True, "DVC tracks the data: the pointer is in Git, and the data file isn't")


def main():
    if not (PROJECT / ".git").exists():
        print("FAIL  project/ is not there. From the folder above it, run: python scripts/setup_project.py")
        return 1
    if run("git", "status", "--porcelain").stdout.strip():
        print("Note: you have uncommitted changes. This checks your last commit only.\n", flush=True)
    has_pointer = check_tracked() or POINTER in run("git", "ls-tree", "-r", "--name-only", "HEAD").stdout.split()

    head = run("git", "rev-parse", "HEAD").stdout.strip()
    versions = run("git", "log", "--format=%H", "--", POINTER).stdout.split()
    with tempfile.TemporaryDirectory() as tmp:
        clone = Path(tmp) / "clone"
        run("git", "clone", "--quiet", str(PROJECT), str(clone), cwd=tmp)
        run("dvc", "remote", "modify", "--local", "storage", "url", str(BUCKET), cwd=clone)
        data = {commit: restore(clone, commit) for commit in dict.fromkeys([head] + versions)}

    latest = data.get(head)
    if not has_pointer:
        report(False, "There's no DVC pointer in your last commit, so a fresh clone has no data to pull. Do step 1.")
    else:
        report(latest is not None, "A fresh clone pulls the data from your bucket into an empty cache" if latest is not None else
               "A fresh clone with an empty cache could not pull data/penguins.csv. Run dvc push.")

    first = [c for c, d in data.items() if c in versions and d is not None and set(d["year"]) == {2007} and len(d) == 110]
    missing = [c for c in versions if data[c] is None]
    if any(matches(metrics_at(c), data[c]) for c in first):
        report(True, "The 2007 version restores from the bucket, and its commit's metrics.json matches it")
    elif first:
        report(False, "The 2007 version restores, but metrics.json in that commit doesn't match it. Run dvc repro before you commit.")
    elif missing:
        report(False, "A commit points to data that isn't in your bucket. Push every version: dvc push --all-commits")
    else:
        report(False, "No commit holds a DVC pointer to the 2007 season. Do step 1, and commit it before step 2.")

    if latest is None or len(latest) != 344 or set(latest["year"]) != {2007, 2008, 2009}:
        report(False, "Your last commit doesn't hold all three seasons, 2007 to 2009, from the bucket. Do step 2: commit, then dvc push.")
    else:
        ok = matches(metrics_at(head), latest)
        report(ok, "Your last commit holds all three seasons, and its metrics.json matches them" if ok else
               "Your last commit holds all three seasons, but its metrics.json doesn't match them. "
               "Run dvc repro, then commit dvc.lock and metrics.json.")

    print(f"\n{sum(results)} of {len(results)} parts pass.")
    if all(results):
        print("You're done. Each data version is in the bucket, and each commit brings back its data and its result.")
        return 0
    return 1


sys.exit(main())
