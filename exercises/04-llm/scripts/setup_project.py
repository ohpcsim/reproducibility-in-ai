#!/usr/bin/env python3
"""Build project/: the frozen exercise 3 files, the recorded runs, and starter tests.

Run it again and it leaves your work alone. To start over, use --reset. That deletes your work.
"""
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
PROJECT = HERE / "project"


def git(*args):
    subprocess.run(["git", *args], cwd=PROJECT, check=True, capture_output=True)


def main():
    if "--reset" in sys.argv:
        shutil.rmtree(PROJECT, ignore_errors=True)
    if PROJECT.exists():
        print("project/ already exists, so I left your work alone. To start over: python scripts/setup_project.py --reset")
        return
    shutil.copytree(HERE / ".exercise" / "project", PROJECT)
    git("init", "--quiet", "--initial-branch=main")
    for key, value in (("core.autocrlf", "false"), ("commit.gpgsign", "false"),
                       ("user.name", "Workshop Learner"), ("user.email", "learner@example.org")):
        git("config", key, value)
    git("add", "-A")
    git("commit", "--quiet", "--no-verify", "--message", "Add the frozen classifier, the recorded runs and starter tests")
    print("Built project/ with the frozen classifier and the recorded runs. Now run: cd project")


main()
