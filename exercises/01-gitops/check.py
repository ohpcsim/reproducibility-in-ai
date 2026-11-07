#!/usr/bin/env python3
"""Check your work. Each part prints PASS or FAIL with what to do next. It reads what you committed.

Run it from project/:
python ../check.py --short   checks step 1, the short path.
python ../check.py           checks everything.
"""
import ast
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJECT = HERE / "project"
REMOTE = HERE / "remote" / "co2.git"
ENV = HERE / "envs" / "co2"
PACKAGE_FOR_IMPORT = {"yaml": "pyyaml"}

# The digest lets this script recognize the right growth rate without containing it.
SALT = "mauna-loa-exercise-1:"
GROWTH_DIGEST = "e3de544612819db8542e147a809c2fb7f876814d049aafb1ba69e38b297f4ea3"

results = []


def mark(ok):
    word, color = ("PASS", 32) if ok else ("FAIL", 31)
    return f"\033[{color}m{word}\033[0m" if sys.stdout.isatty() or os.environ.get("CLICOLOR_FORCE") else word


def report(ok, message):
    results.append(ok)
    print(f"{mark(ok)}  {message}")


def run(*args, cwd=PROJECT, env=None):
    return subprocess.run(args, cwd=cwd, env=env, capture_output=True, text=True)


def git(*args, cwd=PROJECT):
    return run("git", *args, cwd=cwd)


def good_growth(value):
    return hashlib.sha256(f"{SALT}{value:.3f}".encode()).hexdigest() == GROWTH_DIGEST


def package_names(lock_text):
    return {m.group(1) for m in re.finditer(r"/([^/\s]+)-[^-/\s]+-[^-/\s]+\.(?:conda|tar\.bz2)", lock_text)}


def imported_packages(tracked):
    """Third-party packages the committed Python files import."""
    local = {Path(name).stem for name in tracked if name.endswith(".py")}
    found = {}
    for name in tracked:
        if not name.endswith(".py"):
            continue
        for node in ast.walk(ast.parse(git("show", f"HEAD:{name}").stdout)):
            modules = []
            if isinstance(node, ast.Import):
                modules = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom) and node.module:
                modules = [node.module]
            for module in modules:
                top = module.split(".")[0]
                if top not in sys.stdlib_module_names and top not in local:
                    found.setdefault(PACKAGE_FOR_IMPORT.get(top, top), name)
    return found


def explain_undeclared(package):
    """Say which easy mistake this is: the wrong file, an unsaved edit, or a missing commit."""
    edited = (PROJECT / "environment.yml").read_text()
    session = (HERE / ".binder" / "environment.yml").read_text()
    if re.search(rf"^\s*-\s*{package}\b", edited, re.M):
        print(f"      You added {package} to environment.yml in project/, but it isn't committed. Run: git add environment.yml, then git commit.")
    elif re.search(rf"^\s*-\s*{package}\b", session, re.M):
        print(f"      You added {package} to .binder/environment.yml, which is the session's file. Take it out and edit environment.yml in project/.")
    elif ENV.exists():
        print(f"      envs/co2 was built from a file without {package}. Edit environment.yml in project/ and confirm with git diff environment.yml.")
        print("      Then delete the old environment with: rm -rf ../envs/co2")


def check_declared():
    tracked = git("ls-tree", "-r", "--name-only", "HEAD").stdout.split()
    packages = imported_packages(tracked)
    declared = set(re.findall(r"^\s*-\s*([A-Za-z0-9_.-]+)", git("show", "HEAD:environment.yml").stdout, re.M))
    missing = {p: f for p, f in packages.items() if p not in declared}
    report(not missing, "environment.yml declares every import" if not missing else
           "; ".join(f"{f} imports {p}, and the committed environment.yml does not declare it" for p, f in missing.items()))
    for package in missing:
        explain_undeclared(package)

    locks = [name for name in tracked if re.fullmatch(r"explicit-[\w-]+\.txt", name)]
    if not locks:
        report(False, "No lock file is committed. Write one with conda list --explicit --md5 and commit it.")
        return
    for lock in locks:
        absent = set(packages) - package_names(git("show", f"HEAD:{lock}").stdout)
        report(not absent, f"{lock} holds every import" if not absent else
               f"{lock} is missing {', '.join(sorted(absent))}. Rebuild the environment, write the lock again, commit it.")


def rerun_growth(clone, python=sys.executable):
    code = ("import json, trend, yaml\n"
            "t, ppm = trend.load_table(open('data/co2_mm_mlo.csv', 'rb').read())\n"
            "print(trend.summarize(t, ppm, yaml.safe_load(open('params.yaml')))['growth_rate_ppm_per_year'])\n")
    result = run(python, "-c", code, cwd=clone)
    return float(result.stdout) if result.returncode == 0 else None


def check_number(clone):
    fresh = run(sys.executable, "check_fresh.py", cwd=clone)
    report(fresh.returncode == 0, "metrics.json matches a rerun" if fresh.returncode == 0 else
           "The committed metrics.json does not match a rerun. Run python check_fresh.py to see the numbers.")
    growth = rerun_growth(clone)
    ok = growth is not None and good_growth(growth)
    report(ok, "The growth rate is the one this data supports" if ok else
           "A rerun of the committed params.yaml gives a growth rate this exercise doesn't accept. "
           "A rerun alone won't fix that. Compare the degrees with holdout.py, then decide.")


def check_message():
    history = git("log", "--reverse", "--format=%H", "--", "params.yaml").stdout.split()
    previous, culprit = None, None
    for sha in history:
        degree = re.search(r"^degree:\s*(\d+)", git("show", f"{sha}:params.yaml").stdout, re.M)
        degree = degree and degree.group(1)
        touched = git("show", "--name-only", "--format=", sha).stdout.split()
        if previous and degree != previous and "metrics.json" not in touched:
            culprit = sha
            break
        previous = degree
    if culprit is None:
        report(False, "I can't find the commit that changed the degree. Did the history get rewritten? "
                      "To start over, from the folder above project/: python scripts/setup_project.py --reset")
        return
    later = git("log", "--format=%H%x00%B%x01", f"{culprit}..HEAD").stdout.split("\x01")
    for entry in later:
        sha, _, message = entry.strip().partition("\x00")
        names_it = any(culprit.startswith(token) for token in re.findall(r"\b[0-9a-f]{7,40}\b", message))
        if names_it and "degree" in message.lower() and len(message) >= 60:
            report(True, "A commit message names the commit git bisect found and argues for the degree")
            return
    report(False, "No commit message names the commit git bisect found, with at least its first 7 characters, "
                  "and says why you chose this degree. Use the word degree and give your reason.")


def check_hook(clone):
    hook = PROJECT / git("rev-parse", "--git-path", "hooks/pre-commit").stdout.strip()
    if not hook.is_file() or not os.access(hook, os.X_OK):
        report(False, "The pre-commit hook is not installed in project/. Copy hooks/pre-commit into .git/hooks/. "
                      "A clone does not bring hooks with it.")
        return
    shutil.copy2(hook, Path(clone) / ".git" / "hooks" / "pre-commit")
    env = {**os.environ, "PATH": f"{Path(sys.executable).parent}{os.pathsep}{os.environ['PATH']}"}
    who = ("-c", "user.name=check", "-c", "user.email=check@example.org", "-c", "core.hooksPath=.git/hooks")

    readme = Path(clone) / "README.md"
    readme.write_text(readme.read_text() + "\nA harmless change.\n")
    run("git", "add", "README.md", cwd=clone, env=env)
    allowed = run("git", *who, "commit", "-m", "A harmless change", cwd=clone, env=env).returncode == 0

    params = Path(clone) / "params.yaml"
    params.write_text(re.sub(r"(?m)^degree:\s*(\d+)", lambda m: f"degree: {int(m.group(1)) + 1}", params.read_text()))
    run("git", "add", "params.yaml", cwd=clone, env=env)
    refused = run("git", *who, "commit", "-m", "A stale change", cwd=clone, env=env).returncode != 0
    ok = allowed and refused
    report(ok, "The hook refuses a stale metrics.json and allows everything else" if ok else
           "The installed hook should refuse a commit with a stale metrics.json and allow a fresh one. "
           "It did not. Compare it with hooks/pre-commit.")


def check_env():
    python = ENV / "bin" / "python"
    if not python.exists():
        report(False, "No environment at envs/co2. Build it with the commands in step 1.")
        return False
    meta = ENV / "conda-meta"
    records = [json.loads(f.read_text()) for f in meta.glob("*.json")]
    installed = {record.get("md5") for record in records}
    platform = next((r.get("subdir") for r in records if r.get("name") == "python"), None)
    mine = [lock for lock in PROJECT.glob("explicit-*.txt") if f"# platform: {platform}" in lock.read_text()]
    wanted = {line.rsplit("#", 1)[1].strip() for lock in mine for line in lock.read_text().splitlines()
              if line.startswith("http") and "#" in line}
    ok = bool(mine) and wanted == installed
    report(ok, "envs/co2 is exactly what the lock lists" if ok else
           "envs/co2 does not match your lock for this platform. If you changed environment.yml after building, run rm -rf ../envs/co2 and build it and write the lock again.")
    return True


def check_runs():
    with tempfile.TemporaryDirectory() as tmp:
        clone = Path(tmp) / "clone"
        git("clone", "--quiet", str(PROJECT), str(clone), cwd=tmp)
        ok = run(str(ENV / "bin" / "python"), "analyze.py", cwd=clone).returncode == 0
        report(ok, "analyze.py runs from a clean clone of your last commit" if ok else
               "analyze.py failed from a clean clone of your last commit, using envs/co2. Run it there and read the error.")


def check_rebuild():
    python = ENV / "bin" / "python"
    check_env()

    tag_type = git("--git-dir", str(REMOTE), "cat-file", "-t", "v1.0", cwd=HERE).stdout.strip()
    if tag_type != "tag":
        report(False, "remote/co2.git has no annotated tag v1.0. Use git tag -a v1.0, then git push origin v1.0.")
        return
    report(True, "Tag v1.0 is on the remote")
    if not python.exists():
        return
    with tempfile.TemporaryDirectory() as tmp:
        clone = Path(tmp) / "fresh"
        git("clone", "--quiet", "--branch", "v1.0", str(REMOTE), str(clone), cwd=tmp)
        result = run(str(python), "analyze.py", cwd=clone)
        changed = git("status", "--porcelain", cwd=clone).stdout.strip()
        committed = json.loads((clone / "metrics.json").read_text()).get("growth_rate_ppm_per_year") if result.returncode == 0 else None
        ok = result.returncode == 0 and not changed and good_growth(committed)
        report(ok, "A fresh clone of v1.0 in the rebuilt environment gives the same number" if ok else
               "A fresh clone of v1.0, run in envs/co2, did not reproduce the committed metrics.json with the accepted growth rate.")


def main():
    if not (PROJECT / ".git").exists():
        print("FAIL  project/ is not there. From the folder above it, run: python scripts/setup_project.py")
        print("       If you deleted it for step 3, clone it again: git clone remote/co2.git project")
        return 1
    check_declared()
    if "--short" in sys.argv:
        if check_env():
            check_runs()
        print(f"\n{sum(results)} of {len(results)} parts pass.")
        if all(results):
            print("You've finished the short path. Steps 2 and 3 are optional. To check them too, run: python ../check.py")
            return 0
        return 1
    with tempfile.TemporaryDirectory() as tmp:
        clone = Path(tmp) / "clone"
        git("clone", "--quiet", str(PROJECT), str(clone), cwd=tmp)
        check_number(clone)
        check_message()
        check_hook(clone)
    check_rebuild()
    print(f"\n{sum(results)} of {len(results)} parts pass.")
    if all(results):
        print("You're done. Tag v1.0 reruns from a fresh clone in an environment built from your lock.")
        return 0
    return 1


sys.exit(main())
