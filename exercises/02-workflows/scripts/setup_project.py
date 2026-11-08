#!/usr/bin/env python3
"""Build the starter repository in project/: the 2007 penguins, three scripts run by hand, and a correct metrics.json, in one commit.

The date is fixed, so everyone gets the same commit ID.
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
ENV = {**os.environ, "GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_NOSYSTEM": "1"}
STAMP = "2025-02-03T10:00:00+0000"


def run(*args, env=ENV):
    subprocess.run(args, cwd=PROJECT, env=env, check=True, capture_output=True)


def build():
    shutil.copytree(FILES, PROJECT)
    shutil.copytree(HERE / ".exercise" / "data", PROJECT / "data", ignore=shutil.ignore_patterns("SOURCE.md"))
    run("git", "init", "--quiet", "--initial-branch=main")
    run("git", "config", "core.autocrlf", "false")
    run("git", "config", "user.name", "Workshop Learner")
    run("git", "config", "user.email", "learner@example.org")
    # The README's procedure, run in full, so the committed number is current.
    for script in ("clean.py", "validate.py", "report.py"):
        run(sys.executable, script)
    run("git", "add", "-A")
    run("git", "commit", "--quiet", "--no-verify", "--message", "Add the 2007 penguins, the three scripts and the result",
        env={**ENV, "GIT_AUTHOR_DATE": STAMP, "GIT_COMMITTER_DATE": STAMP})


def main():
    if "--reset" in sys.argv:
        shutil.rmtree(PROJECT, ignore_errors=True)
    if PROJECT.exists():
        print("project/ already exists, so I left your work alone. To start over: python scripts/setup_project.py --reset")
        return
    build()
    print("Built project/ with the 2007 penguins, three scripts and one commit. Now run: cd project")


main()
