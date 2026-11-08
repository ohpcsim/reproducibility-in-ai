#!/usr/bin/env python3
"""Run tests/ over every recorded card, and print one line per card."""
import os
import re
import subprocess
import sys
from pathlib import Path

rejected = 0
for card in sorted(Path("runs").glob("*/card.md")):
    done = subprocess.run([sys.executable, "-m", "pytest", "-q", "--tb=no", "--color=no", "-p", "no:cacheprovider", "tests"],
                          env={**os.environ, "CARD": str(card)}, capture_output=True, text=True)
    failed = re.findall(r"^FAILED \S*::(\S+)", done.stdout, re.M)
    print(f"{card.parent.name:32} {'PASS' if done.returncode == 0 else 'FAIL'}  {' '.join(failed)}")
    rejected += done.returncode != 0
print(f"\n{rejected} rejected.")
