#!/usr/bin/env python3
"""Check your work. Each part prints PASS or FAIL with what to do next. It reads what you committed.

It works in a throwaway clone of your last commit, so it can't damage your project.

Run it from project/:
python ../check.py           checks everything. --short is accepted and runs the same parts.
Add --nextflow to check a main.nf instead of a Snakefile (the Nextflow page).
"""
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJECT = HERE / "project"
OUTPUTS = ("results/clean.csv", "results/validated.csv", "metrics.json")
NEXTFLOW = "--nextflow" in sys.argv
WORKFLOW_FILE = "main.nf" if NEXTFLOW else "Snakefile"
COMMAND = "nextflow run main.nf" if NEXTFLOW else "snakemake --cores 1"

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
    errors = [line for line in lines if re.search(r"Error|ERROR", line)]
    return (errors or lines)[0 if errors else -1] if lines else "no output"


def tasks(clone):
    """Which processes the last Nextflow run ran, and which it took from the cache, from its own log."""
    log = (clone / ".nextflow.log").read_text()
    return set(re.findall(r"Submitted process > (\w+)", log)), set(re.findall(r"Cached process > (\w+)", log))


def metrics(clone):
    return json.loads((clone / "metrics.json").read_text())


def stamp(clone, name):
    return (clone / name).stat().st_mtime_ns if (clone / name).exists() else None


def flip_statistic(clone):
    """Change report.statistic between mean and median. Returns False if params.yaml has no such line."""
    params = clone / "params.yaml"
    text = params.read_text()
    found = re.search(r"(?m)^(\s+statistic:\s*)(mean|median)", text)
    if not found:
        return False
    other = "median" if found.group(2) == "mean" else "mean"
    params.write_text(text[:found.start(2)] + other + text[found.end(2):])
    return True


def check_workflow_file(clone):
    if not (clone / WORKFLOW_FILE).exists():
        return report(False, f"No {WORKFLOW_FILE} is committed. Write the {'processes' if NEXTFLOW else 'rules'} in step 1, "
                             f"then git add {WORKFLOW_FILE} and commit.")
    dry = nextflow(clone, "-preview") if NEXTFLOW else snakemake(clone, "-n")
    return report(dry.returncode == 0, f"The committed {WORKFLOW_FILE} parses" if dry.returncode == 0 else
                  f"{COMMAND + ' -preview' if NEXTFLOW else 'snakemake -n'} fails on your last commit: {last_line(dry)}")


def check_build(clone):
    if not (clone / "metrics.json").exists():
        return report(False, "metrics.json is not committed. Build it and commit it, so a reader sees the numbers without running anything.")
    committed = metrics(clone)
    for name in OUTPUTS:
        (clone / name).unlink(missing_ok=True)
    built = build(clone)
    if built.returncode != 0:
        return report(False, f"In a clean clone with every output deleted, {COMMAND} failed: {last_line(built)}")
    if not (clone / "metrics.json").exists():
        return report(False, f"In a clean clone with every output deleted, {COMMAND} finished without writing metrics.json. " +
                      ("Add the VALIDATE and REPORT processes and call them in the workflow block (step 1)." if NEXTFLOW else
                       "Add the rules for validate.py and report.py (step 1)."))
    report(True, f"{COMMAND.split()[0]} builds metrics.json from the raw data in a clean clone")
    fresh = metrics(clone) == committed
    return report(fresh, "The committed metrics.json matches a clean build" if fresh else
                  "The committed metrics.json does not match a clean build from the raw data. "
                  f"Run {COMMAND if NEXTFLOW else COMMAND + ' --forceall'}, then commit metrics.json.")


def check_params(clone):
    before = metrics(clone)
    if not flip_statistic(clone):
        return report(False, "params.yaml has no report.statistic line that says mean or median. Put it back, so report.py can read it.")
    clean_before = stamp(clone, "results/clean.csv")
    done = snakemake(clone)
    changed = done.returncode == 0 and metrics(clone) != before
    if not changed:
        report(False, "I changed report.statistic in params.yaml, ran snakemake --cores 1, and metrics.json did not change. "
                      "Declare the parameters report.py reads in the report rule: params: config[\"report\"] (step 1).")
    elif stamp(clone, "results/clean.csv") != clean_before:
        report(False, "I changed report.statistic and results/clean.csv rebuilt too. Only report.py reads that parameter. "
                      "Give each rule the section of params.yaml it reads with params:, and don't list params.yaml as an input (step 1).")
    else:
        report(True, "A changed report.statistic reruns report and not clean")


def check_nextflow_params(clone):
    before = metrics(clone)
    if not flip_statistic(clone):
        return report(False, "params.yaml has no report.statistic line that says mean or median. Put it back, so report.py can read it.")
    done = nextflow(clone, "-resume")
    ran, cached = tasks(clone) if done.returncode == 0 else (set(), set())
    changed = done.returncode == 0 and metrics(clone) != before
    if not changed or "REPORT" not in ran:
        report(False, "I changed report.statistic in params.yaml, ran nextflow run main.nf -resume, and the result did not follow. "
                      f"Ran: {', '.join(sorted(ran)) or 'nothing'}. Cached: {', '.join(sorted(cached)) or 'nothing'}. "
                      "params.yaml has to be an input of REPORT, and publishDir needs overwrite: true (step 1).")
    elif "VALIDATE" not in cached:
        report(False, "I changed report.statistic and VALIDATE ran again too. Its inputs have the same content, so -resume should take it "
                      "from the cache. VALIDATE reads results/clean.csv and validate.py, not params.yaml (step 1).")
    else:
        report(True, "A changed report.statistic reruns REPORT, and -resume takes VALIDATE from the cache")


def main():
    if not (PROJECT / ".git").exists():
        print("FAIL  project/ is not there. From the folder above it, run: python scripts/setup_project.py")
        return 1
    if git("status", "--porcelain").stdout.strip():
        print("Note: you have uncommitted changes. This checks your last commit only.\n", flush=True)
    with tempfile.TemporaryDirectory() as tmp:
        clone = Path(tmp) / "clone"
        git("clone", "--quiet", str(PROJECT), str(clone), cwd=tmp)
        if check_workflow_file(clone) and check_build(clone):
            check_nextflow_params(clone) if NEXTFLOW else check_params(clone)
    print(f"\n{sum(results)} of {len(results)} parts pass.")
    if all(results):
        print("You're done. One command rebuilds the result from the raw data, and a changed parameter reruns only what depends on it.")
        return 0
    return 1


sys.exit(main())
