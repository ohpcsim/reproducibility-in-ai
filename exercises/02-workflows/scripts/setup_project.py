#!/usr/bin/env python3
"""Build the starter repository in project/: the 2007 penguins, the scripts and a working Snakefile, in one commit.

Built outputs are not in Git. The workflow builds them.
--nextflow builds the same project with main.nf and nextflow.config instead of the Snakefile, for the Nextflow page.
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
NEXTFLOW = "--nextflow" in sys.argv
ENV = {**os.environ, "GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_NOSYSTEM": "1"}
STAMP = "2025-02-03T10:00:00+0000"


def run(*args, env=ENV):
    subprocess.run(args, cwd=PROJECT, env=env, check=True, capture_output=True)


def build():
    shutil.copytree(FILES, PROJECT, ignore=shutil.ignore_patterns("Snakefile", "profiles") if NEXTFLOW else None)
    shutil.copytree(HERE / ".exercise" / "data", PROJECT / "data", ignore=shutil.ignore_patterns("SOURCE.md"))
    if NEXTFLOW:
        for name in ("main.nf", "nextflow.config"):
            shutil.copyfile(HERE / "nextflow" / name, PROJECT / name)
        with open(PROJECT / ".gitignore", "a") as ignore:
            ignore.write("work/\n.nextflow/\n.nextflow.log*\n")
        readme = PROJECT / "README.md"
        readme.write_text(readme.read_text().replace("snakemake --cores 1", "nextflow run main.nf"))
    run("git", "init", "--quiet", "--initial-branch=main")
    run("git", "config", "core.autocrlf", "false")
    run("git", "config", "user.name", "Workshop Learner")
    run("git", "config", "user.email", "learner@example.org")
    run("git", "add", "-A")
    run("git", "commit", "--quiet", "--no-verify", "--message",
        f"Add the 2007 penguins, the scripts and the workflow in {'main.nf' if NEXTFLOW else 'a Snakefile'}",
        env={**ENV, "GIT_AUTHOR_DATE": STAMP, "GIT_COMMITTER_DATE": STAMP})


def main():
    if "--reset" in sys.argv:
        shutil.rmtree(PROJECT, ignore_errors=True)
    if PROJECT.exists():
        print("project/ already exists, so I left your work alone. To start over: python scripts/setup_project.py --reset")
        return
    build()
    print(f"Built project/ with the 2007 penguins, the scripts and a working {'main.nf' if NEXTFLOW else 'Snakefile'}, "
          "in one commit. Now run: cd project")


main()
