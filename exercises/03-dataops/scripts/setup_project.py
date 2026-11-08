#!/usr/bin/env python3
"""Build the starting repository in project/: Exercise 2's pipeline on the 2007 field season, declared as DVC stages.

Run it again and it leaves your work alone. To start over, use --reset. That deletes your work.
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
FILES = HERE / ".exercise" / "project"
PROJECT = HERE / "project"
BUCKET = HERE / "osn-bucket"
ENV = {**os.environ, "GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_NOSYSTEM": "1"}
# A fixed date, so every learner gets the commit IDs on the page.
STAMP = "2025-04-03T10:00:00+0000"


def run(*args, env=ENV):
    subprocess.run(args, cwd=PROJECT, env=env, check=True, capture_output=True)


def git(*args):
    run("git", *args, env={**ENV, "GIT_AUTHOR_DATE": STAMP, "GIT_COMMITTER_DATE": STAMP})


def stage(name, inputs, outputs, script):
    flags = [flag for path in inputs for flag in ("-d", path)] + list(outputs)
    run("dvc", "stage", "add", "--quiet", "-n", name, *flags, "python", script)


def build():
    shutil.copytree(FILES, PROJECT)
    # The first season is the 2007 rows of the full table, byte for byte.
    lines = (HERE / ".exercise" / "data" / "penguins.csv").read_text().splitlines(keepends=True)
    season = [lines[0]] + [line for line in lines[1:] if line.strip().endswith(",2007")]
    (PROJECT / "data").mkdir()
    (PROJECT / "data" / "penguins.csv").write_text("".join(season))
    for script in ("clean.py", "validate.py", "report.py"):
        run(sys.executable, script)

    # Exercise 2's end state: the scripts, the Snakefile, the data and the result, all in Git.
    git("init", "--quiet", "--initial-branch=main")
    git("config", "core.autocrlf", "false")
    git("config", "user.name", "Workshop Learner")
    git("config", "user.email", "learner@example.org")
    git("add", "-A")
    git("commit", "--quiet", "--no-verify", "--message", "Declare the steps in a Snakefile")

    # Declare the same steps as DVC stages. The data stays in Git, for step 1 to move.
    BUCKET.mkdir()
    run("dvc", "init", "--quiet")
    run("dvc", "config", "core.analytics", "false")
    run("dvc", "remote", "add", "--default", "storage", "../osn-bucket")
    # DVC reads a relative path from old commits as relative to /, so dvc push --all-commits needs the full path.
    run("dvc", "remote", "modify", "--local", "storage", "url", str(BUCKET))
    stage("clean", ["data/penguins.csv", "clean.py"], ["-o", "results/clean.csv"], "clean.py")
    stage("validate", ["results/clean.csv", "validate.py"], ["-o", "results/validated.csv"], "validate.py")
    stage("report", ["results/validated.csv", "report.py"], ["-p", "report", "-M", "metrics.json"], "report.py")
    run("dvc", "repro", "--quiet")
    git("add", ".")
    git("commit", "--quiet", "--no-verify", "--message", "Declare the same steps as DVC stages")


def main():
    if "--reset" in sys.argv:
        shutil.rmtree(PROJECT, ignore_errors=True)
        shutil.rmtree(BUCKET, ignore_errors=True)
    if PROJECT.exists():
        print("project/ already exists, so I left your work alone. To start over: python scripts/setup_project.py --reset")
        return
    build()
    print("Built project/ with the 2007 field season and its DVC pipeline, and osn-bucket/ as a stand-in for object storage. Now run: cd project")


main()
