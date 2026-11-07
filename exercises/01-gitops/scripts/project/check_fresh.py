"""Does the staged metrics.json match a rerun? Exit 0 if yes, 1 if no.

Git stores what you stage, so this reads the staged files, not your working copy.
"""
import json
import subprocess
import sys

import yaml

import trend


def staged(path):
    return subprocess.run(["git", "show", f":{path}"], capture_output=True, check=True).stdout


t, ppm = trend.load_table(staged("data/co2_mm_mlo.csv"))
rerun = trend.summarize(t, ppm, yaml.safe_load(staged("params.yaml")))
committed = json.loads(staged("metrics.json"))

stale = {k: (committed.get(k), v) for k, v in rerun.items() if committed.get(k) is None or abs(committed[k] - v) > 0.002}
if stale:
    print("STALE: metrics.json does not match a rerun of params.yaml and the data.")
    for key, (old, new) in stale.items():
        print(f"  {key}: metrics.json says {old}, a rerun gives {new}")
    sys.exit(1)
print("Fresh: metrics.json matches a rerun.")
