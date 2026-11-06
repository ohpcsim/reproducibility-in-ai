"""Negative control: overwrite the first validation row with a known-wrong value."""
import pathlib

path = pathlib.Path("data/val/data.csv")
lines = path.read_text().splitlines(keepends=True)
lines[1] = "5.000000,999.000000\n"
path.write_text("".join(lines))
