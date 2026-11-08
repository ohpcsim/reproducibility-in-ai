#!/usr/bin/env python3
"""Build the starter repository in project/: one commit, with environment.yml and pyproject.toml.

The date and author are fixed, so everyone gets the same commit ID.
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
STAMP = "2025-03-03T10:00:00+0000"
AUTHOR = {"GIT_AUTHOR_NAME": "Priya Rao", "GIT_AUTHOR_EMAIL": "priya@example.org", "GIT_AUTHOR_DATE": STAMP,
          "GIT_COMMITTER_NAME": "Priya Rao", "GIT_COMMITTER_EMAIL": "priya@example.org", "GIT_COMMITTER_DATE": STAMP}


def git(*args, env=ENV):
    subprocess.run(["git", *args], cwd=PROJECT, env=env, check=True, capture_output=True)


def build():
    shutil.copytree(FILES, PROJECT)
    shutil.copytree(HERE / ".exercise" / "data", PROJECT / "data", ignore=shutil.ignore_patterns("SOURCE.md"))
    git("init", "--quiet", "--initial-branch=main")
    git("config", "core.autocrlf", "false")
    git("add", "-A")
    git("commit", "--quiet", "--no-verify", "--message", "Add the penguin analysis", env={**ENV, **AUTHOR})
    git("config", "user.name", "Workshop Learner")
    git("config", "user.email", "learner@example.org")


def main():
    if "--reset" in sys.argv:
        shutil.rmtree(PROJECT, ignore_errors=True)
        shutil.rmtree(HERE / "envs", ignore_errors=True)
    if PROJECT.exists():
        print("project/ already exists, so I left your work alone. To start over: python scripts/setup_project.py --reset")
        return
    build()
    print("Built project/ with one commit. Now run: cd project")


main()
