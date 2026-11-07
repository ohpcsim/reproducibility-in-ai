#!/usr/bin/env python3
"""Check your work. Each part prints PASS or FAIL with what to do next. It reads what you committed.

It works in a throwaway clone, so it can't damage your project. It plants its own bad
deliveries, so it doesn't hold a list of answers to look up.

python check.py --short   checks step 1, the short path.
python check.py           checks everything.
"""
import json
import os
import random
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import pandas as pd
import yaml

HERE = Path(__file__).resolve().parent
PROJECT = HERE / "project"
BUCKET = HERE / "osn-bucket"
TABLE = HERE / "data" / "penguins.csv"

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


def usable(df):
    return df.dropna(subset=["flipper_length_mm", "body_mass_g"])


def within_species_slope(df):
    x = df["flipper_length_mm"] - df.groupby("species")["flipper_length_mm"].transform("mean")
    y = df["body_mass_g"] - df.groupby("species")["body_mass_g"].transform("mean")
    return (x * y).sum() / (x * x).sum()


def plant_inches(df, rng, count=3):
    df = df.copy()
    rows = rng.sample(list(usable(df).index), count)
    df.loc[rows, "flipper_length_mm"] = (df.loc[rows, "flipper_length_mm"] / 25.4).round(2)
    return df


def plant_duplicates(df, rng, count=2):
    rows = rng.sample(list(usable(df).index), count)
    return pd.concat([df, df.loc[rows]], ignore_index=True)


def plant_typo(df, rng):
    df = df.copy()
    rows = rng.sample(list(df.index[df["species"] == "Adelie"]), 2)
    df.loc[rows, "species"] = "Adeile"
    return df


class Clone:
    """A clone of your last commit, with its data pulled from your bucket into an empty cache."""

    def __init__(self, path):
        self.path = path

    def pull(self):
        cloned = run("git", "clone", "--quiet", str(PROJECT), str(self.path), cwd=self.path.parent)
        if cloned.returncode != 0:
            return cloned.stderr
        run("dvc", "remote", "modify", "--local", "storage", "url", str(BUCKET), cwd=self.path)
        pulled = run("dvc", "pull", cwd=self.path)
        if pulled.returncode != 0:
            return pulled.stderr + pulled.stdout
        return None

    def set_policy(self, **flags):
        path = self.path / "params.yaml"
        params = yaml.safe_load(path.read_text())
        params["clean"].update(flags)
        path.write_text(yaml.safe_dump(params))

    def deliver(self, df):
        df.to_csv(self.path / "data" / "penguins.csv", index=False)

    def repro(self):
        return run("dvc", "repro", cwd=self.path)

    def metrics(self):
        return json.loads((self.path / "metrics.json").read_text())


def check_committed():
    tracked = run("git", "ls-tree", "-r", "--name-only", "HEAD").stdout.split()
    missing = [f for f in ("dvc.yaml", "dvc.lock", "metrics.json", "data/penguins.csv.dvc") if f not in tracked]
    if missing:
        return report(False, f"Not committed yet: {', '.join(missing)}. Run the setup cells, which commit them.")
    stages = yaml.safe_load(run("git", "show", "HEAD:dvc.yaml").stdout).get("stages", {})
    absent = [s for s in ("clean", "validate", "report") if s not in stages]
    if absent:
        return report(False, f"dvc.yaml has no stage named {', '.join(absent)}. check.py looks for these names.")
    return report(True, "The pipeline is committed")


def check_season(clone, full, first_season):
    metrics = clone.metrics()
    if metrics.get("n_rows") != len(usable(full)):
        report(False, "Your last commit doesn't hold the new delivery, cleaned. Finish step 2 and commit it, then dvc push.")
        return
    close = abs(metrics["slope_g_per_mm"] - within_species_slope(usable(first_season))) < 0.5
    report(close, "The cleaned delivery reproduces the first season's slope" if close else
           "The row count is right, but the slope doesn't match the first season's. Look at how clean.py converts the inches.")


def check_refusals(clone, full, rng):
    repairs_off = {"convert_inches": False, "drop_duplicates": False, "drop_missing_sex": False}
    clone.set_policy(**repairs_off)
    clone.deliver(full)
    good = clone.repro()
    if not report(good.returncode == 0, "Good data passes validate" if good.returncode == 0 else
                  "The clean, published table failed your pipeline with the repairs off. Your checks are too strict, "
                  "or a script broke. Run dvc repro on it to see the message."):
        return False
    planted = {"flipper lengths in inches": plant_inches, "repeated rows": plant_duplicates, "a misspelled species": plant_typo}
    for name, plant in planted.items():
        clone.deliver(plant(full, rng))
        result = clone.repro()
        stopped = result.returncode != 0 and "validate" in result.stdout + result.stderr
        report(stopped, f"dvc repro stops at validate on {name}" if stopped else
               f"I planted a delivery with {name}, with the repairs off, and dvc repro did not stop at validate. "
               "Add a check to validate.py.")
    return True


def check_policy_declared(clone, full):
    clone.set_policy(convert_inches=False, drop_duplicates=False, drop_missing_sex=False)
    clone.deliver(full)
    clone.repro()
    before = clone.metrics()["n_rows"]
    clone.set_policy(drop_missing_sex=True)
    result = clone.repro()
    after = clone.metrics()["n_rows"] if result.returncode == 0 else before
    ok = after < before
    report(ok, "Changing the policy rebuilds the report" if ok else
           "I changed drop_missing_sex and the report didn't rebuild. Declare the policy as a dependency in dvc.yaml.")


def check_repairs(clone, full, rng):
    clone.set_policy(convert_inches=True, drop_duplicates=True, drop_missing_sex=False)
    clone.deliver(plant_duplicates(plant_inches(full, rng, count=25), rng, count=7))
    result = clone.repro()
    if result.returncode != 0:
        report(False, "With convert_inches and drop_duplicates on, a delivery with both problems should pass. It stopped. "
                      "Make clean.py read those two settings and do the repairs.")
        return
    metrics = clone.metrics()
    ok = metrics["n_rows"] == len(usable(full)) and abs(metrics["slope_g_per_mm"] - within_species_slope(usable(full))) < 0.05
    report(ok, "With the repairs on, clean.py repairs a new bad delivery" if ok else
           "With the repairs on, I planted new inches and repeats, and the result didn't match the good table. "
           "Check that clean.py uses both settings.")


def check_rolled_back():
    diff = run("dvc", "metrics", "diff")
    ok = diff.returncode == 0 and not diff.stdout.strip()
    report(ok, "Your workspace is back at your last commit: dvc metrics diff is empty" if ok else
           "dvc metrics diff in project/ isn't empty, so your workspace doesn't match your last commit. "
           "Roll back with the commands in step 1, or commit the result you want to keep.")


def check_negative_control():
    text = run("git", "show", "HEAD:negative-control.txt").stdout
    moved = False
    for line in text.splitlines():
        fields = line.split()
        if "slope_g_per_mm" in fields:
            try:
                moved = float(fields[-1]) != 0
            except ValueError:
                moved = False
    report(moved, "negative-control.txt shows the slope moved" if moved else
           "Commit negative-control.txt: the dvc metrics diff from changing one row. The slope has to move (step 3).")


def main():
    short = "--short" in sys.argv
    if not (PROJECT / ".git").exists():
        print("FAIL  project/ is not there. Run: python scripts/setup_project.py")
        return 1
    if run("git", "status", "--porcelain").stdout.strip():
        print("Note: you have uncommitted changes. This checks your last commit only.\n", flush=True)
    if not check_committed():
        print("\nThe setup cells come first.")
        return 1

    full = pd.read_csv(TABLE)
    first_season = full[full["year"] == 2007]
    rng = random.Random()
    with tempfile.TemporaryDirectory() as tmp:
        clone = Clone(Path(tmp) / "clone")
        problem = clone.pull()
        if not report(problem is None, "A fresh clone pulls everything into an empty cache" if problem is None else
                      "A fresh clone with an empty cache could not get its data. Run dvc push after your last dvc repro."):
            print("\nThe other parts need that data, so fix this first.")
            return 1
        check_rolled_back()
        if short:
            check_refusals(clone, full, rng)
            print(f"\n{sum(results)} of {len(results)} parts pass.")
            if all(results):
                print("You've finished the short path. Steps 2 and 3 are optional. To check them too, run: python check.py")
                return 0
            return 1
        check_season(clone, full, first_season)
        if check_refusals(clone, full, rng):
            check_policy_declared(clone, full)
        check_repairs(clone, full, rng)
    check_negative_control()
    print(f"\n{sum(results)} of {len(results)} parts pass.")
    if all(results):
        print("You're done. A bad delivery now stops the pipeline, and a repair needs a recorded decision.")
        return 0
    return 1


sys.exit(main())
