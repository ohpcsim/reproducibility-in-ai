#!/usr/bin/env python3
"""Check your work. Each part prints PASS or FAIL with what to do next. It reads what you committed.

It works in a throwaway clone of your last commit, so it can't damage your project. It knows
the accepted start magnitudes only as salted digests, so it holds no answer to look up.

Run it from project/:
python ../check.py --short   checks step 1, the short path.
python ../check.py           checks everything.
Add --nextflow to check a main.nf instead of a Snakefile (the Nextflow page).
"""
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
OUTPUTS = ("results/subset.csv", "results/counts.csv", "metrics.json")
NEXTFLOW = "--nextflow" in sys.argv
WORKFLOW_FILE = "main.nf" if NEXTFLOW else "Snakefile"
COMMAND = "nextflow run main.nf" if NEXTFLOW else "snakemake --cores 1"
# What the tool writes besides the outputs. Cattle, and in .gitignore.
SCRATCH = ("results", "work", ".nextflow") if NEXTFLOW else ("results", ".snakemake")

# The digests let this script recognize an accepted start magnitude without containing one.
SALT = "earthquakes-exercise-2:"
ACCEPTED = {
    "d8071bd2120d6bf2aee166dc3835e6a63cf4aaa0066e0214ccab2e67412c2e1e",
    "0ed3fbe7382273b572468c58daf05168d602c98c773394974141e97f0870f44d",
    "2763b0abd5daf4f25f33f05f7e57473ff30654e878a2276e92675385ca087b57",
    "8bac93cdaeb782d41b08dacde7d8dcbcad3bd98c131104850884af3a21e31feb",
    "69da54d485c956b62abbd4eeafe92f1fcb296b9f1a3ee01b1c328be23cb60a42",
    "e3f834a92d0c8fb24b0f4fe650954ab9a4bc0d7da572b425b27eb813d3268876",
}

results = []


def mark(ok):
    word, color = ("PASS", 32) if ok else ("FAIL", 31)
    return f"\033[{color}m{word}\033[0m" if sys.stdout.isatty() or os.environ.get("CLICOLOR_FORCE") else word


def report(ok, message):
    results.append(ok)
    print(f"{mark(ok)}  {message}", flush=True)
    return ok


def run(*args, cwd):
    return subprocess.run(args, cwd=cwd, capture_output=True, text=True)


def git(*args, cwd=PROJECT):
    return run("git", *args, cwd=cwd)


def snakemake(clone, *args):
    return run("snakemake", "--cores", "1", *args, cwd=clone)


def nextflow(clone, *args):
    return run("nextflow", "run", "main.nf", "-ansi-log", "false", *args, cwd=clone)


def build(clone):
    return nextflow(clone) if NEXTFLOW else snakemake(clone)


def last_line(done):
    lines = [line for line in (done.stdout + done.stderr).splitlines() if line.strip()]
    errors = [line for line in lines if line.startswith("Error") or "ERROR" in line]
    return (errors or lines)[0 if errors else -1] if lines else "no output"


def tasks(clone):
    """Which processes the last Nextflow run ran, and which it took from the cache, from its own log."""
    log = (clone / ".nextflow.log").read_text()
    return set(re.findall(r"Submitted process > (\w+)", log)), set(re.findall(r"Cached process > (\w+)", log))


def metrics(clone):
    return json.loads((clone / "metrics.json").read_text())


def stamps(clone):
    return [(clone / name).stat().st_mtime_ns if (clone / name).exists() else None for name in OUTPUTS]


def min_magnitude(text):
    found = re.search(r"(?m)^min_magnitude:\s*([\d.]+)", text)
    return float(found.group(1)) if found else None


def check_workflow_file(clone):
    if not (clone / WORKFLOW_FILE).exists():
        return report(False, f"No {WORKFLOW_FILE} is committed. Write the {'processes' if NEXTFLOW else 'rules'} in step 1, "
                             f"then git add {WORKFLOW_FILE} and commit.")
    dry = nextflow(clone, "-preview") if NEXTFLOW else snakemake(clone, "-n")
    return report(dry.returncode == 0, f"The committed {WORKFLOW_FILE} parses" if dry.returncode == 0 else
                  f"{COMMAND + ' -preview' if NEXTFLOW else 'snakemake -n'} fails on your last commit: {last_line(dry)}")


def check_build(clone):
    if not (clone / "metrics.json").exists():
        return report(False, "metrics.json is not committed. Build it and commit it, so a reader sees the number without running anything.")
    committed = metrics(clone)
    for name in OUTPUTS:
        (clone / name).unlink(missing_ok=True)
    built = build(clone)
    if built.returncode != 0:
        return report(False, f"In a clean clone with every output deleted, {COMMAND} failed: {last_line(built)}")
    if not (clone / "metrics.json").exists():
        return report(False, f"In a clean clone with every output deleted, {COMMAND} finished without writing metrics.json. " +
                      ("Add the COUNT and FIT processes and call them in the workflow block (step 1)." if NEXTFLOW else
                       "Add the rules for count.py and fit.py (step 1)."))
    report(True, f"{COMMAND.split()[0]} builds metrics.json from the raw data in a clean clone")
    fresh = metrics(clone) == committed
    return report(fresh, "The committed metrics.json matches a clean build" if fresh else
                  "The committed metrics.json does not match a clean build from the raw data. "
                  f"Run {COMMAND if NEXTFLOW else COMMAND + ' --forceall'}, then commit metrics.json.")


def check_params(clone):
    before = metrics(clone)["n_earthquakes"]
    params = clone / "params.yaml"
    text = params.read_text()
    depth = re.search(r"(?m)^max_depth_km:\s*(\d+)", text)
    if not depth:
        return report(False, "params.yaml has no max_depth_km line. Put it back, so subset.py can read it.")
    other = 700 if int(depth.group(1)) < 300 else 70
    params.write_text(re.sub(r"(?m)^max_depth_km:.*", f"max_depth_km: {other}", text))
    done = snakemake(clone)
    changed = done.returncode == 0 and metrics(clone)["n_earthquakes"] != before
    report(changed, "A changed parameter rebuilds the result" if changed else
           "I changed max_depth_km in params.yaml, ran snakemake --cores 1, and metrics.json did not change. "
           "Declare params.yaml as an input of the rule that runs subset.py (step 2).")
    git("checkout", "--", "params.yaml", cwd=clone)
    snakemake(clone)


def check_code(clone):
    before = stamps(clone)
    with open(clone / "count.py", "a") as script:
        script.write("\n# An edit to the code.\n")
    done = snakemake(clone)
    after = stamps(clone)
    downstream = done.returncode == 0 and before[1] != after[1] and before[2] != after[2]
    if not downstream:
        report(False, "I edited count.py, ran snakemake --cores 1, and results/counts.csv did not rebuild. "
                      "Declare each script as an input of its rule (step 2).")
    elif before[0] != after[0]:
        report(False, "I edited count.py and results/subset.csv rebuilt too. Only the steps after a change should rerun. "
                      "Check the inputs of the rule that runs subset.py.")
    else:
        report(True, "An edited script reruns its step and the steps after it, and nothing else")
    git("checkout", "--", "count.py", cwd=clone)


def check_nextflow_code(clone):
    with open(clone / "count.py", "a") as script:
        script.write("\n# An edit to the code.\n")
    done = nextflow(clone, "-resume")
    ran, cached = tasks(clone) if done.returncode == 0 else (set(), set())
    if "COUNT" not in ran:
        report(False, "I edited count.py, ran nextflow run main.nf -resume, and COUNT did not rerun. "
                      "The script has to be an input of its process, so an edit changes the task hash (step 2).")
    elif "SUBSET" not in cached:
        report(False, "I edited count.py and SUBSET ran again too. With -resume, a task whose inputs and script are unchanged "
                      "comes from the cache. Check the inputs of SUBSET (step 2).")
    else:
        report(True, "An edited script reruns its task, and -resume takes the task before it from the cache")
    git("checkout", "--", "count.py", cwd=clone)


def check_nextflow_params(clone):
    before = metrics(clone)["n_earthquakes"]
    params = clone / "params.yaml"
    text = params.read_text()
    depth = re.search(r"(?m)^max_depth_km:\s*(\d+)", text)
    if not depth:
        return report(False, "params.yaml has no max_depth_km line. Put it back, so subset.py can read it.")
    other = 700 if int(depth.group(1)) < 300 else 70
    params.write_text(re.sub(r"(?m)^max_depth_km:.*", f"max_depth_km: {other}", text))
    done = nextflow(clone, "-resume")
    ran, cached = tasks(clone) if done.returncode == 0 else (set(), set())
    changed = done.returncode == 0 and metrics(clone)["n_earthquakes"] != before and {"SUBSET", "COUNT", "FIT"} <= ran
    report(changed, "A changed parameter reruns every task that depends on it" if changed else
           "I changed max_depth_km in params.yaml, ran nextflow run main.nf -resume, and the result did not follow. "
           f"Ran: {', '.join(sorted(ran)) or 'nothing'}. Cached: {', '.join(sorted(cached)) or 'nothing'}. "
           "Every task downstream of params.yaml has to rerun (step 2).")
    git("checkout", "--", "params.yaml", cwd=clone)


def check_decision():
    chosen = min_magnitude(git("show", "HEAD:params.yaml").stdout)
    ok = chosen is not None and hashlib.sha256(f"{SALT}{chosen:.1f}".encode()).hexdigest() in ACCEPTED
    report(ok, "min_magnitude is a start magnitude this catalog supports" if ok else
           "The committed min_magnitude is not a start magnitude this exercise accepts. Read the table from "
           "python completeness.py, and pick the lowest start magnitude at which b has stopped rising (step 2).")
    if not ok:
        return
    for sha in git("log", "--format=%H", "--", "params.yaml").stdout.split():
        parent = git("show", f"{sha}^:params.yaml")
        was = min_magnitude(parent.stdout) if parent.returncode == 0 else None
        if min_magnitude(git("show", f"{sha}:params.yaml").stdout) != was:
            message = git("log", "-1", "--format=%B", sha).stdout.strip()
            said = f"{chosen:.1f}" in message and len(message) >= 40
            report(said, "The commit that set min_magnitude names the magnitude and gives a reason" if said else
                   "The commit that set min_magnitude does not name the magnitude and say why. "
                   "Commit the choice with its reason from the completeness table (step 2).")
            return


def check_cattle(clone, built):
    if "completeness.md" not in git("ls-tree", "-r", "--name-only", "HEAD").stdout.split():
        return report(False, "completeness.md is not committed. " +
                      ("Add a COMPLETENESS process that writes it, call it in the workflow block, build it and commit it (step 2)." if NEXTFLOW else
                       "Declare a rule that writes it, add it to rule all, build it and commit it (step 3)."))
    if not built:
        return
    git("checkout", "--", ".", cwd=clone)
    for folder in SCRATCH:
        shutil.rmtree(clone / folder, ignore_errors=True)
    for name in ("metrics.json", "completeness.md", *clone.glob(".nextflow.log*")):
        (clone / name).unlink(missing_ok=True)
    done = build(clone)
    status = git("status", "--porcelain", cwd=clone).stdout.strip()
    ok = done.returncode == 0 and not status
    report(ok, "Every output comes back byte for byte from the raw data" if ok else
           f"I deleted every output in a clone and ran {COMMAND}, and git status --short was not empty: "
           f"{status.replace(chr(10), ', ') or last_line(done)}. Every committed output has to come back from the workflow" +
           (", and work/, .nextflow/ and .nextflow.log* belong in .gitignore (step 2)." if NEXTFLOW else " (step 3)."))


def main():
    short = "--short" in sys.argv
    if not (PROJECT / ".git").exists():
        print("FAIL  project/ is not there. From the folder above it, run: python scripts/setup_project.py")
        return 1
    if git("status", "--porcelain").stdout.strip():
        print("Note: you have uncommitted changes. This checks your last commit only.\n", flush=True)
    with tempfile.TemporaryDirectory() as tmp:
        clone = Path(tmp) / "clone"
        git("clone", "--quiet", str(PROJECT), str(clone), cwd=tmp)
        built = check_workflow_file(clone) and check_build(clone)
        if short:
            print(f"\n{sum(results)} of {len(results)} parts pass.")
            if all(results):
                print("You've finished the short path. " + ("Step 2 is optional. To check it too, run: python ../check.py --nextflow" if NEXTFLOW else
                      "Steps 2 and 3 are optional. To check them too, run: python ../check.py"))
                return 0
            return 1
        if built and NEXTFLOW:
            check_nextflow_code(clone)
            check_nextflow_params(clone)
        elif built:
            check_params(clone)
            check_code(clone)
        check_decision()
        check_cattle(clone, built)
    print(f"\n{sum(results)} of {len(results)} parts pass.")
    if all(results):
        print("You're done. One command rebuilds every output from the raw data, and a change reruns only what depends on it.")
        return 0
    return 1


sys.exit(main())
