#!/usr/bin/env python3
"""Check your work. Each part prints PASS or FAIL with what to do next. It reads what you committed.

It works in a throwaway clone of your last commit, so it can't damage your project.
Nothing built is in Git, so it builds everything from the raw data and compares the result with the numbers on the page.

Run it from project/:
python ../check.py           checks everything. --short is accepted and runs the same parts.
Add --nextflow to check a main.nf instead of a Snakefile (the Nextflow page).
"""
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
FIGURE = "figures/body_mass.svg"
NEXTFLOW = "--nextflow" in sys.argv
WORKFLOW_FILE = "main.nf" if NEXTFLOW else "Snakefile"
COMMAND = "nextflow run main.nf" if NEXTFLOW else "snakemake --cores 1"
# What the 2007 data gives with statistic: mean. The page shows the same numbers.
EXPECTED = {"dimorphism_g_adelie": 648.9, "dimorphism_g_chinstrap": 250.0, "dimorphism_g_gentoo": 934.2, "n_rows": 103}
# What the figure shows: penguins and median body mass per species and sex, from plot.py's description in the SVG.
# The SVG's bytes depend on the font library in your environment, so the check reads what it plots, not its hash.
EXPECTED_FIGURE = {("Adelie", "female"): (22, 3325.0), ("Adelie", "male"): (22, 3950.0),
                   ("Chinstrap", "female"): (13, 3575.0), ("Chinstrap", "male"): (13, 3775.0),
                   ("Gentoo", "female"): (16, 4625.0), ("Gentoo", "male"): (17, 5550.0)}

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


def last_line(done):
    lines = [line for line in (done.stdout + done.stderr).splitlines() if line.strip()]
    errors = [line for line in lines if re.search(r"Error|ERROR", line)]
    return (errors or lines)[0 if errors else -1] if lines else "no output"


def tasks(clone):
    """Which processes the last Nextflow run ran, and which it took from the cache, from its own log."""
    log = (clone / ".nextflow.log").read_text()
    return set(re.findall(r"Submitted process > (\w+)", log)), set(re.findall(r"Cached process > (\w+)", log))


def metrics(clone):
    path = clone / "metrics.json"
    return json.loads(path.read_text()) if path.exists() else None


def figure(path):
    """What an SVG from plot.py shows, read from its description: {(species, sex): (penguins, median)}."""
    found = re.findall(r"(\w+) (female|male): (\d+) penguins, median ([\d.]+) g", path.read_text()) if path.exists() else []
    return {(name, sex): (int(count), float(median)) for name, sex, count, median in found}


def stamp(clone, name):
    return (clone / name).stat().st_mtime_ns if (clone / name).exists() else None


def flip_statistic(clone):
    """Change report.statistic between mean and median. Returns the committed value, or None if there's no such line."""
    params = clone / "params.yaml"
    text = params.read_text()
    found = re.search(r"(?m)^(\s+statistic:\s*)(mean|median)", text)
    if not found:
        return None
    other = "median" if found.group(2) == "mean" else "mean"
    params.write_text(text[:found.start(2)] + other + text[found.end(2):])
    return found.group(2)


def check_workflow_file(clone):
    """Part 1: the workflow file parses and declares the figure step. Returns False only if it doesn't parse."""
    if not (clone / WORKFLOW_FILE).exists():
        report(False, f"No {WORKFLOW_FILE} is committed. Put it back from the starter: git checkout HEAD~ -- {WORKFLOW_FILE}, or start over.")
        return False
    if NEXTFLOW:
        dry = nextflow(clone, "-preview")
        if dry.returncode != 0:
            report(False, f"nextflow run main.nf -preview fails on your last commit: {last_line(dry)}")
            return False
        text = (clone / "main.nf").read_text()
        ok = bool(re.search(r"(?m)^\s*process\s+PLOT\s*\{", text) and re.search(r"(?m)^\s*PLOT\s*\(", text))
        report(ok, "main.nf has a PLOT process, and the workflow block calls it" if ok else
               "main.nf has no PLOT process called in the workflow block. Add it in step 2, then commit main.nf.")
        return True
    dry = snakemake(clone, "-n", "--forceall", "--quiet", "host")  # with each job's inputs and outputs
    if dry.returncode != 0:
        report(False, f"snakemake -n fails on your last commit: {last_line(dry)}")
        return False
    rule = re.search(r"(?m)^rule plot:\n\s+input: (.*)\n\s+output: (.*)", dry.stdout)
    inputs = set(rule.group(1).split(", ")) if rule else set()
    if not rule:
        report(False, f"Snakemake has no plot rule to run for the default target. Add rule plot, and add {FIGURE} "
                      "to the input of rule all (step 2). Then commit the Snakefile.")
    elif rule.group(2).strip() != FIGURE or not {"results/validated.csv", "plot.py"} <= inputs:
        report(False, f"Rule plot reads {rule.group(1)} and writes {rule.group(2)}. It should read results/validated.csv "
                      f"and plot.py, and write {FIGURE} (step 2).")
    else:
        report(True, f"The Snakefile has a plot rule that reads results/validated.csv and plot.py and writes {FIGURE}, "
                     "and rule all asks for the figure")
    return True


def check_build(clone):
    """Part 2: build from the raw data, and compare the numbers with the page."""
    for name in ("results", "figures", "metrics.json"):
        shutil.rmtree(clone / name, ignore_errors=True) if (clone / name).is_dir() else (clone / name).unlink(missing_ok=True)
    built = nextflow(clone) if NEXTFLOW else snakemake(clone, "--forceall")
    if built.returncode != 0:
        return report(False, f"In a clean clone, {COMMAND} failed: {last_line(built)}")
    found = metrics(clone)
    if found is None:
        return report(False, f"In a clean clone, {COMMAND} finished without writing metrics.json. Put the starter's report step back.")
    ok = found == EXPECTED
    return report(ok, f"In a clean clone, {COMMAND} builds metrics.json from the raw data, and the numbers match the page" if ok else
                  f"In a clean clone, {COMMAND} builds metrics.json, and the numbers differ from the page: {found}. "
                  "Is params.yaml back to statistic: mean, and are the scripts unchanged?")


def check_figure(clone):
    """Part 3: the build drew the figure from the data, and plot.py draws the same bytes again."""
    built = clone / FIGURE
    if not built.exists():
        return report(False, f"The build wrote no {FIGURE}. README.md shows it, so declare the step that draws it (step 2).")
    shown = figure(built)
    if shown != EXPECTED_FIGURE:
        return report(False, f"{FIGURE} doesn't show the 2007 penguins the numbers come from. Shown: {shown or 'nothing plot.py wrote'}. "
                             "Build it with plot.py from results/validated.csv.")
    first = built.read_bytes()
    redone = run(sys.executable, "plot.py", cwd=clone)
    if redone.returncode != 0 or built.read_bytes() != first:
        return report(False, f"plot.py run again on the same data drew a different {FIGURE}. Put plot.py back as the starter had it.")
    if "](figures/body_mass.svg)" not in (clone / "README.md").read_text():
        return report(False, "README.md doesn't show the figure any more. Put back the line ![Body mass by species and sex](figures/body_mass.svg).")
    return report(True, f"{COMMAND} draws {FIGURE} from the data, the same bytes every time, and README.md shows it")


def check_params(clone):
    """Part 4: statistic is back to mean, and a changed statistic reruns only the report step."""
    before = metrics(clone)
    committed = flip_statistic(clone)
    if committed is None:
        return report(False, "params.yaml has no report.statistic line that says mean or median. Put it back, so report.py can read it.")
    if committed != "mean":
        return report(False, "params.yaml says statistic: median in your last commit. Set it back to mean and commit (step 3).")
    if NEXTFLOW:
        done = nextflow(clone, "-resume")
        ran, cached = tasks(clone) if done.returncode == 0 else (set(), set())
        if done.returncode != 0 or metrics(clone) == before or "REPORT" not in ran:
            return report(False, "I changed report.statistic, ran nextflow run main.nf -resume, and REPORT didn't rerun. "
                                 f"Ran: {', '.join(sorted(ran)) or 'nothing'}. params.yaml has to be an input of REPORT.")
        if ran != {"REPORT"}:
            return report(False, f"I changed report.statistic, and more than REPORT ran: {', '.join(sorted(ran))}. "
                                 "Only REPORT reads params.yaml, so only REPORT should list it as an input.")
        return report(True, f"A changed report.statistic reruns REPORT, and -resume takes the rest from the cache: {', '.join(sorted(cached))}")
    clean_before, figure_before = stamp(clone, "results/clean.csv"), stamp(clone, FIGURE)
    done = snakemake(clone)
    if done.returncode != 0 or metrics(clone) == before:
        return report(False, "I changed report.statistic, ran snakemake --cores 1, and metrics.json did not change. "
                             "The report rule needs params: config[\"report\"], as the starter had it.")
    if stamp(clone, "results/clean.csv") != clean_before or stamp(clone, FIGURE) != figure_before:
        return report(False, "I changed report.statistic, and clean or plot reran too. Only report.py reads that parameter, "
                             "so only the report rule should declare it, and no rule should list params.yaml as an input.")
    return report(True, "A changed report.statistic reruns report, not clean or plot")


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
            check_figure(clone)
            check_params(clone)
    print(f"\n{sum(results)} of {len(results)} parts pass.")
    if all(results):
        print("You're done. One command builds the numbers and the figure from the raw data, and a changed parameter reruns only what reads it.")
        return 0
    return 1


sys.exit(main())
