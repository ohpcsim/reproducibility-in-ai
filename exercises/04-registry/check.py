#!/usr/bin/env python3
"""Check your work. Each part prints PASS or FAIL with what to do next. It reads what you committed.

It works in throwaway clones, so it can't damage your project. It works out the right
answer from what you registered, so there's no answer in this file to look up.

Run it from project/:
python ../check.py --short   checks step 1, the short path.
python ../check.py           checks everything.
"""
import json
import os
import random
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJECT = HERE / "project"
BUCKET = HERE / "osn-bucket"

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


def show(ref, path):
    return run("git", "show", f"{ref}:{path}").stdout


def disjoint(splits):
    train, val, test = (set(splits[k]) for k in ("train", "val", "test"))
    return not (train & val or train & test or val & test)


def registered():
    """Each registered version with its validation accuracy, for versions whose splits don't overlap."""
    versions = {}
    for tag in run("git", "tag", "--list", "digits-clf@*").stdout.split():
        try:
            versions[tag.split("@", 1)[1]] = {
                "accuracy": json.loads(show(tag, "metrics.json"))["val_accuracy"],
                "clean": disjoint(json.loads(show(tag, "splits.json"))),
            }
        except (ValueError, KeyError):
            versions[tag.split("@", 1)[1]] = {"accuracy": None, "clean": False}
    return versions


def clone_into(tmp, ref=None):
    clone = Path(tmp) / "clone"
    run("git", "clone", "--quiet", str(PROJECT), str(clone), cwd=tmp)
    run("dvc", "remote", "modify", "--local", "storage", "url", str(BUCKET), cwd=clone)
    if ref:
        run("git", "checkout", "--quiet", ref, cwd=clone)
    return clone


def check_versions(versions):
    usable = [v for v in versions.values() if v["accuracy"] is not None]
    report(len(usable) >= 2, f"{len(usable)} versions are registered" if len(usable) >= 2 else
           "Register at least two versions. Train a second width, commit it, and use gto register (step 1).")


def check_prod_choice(versions):
    prod = run("gto", "show", "digits-clf#prod", "--version").stdout.strip()
    if prod not in versions:
        report(False, "Nothing registered is in prod. Use gto assign --stage prod.")
        return None
    if not versions[prod]["clean"]:
        report(False, "The version in prod has rows that are in more than one of train, val and test. Move prod to a clean version.")
        return prod
    best = max(v["accuracy"] for v in versions.values() if v["clean"])
    ok = versions[prod]["accuracy"] >= best
    report(ok, "Prod is the version with the best validation accuracy" if ok else
           "Another registered version has better validation accuracy than the one in prod. Compare them with dvc metrics diff.")
    return prod


def check_prod_rebuilds(prod):
    tag = f"digits-clf@{prod}"
    with tempfile.TemporaryDirectory() as tmp:
        clone = clone_into(tmp)
        served = run(sys.executable, "score.py", cwd=clone)
        if not report(served.returncode == 0, "score.py serves prod from an empty cache" if served.returncode == 0 else
                      f"A fresh clone can't serve prod, which is {prod}. Its model isn't in the bucket. In project/, run git checkout digits-clf@{prod}, then dvc push, then git checkout main."):
            return
        run("git", "checkout", "--quiet", tag, cwd=clone)
        rebuilt = run("dvc", "repro", "--force", cwd=clone)
        if rebuilt.returncode != 0:
            report(False, f"dvc repro --force failed at {tag}. Check out that tag and run it to see why.")
            return
        again = json.loads((clone / "metrics.json").read_text())["val_accuracy"]
        recorded = json.loads(show(tag, "metrics.json"))["val_accuracy"]
        ok = 0.96 <= again <= 0.999 and abs(again - recorded) <= 0.01
        report(ok, "Rebuilding prod from scratch gives a believable accuracy that matches its record" if ok else
               "Rebuilding prod from scratch gave a validation accuracy that doesn't match its record, or that's too good or too poor to believe.")


def plant_overlap(splits, rng, first, second):
    planted = {k: list(v) for k, v in splits.items()}
    planted[first].append(rng.choice(planted[second]))
    return planted


def check_split_test():
    test_file = show("HEAD", "tests/test_split.py")
    if not test_file:
        report(False, "Commit tests/test_split.py, which reads splits.json and tests that the row lists don't overlap (step 2).")
        return
    candidate = show("candidate-v2", "splits.json")
    good = show("HEAD", "splits.json")
    rng = random.Random()
    good_splits = json.loads(good)
    cases = {"candidate-v2": candidate}
    for first, second in (("train", "test"), ("train", "val"), ("val", "test")):
        cases[f"one row shared by {first} and {second}"] = json.dumps(plant_overlap(good_splits, rng, first, second))

    def result(splits_text):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            (folder / "tests").mkdir()
            (folder / "tests" / "test_split.py").write_text(test_file)
            (folder / "splits.json").write_text(splits_text)
            return run(sys.executable, "-m", "pytest", "-q", "--color=no", "-p", "no:cacheprovider", "tests/test_split.py", cwd=folder).returncode

    passes = result(good) == 0
    if not report(passes, "Your split test passes on your own clean splits" if passes else
                  "Your split test should pass on clean splits, and it fails on yours. It needs to read splits.json from the project folder."):
        return
    for name, text in cases.items():
        fails = result(text) == 1
        report(fails, f"Your split test fails on {name}" if fails else
               f"I gave your split test {name}, and it didn't fail. Test every pair of lists.")


def check_refusal():
    text = show("HEAD", "decisions.md")
    named = "candidate-v2" in text
    reason = re.search(r"overlap|leak|disjoint|test rows|same rows|shared", text, re.I) is not None
    ok = named and reason and len(text) >= 60
    report(ok, "decisions.md refuses the candidate and says why" if ok else
           "Commit decisions.md. Name candidate-v2 and say what's wrong with its rows, so the next person doesn't have to find it again.")


def check_all_versions(versions):
    missing = []
    with tempfile.TemporaryDirectory() as tmp:
        clone = clone_into(tmp)
        for version in versions:
            run("git", "checkout", "--quiet", f"digits-clf@{version}", cwd=clone)
            (clone / "model.pkl").unlink(missing_ok=True)
            if run("dvc", "pull", cwd=clone).returncode != 0 or not (clone / "model.pkl").exists():
                missing.append(version)
    report(not missing, "Every registered version restores from the bucket into an empty folder" if not missing else
           f"These versions aren't in the bucket: {', '.join(missing)}. See step 3.")


def main():
    if not (PROJECT / ".git").exists():
        print("FAIL  project/ is not there. From the folder above it, run: python scripts/setup_project.py")
        return 1
    versions = registered()
    if not versions:
        print("FAIL  Nothing is registered. From the folder above project/, run: python scripts/setup_project.py --reset")
        return 1
    check_versions(versions)
    prod = check_prod_choice(versions)
    if prod in versions and versions[prod]["clean"]:
        check_prod_rebuilds(prod)
    if "--short" in sys.argv:
        print(f"\n{sum(results)} of {len(results)} parts pass.")
        if all(results):
            print("You've finished the short path. Steps 2 and 3 are optional. To check them too, run: python ../check.py")
            return 0
        return 1
    check_split_test()
    check_refusal()
    check_all_versions(versions)
    print(f"\n{sum(results)} of {len(results)} parts pass.")
    if all(results):
        print("You're done. Prod is the honest best, the leaky candidate is refused in writing, and every version restores by tag.")
        return 0
    return 1


sys.exit(main())
