#!/usr/bin/env python3
"""Build the group's starting repository in project/: the 2007 field season, tracked by DVC, with its pipeline.

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


def run(*args):
    subprocess.run(args, cwd=PROJECT, env=ENV, check=True, capture_output=True)


def git(*args):
    run("git", *args)


def stage(name, inputs, outputs, script):
    flags = [flag for path in inputs for flag in ("-d", path)] + list(outputs)
    run("dvc", "stage", "add", "--quiet", "-n", name, *flags, "python", script)


def build():
    shutil.copytree(FILES, PROJECT)
    git("init", "--quiet", "--initial-branch=main")
    git("config", "core.autocrlf", "false")
    git("config", "user.name", "Workshop Learner")
    git("config", "user.email", "learner@example.org")
    git("add", "-A")
    git("commit", "--quiet", "--no-verify", "--message", "Add the analysis scripts and cleaning policy")

    # The first season is the 2007 rows of the full table, byte for byte.
    lines = (HERE / ".exercise" / "data" / "penguins.csv").read_text().splitlines(keepends=True)
    season = [lines[0]] + [line for line in lines[1:] if line.strip().endswith(",2007")]
    (PROJECT / "data").mkdir()
    (PROJECT / "data" / "penguins.csv").write_text("".join(season))
    (PROJECT / "results").mkdir()
    BUCKET.mkdir()

    run("dvc", "init", "--quiet")
    run("dvc", "config", "core.analytics", "false")
    run("dvc", "remote", "add", "--default", "storage", str(BUCKET))
    run("dvc", "add", "--quiet", "data/penguins.csv")
    stage("clean", ["data/penguins.csv", "clean.py"], ["-o", "results/clean.csv"], "clean.py")
    stage("validate", ["results/clean.csv", "validate.py"], ["-o", "results/validated.csv"], "validate.py")
    stage("report", ["results/validated.csv", "report.py"], ["-M", "metrics.json", "-o", "results/report.md"], "report.py")
    run("dvc", "repro", "--quiet")
    git("add", ".")
    git("commit", "--quiet", "--no-verify", "--message", "Track the 2007 season and the pipeline")
    run("dvc", "push", "--quiet")


def main():
    if "--reset" in sys.argv:
        shutil.rmtree(PROJECT, ignore_errors=True)
        shutil.rmtree(BUCKET, ignore_errors=True)
    if PROJECT.exists():
        print("project/ already exists, so I left your work alone. To start over: python scripts/setup_project.py --reset")
        return
    build()
    print("Built project/ with the 2007 field season and its pipeline, and osn-bucket/ as a stand-in for object storage. Now run: cd project")


main()
