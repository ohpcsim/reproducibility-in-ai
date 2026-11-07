#!/usr/bin/env python3
"""Build the group's repository in project/: the first release in prod, and a teammate's branch that asks for promotion.

Run it again and it leaves your work alone. To start over, use --reset. That deletes your work.
"""
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
FILES = HERE / ".exercise" / "project"
PROJECT = HERE / "project"
BUCKET = HERE / "osn-bucket"

REQUEST = """# Please promote candidate-v2

Validation accuracy is 1.000, up from what we have in prod. I also gave the
training step more data, which always helps. Can you register this and move it
to prod before the review?

Sam
"""


def run(*args):
    subprocess.run(args, cwd=PROJECT, check=True, capture_output=True)


def git(*args):
    run("git", *args)


def commit(message, author=None):
    identity = ["-c", f"user.name={author[0]}", "-c", f"user.email={author[1]}"] if author else []
    git("add", "-A")
    git(*identity, "commit", "--quiet", "--no-verify", "--message", message)


def build():
    shutil.copytree(FILES, PROJECT)
    git("init", "--quiet", "--initial-branch=main")
    for key, value in (("core.autocrlf", "false"), ("commit.gpgsign", "false"), ("tag.gpgsign", "false"),
                       ("user.name", "Workshop Learner"), ("user.email", "learner@example.org")):
        git("config", key, value)
    BUCKET.mkdir()
    run("dvc", "init", "--quiet")
    run("dvc", "config", "core.analytics", "false")
    # An absolute path, because DVC can't resolve a relative one when it reads an old tag's config.
    run("dvc", "remote", "add", "--default", "storage", str(BUCKET))
    commit("Add the digit classifier, its pipeline and its registry entry")

    # The teammate's branch: more hidden units, and every row in the training set.
    git("checkout", "--quiet", "-b", "candidate-v2")
    split = PROJECT / "split.py"
    split.write_text(re.sub(r'"train": sorted\(order\[:first\]\)', '"train": sorted(order)', split.read_text()))
    params = PROJECT / "params.yaml"
    params.write_text(params.read_text().replace("hidden: 32", "hidden: 64"))
    (PROJECT / "PROMOTION_REQUEST.md").write_text(REQUEST)
    run("dvc", "repro", "--quiet")
    commit("Use more data and a wider network", author=("Sam Okafor", "sam@example.org"))
    git("checkout", "--quiet", "main")
    (PROJECT / "model.pkl").unlink()

    # The first release. Nobody ran dvc push for it, and the exercise's step 3 is about that.
    run("dvc", "repro", "--quiet")
    commit("Train with 32 hidden units")
    run("gto", "register", "digits-clf", "--version", "v1.0.0")
    run("gto", "assign", "digits-clf", "--version", "v1.0.0", "--stage", "prod")


def main():
    if "--reset" in sys.argv:
        shutil.rmtree(PROJECT, ignore_errors=True)
        shutil.rmtree(BUCKET, ignore_errors=True)
    if PROJECT.exists():
        print("project/ already exists, so I left your work alone. To start over: python scripts/setup_project.py --reset")
        return
    build()
    print("Built project/ with release v1.0.0 in prod and Sam's candidate-v2 branch, and osn-bucket/ as a stand-in for object storage. Now run: cd project")


main()
