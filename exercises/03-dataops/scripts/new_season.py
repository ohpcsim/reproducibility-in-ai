#!/usr/bin/env python3
"""Deliver the 2008 and 2009 field seasons: replace project/data/penguins.csv with all three seasons."""
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
shutil.copyfile(HERE / ".exercise" / "data" / "penguins.csv", HERE / "project" / "data" / "penguins.csv")
print("Delivered 344 rows to project/data/penguins.csv, covering 2007 to 2009.")
