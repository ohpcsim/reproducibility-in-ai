#!/usr/bin/env python3
"""Check your work. Each part prints PASS or FAIL with what to do next. It reads what you committed.

It builds a correct card from the project's files at run time, damages it in several ways, and asks
your tests about each one. So the check is about your tests, and there's no answer in this file to copy.

Run it from project/:
python ../check.py --short   checks step 1, the short path.
python ../check.py           checks everything.
"""
import json
import os
import random
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
PROJECT = HERE / "project"

results = []


def mark(ok):
    word, color = ("PASS", 32) if ok else ("FAIL", 31)
    return f"\033[{color}m{word}\033[0m" if sys.stdout.isatty() or os.environ.get("CLICOLOR_FORCE") else word


def report(ok, message):
    results.append(ok)
    print(f"{mark(ok)}  {message}", flush=True)
    return ok


def run(*args, cwd=PROJECT, env=None):
    return subprocess.run(args, cwd=cwd, env=env, capture_output=True, text=True)


def clean_card(clone):
    """A correct card, built from the project's own files."""
    accuracy = json.loads((clone / "metrics.json").read_text())["val_accuracy"]
    params = yaml.safe_load((clone / "params.yaml").read_text())
    release = yaml.safe_load((clone / "release.yaml").read_text())
    data = yaml.safe_load((clone / "sources.yaml").read_text())["dataset"]
    sizes = release["split_sizes"]
    return f"""# Model card: {release['artifact']}

The registered version in {release['stage']} is {release['registered_version']}.
Validation accuracy is {accuracy:.3f}, as a fraction of rows, measured on the validation split.
The lock file that records the pipeline is dvc.lock.
The splits have {sizes['train']} train rows, {sizes['val']} validation rows and {sizes['test']} test rows.
The network has {params['train']['hidden']} hidden units.

The data is {data['name']}, with {data['images']} images, from {data['url']}.

This model is for teaching only. It must not be used to make a decision about a real person.
We refused candidate-v2, because its training rows overlap its validation and test rows.
"""


def mutants(card, rng):
    """Each one breaks a rule from the exercise. The random parts mean you can't test for exact strings."""
    number = rng.randint(100, 999)
    accuracy = re.search(r"0\.\d{3}", card).group(0)
    version = re.search(r"v\d+\.\d+\.\d+", card).group(0)
    size = re.search(r"have (\d+) train", card).group(1)
    return {
        "a changed accuracy": card.replace(accuracy, f"0.{rng.randint(900, 979)}"),
        "an accuracy rounded to two decimals": card.replace(accuracy, accuracy[:4]),
        "a changed split size": card.replace(f"have {size} train", f"have {int(size) + rng.randint(1, 50)} train"),
        "an extra number that isn't in the evidence": card + f"\nIt was trained for {number} epochs.\n",
        "a URL that isn't in the evidence": card + f"\nMore at https://example.org/{number}.\n",
        "no registered version": card.replace(version, "the latest version"),
        "no lock file named": card.replace("dvc.lock", "a lock file"),
        "a clinical claim": card + "\nThis model is suitable for clinical diagnosis.\n",
    }


def verdict(clone, text):
    """True if the tests accept this card, False if they reject it, None if they didn't run."""
    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as out:
        out.write(text)
    try:
        return tests_accept(clone, out.name)
    finally:
        os.unlink(out.name)


def tests_accept(clone, path):
    done = run(sys.executable, "-m", "pytest", "-q", "--tb=no", "--color=no", "-p", "no:cacheprovider", "tests",
               cwd=clone, env={**os.environ, "CARD": str(path)})
    return {0: True, 1: False}.get(done.returncode)


def check_tests(clone, rng):
    card = clean_card(clone)
    accepted = verdict(clone, card)
    if accepted is None:
        report(False, "Your tests didn't run. Try: CARD=runs/codex/card.md python -m pytest -q tests")
        return False
    if not report(accepted, "Your tests accept a correct card" if accepted else
                  "Your tests reject a correct card that this script built from the project's files. Are they too strict?"):
        return False
    for name, text in mutants(card, rng).items():
        rejected = verdict(clone, text) is False
        report(rejected, f"Your tests reject a card with {name}" if rejected else
               f"I gave your tests a card with {name}, and they accepted it. Add a test.")
    return True


def check_prompt(clone):
    prompt = (clone / "prompts" / "model-card.md").read_text()
    ok = re.search(r"evidence|source|file", prompt, re.I) and re.search(r"\bunits?\b", prompt, re.I) and len(prompt) > 80
    report(bool(ok), "The prompt asks for evidence and units" if ok else
           "prompts/model-card.md still doesn't ask where each number comes from, and in what unit. Repair it and commit it.")


def check_planted(clone):
    planted = sorted((clone / "runs").glob("planted-*/card.md"))
    missed = [card.parent.name for card in planted if tests_accept(clone, card) is not False]
    report(not missed, "Your tests reject all three planted cards" if not missed else
           f"Your tests accept these planted cards: {', '.join(missed)}. Read each one's manifest, and find out why.")


def check_second_model(clone, rng):
    stated = clean_card(clone)
    without = "\n".join(line for line in stated.splitlines() if "teaching" not in line and "candidate-v2" not in line) + "\n"
    rejected = verdict(clone, without) is False
    report(rejected, "Your tests require the two recorded decisions" if rejected else
           "A card without the teaching-only limit or the refusal of candidate-v2 still passes. Add a test for each (step 3).")
    expected = {"model-a-codex-chat": True, "opencode-free": False, "model-b-opencode-second": True}
    for name, want in expected.items():
        got = tests_accept(clone, clone / "runs" / name / "card.md")
        report(got is want, f"Your tests {'accept' if want else 'reject'} {name}" if got is want else
               f"Your tests should {'accept' if want else 'reject'} runs/{name}/card.md once they check the decisions. They don't.")
    path = clone / "decisions.yaml"
    text = path.read_text() if path.exists() else ""
    ok = re.search(r"teaching", text, re.I) and "candidate-v2" in text
    report(bool(ok), "decisions.yaml holds both decisions" if ok else
           "Commit decisions.yaml with the two decisions from Model A's transcript, so the next model doesn't need the chat.")


def check_record(clone):
    original = run("git", "rev-list", "--max-parents=0", "HEAD", cwd=clone).stdout.strip()
    kept = run("git", "diff", "--name-only", "--diff-filter=D", original, "HEAD", "--", "runs", cwd=clone).stdout.strip()
    report(not kept, "All the recorded runs are still there, including the losers" if not kept else
           "You deleted recorded runs. Keep the losers, so that someone can see what you rejected.")
    try:
        manifest = yaml.safe_load((clone / "manifest.yaml").read_text()) or {}
    except yaml.YAMLError:
        manifest = {}
    empty = [key for key in ("tool", "tool_version", "provider", "model", "revision", "run_date", "settings", "prompt", "evaluation",
                             "acceptance", "reviewer", "not_exposed") if not manifest.get(key)]
    report(not empty, "manifest.yaml is complete, including not_exposed" if not empty else
           f"manifest.yaml has nothing under: {', '.join(empty)}. If something isn't exposed to you, say so.")
    path = clone / "decisions.md"
    text = path.read_text() if path.exists() else ""
    named = [name for name in re.findall(r"[a-z][a-z0-9-]+", text) if (clone / "runs" / name / "card.md").is_file()]
    if not named or len(text) < 60:
        report(False, "Commit decisions.md. Name the run you accept, as it's named under runs/, and say why.")
    elif any(name.startswith("planted-") for name in named):
        report(False, "decisions.md names a planted card. Those were edited by hand to be wrong.")
    else:
        ok = all(tests_accept(clone, clone / "runs" / name / "card.md") is True for name in named[:1])
        report(ok, f"decisions.md accepts {named[0]}, and your tests agree" if ok else
               f"decisions.md accepts {named[0]}, but your tests reject it. Decide which is right, and write down why.")


def main():
    short = "--short" in sys.argv
    if not (PROJECT / ".git").exists():
        print("FAIL  project/ is not there. From the folder above it, run: python scripts/setup_project.py")
        return 1
    if run("git", "status", "--porcelain").stdout.strip():
        print("Note: you have uncommitted changes. This checks your last commit only.\n", flush=True)
    rng = random.Random()
    with tempfile.TemporaryDirectory() as tmp:
        clone = Path(tmp) / "clone"
        run("git", "clone", "--quiet", str(PROJECT), str(clone), cwd=tmp)
        tests_ran = check_tests(clone, rng)
        check_prompt(clone)
        if not short:
            if tests_ran:
                check_planted(clone)
                check_second_model(clone, rng)
            check_record(clone)
    print(f"\n{sum(results)} of {len(results)} parts pass.")
    if not all(results):
        return 1
    print("You've finished the short path. Steps 2 to 4 are optional. To check them too, run: python ../check.py" if short else
          "You're done. Your tests decide, the decisions are in the project, and the losing runs are kept.")
    return 0


sys.exit(main())
