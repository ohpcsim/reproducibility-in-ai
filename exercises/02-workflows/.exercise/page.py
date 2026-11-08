"""Record what the documented commands print, for the notebook's stored output and the site.

Nobody has to run this. It works in a scratch copy, so it can't touch your project.
"""
import atexit
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
LEARNER_FOLDERS = {"project", "remote", "envs", "osn-bucket", ".git", ".ipynb_checkpoints", "_build"}

scratch = Path(tempfile.mkdtemp())
atexit.register(shutil.rmtree, scratch, ignore_errors=True)
root = scratch / "exercise"
shutil.copytree(HERE, root, ignore=lambda folder, names: LEARNER_FOLDERS & set(names) if folder == str(HERE) else ())
environment = {name: value for name, value in os.environ.items() if name != "FORCE_COLOR"}
environment["PY_COLORS"] = "0"
subprocess.run([sys.executable, "scripts/setup_project.py"], cwd=root, env=environment, check=True, capture_output=True)


def run(*commands):
    """Run the commands in the scratch project, and print them the way a terminal would."""
    text = []
    for command in commands:
        done = subprocess.run(["bash", "-c", command], cwd=root / "project", env=environment,
                              stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        text.append(f"$ {command}\n{done.stdout}")
    print("\n".join(text).replace(str(root), "~"), end="")


def reset():
    """Put the scratch project back to its last commit, so a check records what it prints on a fresh starter."""
    subprocess.run(["bash", "-c", "git checkout -- . && git clean -fdq"], cwd=root / "project", env=environment, check=True)
