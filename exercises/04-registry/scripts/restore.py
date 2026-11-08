#!/usr/bin/env python3
"""Restore each registered model into a separate empty folder, without the author's cache."""
import subprocess
import sys
import tempfile
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1] / "project"
BUCKET = PROJECT.parent / "osn-bucket"


def run(*args, cwd):
    return subprocess.run(args, cwd=cwd, capture_output=True, text=True, check=True)


def restore(tag, folder):
    clone = folder / "clone"
    run("git", "clone", "--quiet", "--no-hardlinks", str(PROJECT), str(clone), cwd=folder)
    run("git", "checkout", "--quiet", tag, cwd=clone)
    # A clone has no local config, so give it the bucket's full path.
    run("dvc", "remote", "modify", "--local", "storage", "url", str(BUCKET), cwd=clone)
    run("dvc", "pull", cwd=clone)
    if not (clone / "model.pkl").is_file():
        raise FileNotFoundError("model.pkl was not restored")
    return clone


def main():
    tags = run("git", "tag", "--list", "penguin-sex-clf@*", cwd=PROJECT).stdout.split()
    if not tags:
        print("FAIL  No versions are registered. Use gto register first.")
        return 1
    failed = 0
    for tag in tags:
        try:
            with tempfile.TemporaryDirectory() as tmp:
                restore(tag, Path(tmp))
            print(f"{tag}: restored into an empty folder")
        except (subprocess.CalledProcessError, FileNotFoundError) as error:
            failed += 1
            print(f"{tag}: FAILED. Check the tag and run dvc push --all-tags. {error}")
    return int(bool(failed))


if __name__ == "__main__":
    sys.exit(main())
