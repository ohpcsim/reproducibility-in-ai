#!/usr/bin/env python3
"""Check your work. Each part prints PASS or FAIL with what to do next.

Run it from project/: python ../check.py
It reads your last commit, in a throwaway clone, and builds an environment from each lock.
--short is accepted and checks the same parts: this exercise is all short path.
"""
import os
import platform
import re
import shutil
import subprocess
import sys
import tempfile
import tomllib
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJECT = HERE / "project"
# conda's name for this platform, the same as `conda config --show subdir`.
SUBDIR = {("linux", "x86_64"): "linux-64", ("linux", "aarch64"): "linux-aarch64",
          ("darwin", "arm64"): "osx-arm64", ("darwin", "x86_64"): "osx-64"}.get((sys.platform, platform.machine()), "unknown")
LOCK = f"explicit-{SUBDIR}.txt"
TOOL_ENV = {k: v for k, v in os.environ.items() if k not in ("VIRTUAL_ENV", "UV_PROJECT_ENVIRONMENT")}

results = []


def mark(ok):
    word, color = ("PASS", 32) if ok else ("FAIL", 31)
    return f"\033[{color}m{word}\033[0m" if sys.stdout.isatty() or os.environ.get("CLICOLOR_FORCE") else word


def report(ok, message, *hints):
    results.append(ok)
    print(f"{mark(ok)}  {message}")
    for hint in hints:
        print(f"      {hint}")
    return ok


def run(*args, cwd):
    return subprocess.run(args, cwd=cwd, env=TOOL_ENV, capture_output=True, text=True)


def committed(clone, name):
    path = clone / name
    return path.read_text() if path.is_file() else None


def pandas_line(text):
    """The text after '- pandas' in a conda file, without comments, or None if pandas isn't listed."""
    found = re.search(r"^\s*-\s*pandas\b([^#\n]*)", text or "", re.M)
    return found and found.group(1).strip()


def uv_dependencies(text):
    return {re.split(r"[<>=!~\[; @]", name, maxsplit=1)[0].strip().lower()
            for name in tomllib.loads(text)["project"].get("dependencies", [])}


def check_conda_declared(clone):
    text = committed(clone, "environment.yml")
    rest = pandas_line(text)
    if rest is None:
        hints = []
        if pandas_line((PROJECT / "environment.yml").read_text()) is not None:
            hints.append("You added it in project/, but didn't commit it. Run: git add environment.yml, then git commit.")
        elif pandas_line((HERE / ".binder" / "environment.yml").read_text()) is not None:
            hints.append("You added it to .binder/environment.yml, the session's file. Take it out and edit environment.yml in project/.")
        return report(False, "The committed environment.yml doesn't declare pandas. Add it as '  - pandas', with no version. Step 1.", *hints)
    if rest:
        return report(False, f"environment.yml pins pandas ({rest.strip()}). Leave the version out. The lock records it.")
    return report(True, "environment.yml declares pandas, with no version")


def check_conda_lock(clone):
    text = committed(clone, LOCK)
    if text is None:
        others = sorted(p.name for p in clone.glob("explicit-*.txt"))
        hints = [f"{', '.join(others)} is committed, but this machine is {SUBDIR}. Each platform needs its own lock."] if others else []
        if not others and (PROJECT / LOCK).exists():
            hints.append(f"{LOCK} is in project/ but not committed. Run: git add {LOCK}, then git commit.")
        return report(False, f"No {LOCK} is committed. Write it with conda list --explicit --md5, and commit it. Step 1.", *hints)
    if not re.search(r"^https?://\S+/pandas-[^/\s]+\.(conda|tar\.bz2)", text, re.M):
        return report(False, f"{LOCK} doesn't list pandas. Build the environment from environment.yml again, write the lock again and commit it.")
    return report(True, f"{LOCK} is committed and lists pandas")


def check_conda_rebuild(clone, lock_ok):
    if not lock_ok:
        return report(False, f"Not tested: an environment built from {LOCK} runs analyze.py. Fix the lock first.")
    conda = os.environ.get("CONDA_EXE") or shutil.which("conda")
    if not conda:
        return report(False, "conda isn't on your PATH, so I can't build from the lock. Run conda activate repro-environments.")
    env = clone.parent / "conda-env"
    built = run(conda, "create", "--yes", "--quiet", "--prefix", str(env), "--file", LOCK, cwd=clone)
    if built.returncode != 0:
        return report(False, f"conda create --file {LOCK} failed. Run it yourself to read the error.")
    ok = run(str(env / "bin" / "python"), "analyze.py", cwd=clone).returncode == 0
    return report(ok, f"An environment built from {LOCK} runs analyze.py" if ok else
                  f"An environment built from {LOCK} can't run analyze.py. Run analyze.py in ../envs/conda-lock and read the error.")


def check_uv_declared(clone):
    text = committed(clone, "pyproject.toml")
    try:
        declared = "pandas" in uv_dependencies(text or "")
    except (tomllib.TOMLDecodeError, KeyError):
        return report(False, "The committed pyproject.toml isn't valid. Repair it and commit it.")
    if declared:
        return report(True, "pyproject.toml declares pandas")
    hints = []
    try:
        if "pandas" in uv_dependencies((PROJECT / "pyproject.toml").read_text()):
            hints.append("You added it in project/, but didn't commit it. Run: git add pyproject.toml uv.lock, then git commit.")
    except (tomllib.TOMLDecodeError, KeyError, FileNotFoundError):
        pass
    return report(False, "The committed pyproject.toml doesn't declare pandas. Run uv add pandas. Step 2.", *hints)


def check_uv_lock(clone, uv):
    if committed(clone, "uv.lock") is None:
        hint = ["uv.lock is in project/ but not committed. Run: git add uv.lock, then git commit."] if (PROJECT / "uv.lock").exists() else []
        return report(False, "No uv.lock is committed. uv add writes it. Commit it with pyproject.toml. Step 2.", *hint)
    if not uv:
        return report(False, "uv isn't on your PATH. Run conda activate repro-environments, which includes it.")
    ok = run(uv, "lock", "--check", cwd=clone).returncode == 0
    return report(ok, "uv.lock is committed and matches pyproject.toml" if ok else
                  "The committed uv.lock doesn't match pyproject.toml. Run uv lock, then commit pyproject.toml and uv.lock.")


def check_uv_rebuild(clone, uv, lock_ok):
    if not lock_ok:
        return report(False, "Not tested: uv sync --locked builds an environment that runs analyze.py. Fix uv.lock first.")
    if run(uv, "sync", "--locked", "--quiet", cwd=clone).returncode != 0:
        return report(False, "uv sync --locked failed in a clean clone. Run it yourself to read the error.")
    ok = run(uv, "run", "python", "analyze.py", cwd=clone).returncode == 0
    return report(ok, "uv sync --locked builds an environment that runs analyze.py" if ok else
                  "After uv sync --locked, uv run python analyze.py failed. Run it yourself to read the error.")


def main():
    if not (PROJECT / ".git").exists():
        print("FAIL  project/ is not there. From the folder above it, run: python scripts/setup_project.py")
        return 1
    uv = shutil.which("uv")
    with tempfile.TemporaryDirectory() as tmp:
        clone = Path(tmp) / "clone"
        subprocess.run(["git", "clone", "--quiet", str(PROJECT), str(clone)], check=True, capture_output=True)
        print("Step 1, conda:")
        conda = [check_conda_declared(clone)]
        conda.append(check_conda_lock(clone))
        conda.append(check_conda_rebuild(clone, conda[-1]))
        print("Step 2, uv:")
        uv_parts = [check_uv_declared(clone)]
        uv_parts.append(check_uv_lock(clone, uv))
        uv_parts.append(check_uv_rebuild(clone, uv, uv_parts[-1]))
    print(f"\n{sum(results)} of {len(results)} parts pass.")
    if all(results):
        print(f"Both routes pass. Your conda lock rebuilds on {SUBDIR}. Your uv lock rebuilds on Linux, macOS and Windows.")
        return 0
    if all(conda):
        print("The conda route passes. Step 2, the uv route, is left.")
    elif all(uv_parts):
        print("The uv route passes. Step 1, the conda route, is left.")
    return 1


sys.exit(main())
