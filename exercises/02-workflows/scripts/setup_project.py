#!/usr/bin/env python3
"""Build the starting repository in project/: the 2024 catalog, three scripts run by hand, and a stale result.

The dates are fixed, so everyone gets the same commit IDs.
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


def run(*args, env=ENV):
    subprocess.run(args, cwd=PROJECT, env=env, check=True, capture_output=True)


def commit(day, message):
    stamp = f"2025-02-{day:02d}T10:00:00+0000"
    run("git", "add", "-A")
    run("git", "commit", "--quiet", "--no-verify", "--message", message,
        env={**ENV, "GIT_AUTHOR_DATE": stamp, "GIT_COMMITTER_DATE": stamp})


def build():
    shutil.copytree(FILES, PROJECT)
    shutil.copytree(HERE / ".exercise" / "data", PROJECT / "data", ignore=shutil.ignore_patterns("SOURCE.md"))
    run("git", "init", "--quiet", "--initial-branch=main")
    run("git", "config", "core.autocrlf", "false")
    run("git", "config", "user.name", "Workshop Learner")
    run("git", "config", "user.email", "learner@example.org")

    # The README's procedure, run in full, on the whole catalog.
    for script in ("subset.py", "count.py", "fit.py"):
        run(sys.executable, script)
    commit(3, "Add the 2024 catalog, the three scripts and the first fit")

    # Then the depth limit changed, and only the last step reran. Its output is stale, and nothing says so.
    params = PROJECT / "params.yaml"
    params.write_text(params.read_text().replace("max_depth_km: 700", "max_depth_km: 70"))
    run(sys.executable, "fit.py")
    commit(10, "Keep only shallow earthquakes, 70 km or less. Reran the fit, and the b-value doesn't change")


def main():
    if "--reset" in sys.argv:
        shutil.rmtree(PROJECT, ignore_errors=True)
    if PROJECT.exists():
        print("project/ already exists, so I left your work alone. To start over: python scripts/setup_project.py --reset")
        return
    build()
    print("Built project/ with the 2024 catalog, three scripts and two commits. Now run: cd project")


main()
