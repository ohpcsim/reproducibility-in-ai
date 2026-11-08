#!/usr/bin/env python3
"""Check your work. Each part prints PASS or FAIL with what to do next. It reads what you committed.

It works in a throwaway clone with an empty DVC cache, so it can't damage your project,
and it gets every data version, with its numbers and its figure, from your bucket. Nothing built is in Git.

Run it from project/: python ../check.py
python ../check.py --short runs the same check.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
PROJECT = HERE / "project"
BUCKET = HERE / "osn-bucket"
POINTER = "data/penguins.csv.dvc"
FIGURE = "figures/body_mass.svg"
BUILT = ("metrics.json", "figures/", "results/")

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


def plotted(df):
    """What the figure should show for this data: penguins and median body mass per species and sex."""
    mass = df.dropna(subset=["body_mass_g", "sex"]).groupby(["species", "sex"])["body_mass_g"]
    return {key: (int(count), round(float(median), 1)) for (key, count), median in zip(mass.size().items(), mass.median())}


def shown(svg):
    """What the figure shows, from plot.py's description in the SVG.
    The SVG's bytes depend on the font library in your environment, so the check reads what it plots, not its hash."""
    found = re.findall(r"(\w+) (female|male): (\d+) penguins, median ([\d.]+) g", svg)
    return {(name, sex): (int(count), float(median)) for name, sex, count, median in found}


def agrees(version):
    """The numbers and the figure DVC brought back for a commit match that commit's data."""
    numbers = version["metrics"] or {}
    return (all(isinstance(numbers.get(key), (int, float)) and abs(numbers[key] - value) < 0.051
                for key, value in headline(version["data"]).items())
            and shown(version["figure"]) == plotted(version["data"]))


def restore(clone, commit):
    """Check out one commit in the clone, delete what's built, and pull that commit's data and outputs from the bucket.
    Returns the data, metrics and figure, with None or "" for an output that didn't come back. None if the data didn't."""
    run("git", "checkout", "--quiet", "--force", commit, cwd=clone)
    for name in ("results", "figures"):
        shutil.rmtree(clone / name, ignore_errors=True)
    (clone / "metrics.json").unlink(missing_ok=True)
    run("dvc", "pull", "--quiet", cwd=clone)
    try:
        data = pd.read_csv(clone / "data" / "penguins.csv")
    except OSError:
        return None
    metrics, figure = clone / "metrics.json", clone / FIGURE
    return {"data": data,
            "metrics": json.loads(metrics.read_text()) if metrics.exists() else None,
            "figure": figure.read_text() if figure.exists() else ""}


def check_tracked(tracked):
    if POINTER not in tracked:
        return report(False, "Your last commit has no data/penguins.csv.dvc, so DVC doesn't track the data yet. Do step 1.")
    if "data/penguins.csv" in tracked:
        return report(False, "Your last commit has the DVC pointer, and the data file is still in Git too. "
                             "Run git rm --cached data/penguins.csv, and commit.")
    built = [name for name in tracked if name.startswith(BUILT)]
    if built:
        return report(False, f"Your last commit has built files in Git: {', '.join(built)}. DVC keeps them. "
                             f"Run git rm --cached {' '.join(built)}, and commit.")
    return report(True, "DVC tracks the data: the pointer is in Git, and the data and the built files aren't")


def main():
    if not (PROJECT / ".git").exists():
        print("FAIL  project/ is not there. From the folder above it, run: python scripts/setup_project.py")
        return 1
    if run("git", "status", "--porcelain").stdout.strip():
        print("Note: you have uncommitted changes. This checks your last commit only.\n", flush=True)
    tracked = run("git", "ls-tree", "-r", "--name-only", "HEAD").stdout.split()
    has_pointer = POINTER in tracked
    check_tracked(tracked)

    head = run("git", "rev-parse", "HEAD").stdout.strip()
    versions = run("git", "log", "--format=%H", "--", POINTER).stdout.split()
    with tempfile.TemporaryDirectory() as tmp:
        clone = Path(tmp) / "clone"
        run("git", "clone", "--quiet", str(PROJECT), str(clone), cwd=tmp)
        run("dvc", "remote", "modify", "--local", "storage", "url", str(BUCKET), cwd=clone)
        data = {commit: restore(clone, commit) for commit in dict.fromkeys([head] + versions)}

    def complete(version):
        return version is not None and version["metrics"] is not None and bool(version["figure"])

    latest = data.get(head)
    if not has_pointer:
        report(False, "There's no DVC pointer in your last commit, so a fresh clone has no data to pull. Do step 1.")
    else:
        ok = complete(latest)
        report(ok, "A fresh clone pulls the data, metrics.json and the figure from your bucket into an empty cache" if ok else
               "A fresh clone with an empty cache could not pull the data, metrics.json and the figure. Run dvc push.")

    first = [c for c in versions if data[c] is not None and set(data[c]["data"]["year"]) == {2007} and len(data[c]["data"]) == 110]
    if any(complete(data[c]) and agrees(data[c]) for c in first):
        report(True, "The 2007 version restores from the bucket, with its numbers and its figure, and they match its data")
    elif any(complete(data[c]) for c in first):
        report(False, "The 2007 version restores, but its numbers or its figure don't match its data. Run dvc repro before you commit.")
    elif first or any(not complete(data[c]) for c in versions):
        report(False, "A commit points to data or outputs that aren't in your bucket. Push every version: dvc push --all-commits")
    else:
        report(False, "No commit holds a DVC pointer to the 2007 season. Do step 1, and commit it before step 2.")

    if latest is None or len(latest["data"]) != 344 or set(latest["data"]["year"]) != {2007, 2008, 2009}:
        report(False, "Your last commit doesn't hold all three seasons, 2007 to 2009, from the bucket. Do step 2: commit, then dvc push.")
    elif not complete(latest):
        report(False, "Your last commit holds all three seasons, and its metrics.json or figure isn't in the bucket. Run dvc push.")
    else:
        ok = agrees(latest)
        report(ok, "Your last commit holds all three seasons, and its numbers and its figure match them" if ok else
               "Your last commit holds all three seasons, but its numbers or its figure don't match them. "
               "Run dvc repro, then commit dvc.lock, and run dvc push.")

    print(f"\n{sum(results)} of {len(results)} parts pass.")
    if all(results):
        print("You're done. Each data version is in the bucket, and each commit brings back its data, its numbers and its figure.")
        return 0
    return 1


sys.exit(main())
