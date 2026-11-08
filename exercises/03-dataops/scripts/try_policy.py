#!/usr/bin/env python3
"""Change the cleaning policy, ask DVC what it would rerun, then put the policy back."""
import re
import subprocess
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1] / "project"
params = PROJECT / "params.yaml"
original = params.read_text()
flip = {"true": "false", "false": "true"}
changed = re.sub(r"(drop_missing_sex:\s*)(true|false)", lambda m: m.group(1) + flip[m.group(2)], original)

params.write_text(changed)
try:
    print("I changed drop_missing_sex in params.yaml. A different rule means different rows. dvc status says:\n")
    print(subprocess.run(["dvc", "status"], cwd=PROJECT, capture_output=True, text=True).stdout)
finally:
    params.write_text(original)
print("I put params.yaml back.")
