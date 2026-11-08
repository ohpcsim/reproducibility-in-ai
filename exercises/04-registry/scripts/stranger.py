#!/usr/bin/env python3
"""Clone the project into an empty folder and try to restore every registered version by tag."""
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
PROJECT = HERE / "project"


def run(*args, cwd):
    return subprocess.run(args, cwd=cwd, capture_output=True, text=True)


tags = run("git", "tag", "--list", "digits-clf@*", cwd=PROJECT).stdout.split()
if not tags:
    sys.exit("No versions are registered yet.")

failed = 0
with tempfile.TemporaryDirectory() as tmp:
    clone = Path(tmp) / "clone"
    run("git", "clone", "--quiet", str(PROJECT), str(clone), cwd=tmp)
    run("dvc", "remote", "modify", "--local", "storage", "url", str(HERE / "osn-bucket"), cwd=clone)
    for tag in tags:
        run("git", "checkout", "--quiet", tag, cwd=clone)
        (clone / "model.pkl").unlink(missing_ok=True)
        pulled = run("dvc", "pull", cwd=clone)
        if pulled.returncode == 0 and (clone / "model.pkl").exists():
            print(f"{tag}: restored into an empty folder")
        else:
            failed += 1
            print(f"{tag}: FAILED. Its model isn't in the bucket, so a clean clone can't restore it.")
sys.exit(1 if failed else 0)
