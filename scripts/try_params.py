#!/usr/bin/env python3
"""Change a parameter, ask Snakemake what it would rerun, then put the parameter back."""
import re
import subprocess
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1] / "project"
params = PROJECT / "params.yaml"
original = params.read_text()

params.write_text(re.sub(r"(?m)^max_depth_km:.*", "max_depth_km: 300", original))
try:
    print("I changed max_depth_km in params.yaml. A different depth limit means a different selection. snakemake -n says:\n")
    done = subprocess.run(["snakemake", "-n"], cwd=PROJECT, capture_output=True, text=True)
    text = done.stdout + done.stderr
    # Skip Snakemake's host and version block, and the per-job details after the job table.
    body = text.partition("Building DAG of jobs...\n")[2]
    print(body.split("\n\n")[0] if body else text)
finally:
    params.write_text(original)
print("I put params.yaml back.")
