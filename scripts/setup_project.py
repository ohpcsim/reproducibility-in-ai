#!/usr/bin/env python3
"""Build an unregistered penguin model. Re-running preserves work; --reset deletes it."""
import os
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
PROJECT = HERE / "project"
BUCKET = HERE / "osn-bucket"
ENV = {**os.environ, "GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_NOSYSTEM": "1"}


def run(*args):
    subprocess.run(args, cwd=PROJECT, env=ENV, check=True, capture_output=True)


def build():
    shutil.copytree(HERE / ".exercise" / "project", PROJECT)
    (PROJECT / "data").mkdir()
    shutil.copyfile(HERE / ".exercise" / "data" / "penguins.csv", PROJECT / "data" / "penguins.csv")
    run("git", "init", "--quiet", "--initial-branch=main")
    for key, value in (("core.autocrlf", "false"), ("commit.gpgsign", "false"), ("tag.gpgsign", "false"),
                       ("user.name", "Workshop Learner"), ("user.email", "learner@example.org")):
        run("git", "config", key, value)
    BUCKET.mkdir()
    run("dvc", "init", "--quiet")
    run("dvc", "config", "core.analytics", "false")
    # Old tags and fresh clones must resolve the same stand-in bucket.
    run("dvc", "remote", "add", "--default", "storage", str(BUCKET))
    run("dvc", "add", "--quiet", "data/penguins.csv")
    run("dvc", "repro", "--quiet")
    run("git", "add", ".")
    run("git", "commit", "--quiet", "--no-verify", "--message", "Train the penguin sex classifier with C=0.01")
    run("dvc", "push", "--quiet")


def main():
    if "--reset" in sys.argv:
        shutil.rmtree(PROJECT, ignore_errors=True)
        shutil.rmtree(BUCKET, ignore_errors=True)
    if PROJECT.exists():
        print("project/ already exists, so I left your work alone. To start over: python scripts/setup_project.py --reset")
        return
    build()
    print("Built project/ with the published penguins and an unregistered model, and osn-bucket/ as a stand-in for object storage. Now run: cd project")


if __name__ == "__main__":
    main()
