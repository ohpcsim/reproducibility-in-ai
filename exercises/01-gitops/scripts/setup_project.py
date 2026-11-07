#!/usr/bin/env python3
"""Build the group's repository: six commits of history in project/, and a stand-in for GitHub in remote/.

The dates and authors are fixed, so everyone gets the same commit IDs.
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
REMOTE = HERE / "remote" / "co2.git"

ENV = {**os.environ, "GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_NOSYSTEM": "1"}


def git(*args, cwd=PROJECT, env=None):
    subprocess.run(["git", *args], cwd=cwd, env=env or ENV, check=True, capture_output=True)


def write(name, text):
    path = PROJECT / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def copy(name):
    target = PROJECT / name
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(FILES / name, target)


def params(start, degree, comments=False):
    if comments:
        return f"# Years to fit, inclusive.\nstart_year: {start}\nend_year: 2024\n\n# Polynomial degree of the trend.\ndegree: {degree}\n"
    return f"start_year: {start}\nend_year: 2024\ndegree: {degree}\n"


def metrics(growth, rmse, amplitude):
    return (
        '{\n'
        f'  "growth_rate_ppm_per_year": {growth},\n'
        f'  "rmse_ppm": {rmse},\n'
        f'  "seasonal_amplitude_ppm": {amplitude}\n'
        '}\n'
    )


def commit(day, author, email, message):
    stamp = f"2025-03-{day:02d}T10:00:00+0000"
    env = {**ENV, "GIT_AUTHOR_NAME": author, "GIT_AUTHOR_EMAIL": email, "GIT_AUTHOR_DATE": stamp,
           "GIT_COMMITTER_NAME": author, "GIT_COMMITTER_EMAIL": email, "GIT_COMMITTER_DATE": stamp}
    git("add", "-A")
    git("commit", "--quiet", "--no-verify", "--message", message, env=env)


FIRST_ANALYZE = '''"""Fit the trend and write the numbers the group publishes to metrics.json."""
import json

import yaml

import trend

params = yaml.safe_load(open("params.yaml"))
t, ppm = trend.load_table(open("data/co2_mm_mlo.csv", "rb").read())
metrics = trend.summarize(t, ppm, params)

with open("metrics.json", "w") as out:
    json.dump(metrics, out, indent=2)
    out.write("\\n")
print(json.dumps(metrics, indent=2))
'''

FIRST_README = "# Mauna Loa CO2 growth rate\n\nRun `python analyze.py`. It writes `metrics.json`.\n"


def build():
    PROJECT.mkdir()
    git("init", "--quiet", "--initial-branch=main")
    git("config", "core.autocrlf", "false")

    shutil.copytree(HERE / ".exercise" / "data", PROJECT / "data", ignore=shutil.ignore_patterns("SOURCE.md"))
    for name in ("trend.py", "check_fresh.py", "environment.yml", "hooks/pre-commit"):
        copy(name)
    write("analyze.py", FIRST_ANALYZE)
    write("README.md", FIRST_README)
    write("params.yaml", params(1990, 2))
    write("metrics.json", metrics(2.712, 0.547, 6.63))
    write(".gitignore", "__pycache__/\n.pytest_cache/\n")
    commit(3, "Priya Rao", "priya@example.org", "Add the Mauna Loa data and a first trend fit")

    write("params.yaml", params(2000, 2))
    write("metrics.json", metrics(2.681, 0.473, 6.625))
    commit(5, "Priya Rao", "priya@example.org", "Start the fit at 2000, and rerun")

    copy("test_trend.py")
    copy("holdout.py")
    commit(10, "Sam Okafor", "sam@example.org", "Add a test of the fit and a holdout comparison")

    write("params.yaml", params(2000, 3, comments=True))
    commit(12, "Lee Tran", "lee@example.org", "Tidy params.yaml")

    copy("analyze.py")
    commit(17, "Lee Tran", "lee@example.org", "Read the CSV with pandas")

    copy("README.md")
    commit(20, "Sam Okafor", "sam@example.org", "Describe the project in the README")

    git("config", "user.name", "Workshop Learner")
    git("config", "user.email", "learner@example.org")
    REMOTE.parent.mkdir()
    git("init", "--quiet", "--bare", "--initial-branch=main", str(REMOTE), cwd=HERE)
    git("remote", "add", "origin", str(REMOTE))
    git("push", "--quiet", "--set-upstream", "origin", "main")


def main():
    if "--reset" in sys.argv:
        shutil.rmtree(PROJECT, ignore_errors=True)
        shutil.rmtree(REMOTE.parent, ignore_errors=True)
        shutil.rmtree(HERE / "envs", ignore_errors=True)
    if REMOTE.exists():
        print("The repository already exists, so I left your work alone. To start over: python scripts/setup_project.py --reset")
        return
    build()
    print("Built project/ with six commits, and remote/co2.git as a stand-in for GitHub. Now run: cd project")


main()
