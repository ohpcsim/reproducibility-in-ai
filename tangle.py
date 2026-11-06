#!/usr/bin/env python3
"""Extract the files in this repository from README.md. --check compares and writes nothing."""
import pathlib
import re
import sys

blocks = re.findall(r"^(?:<!-- ([^\n]+) -->\n)?`{3}\w*\n(.*?)^`{3}$", pathlib.Path("README.md").read_text(), re.M | re.S)
chunks, files = {}, []
for marker, block in blocks:
    head, _, rest = block.partition("\n")
    head, body = (marker, block) if marker else (head.removeprefix("# "), rest)
    match = re.fullmatch(r"file: (.+)|<<(.+)>>=", head)
    if match:
        name = match[1] or match[2]
        files += [name] if match[1] else []
        chunks.setdefault(name, []).append(body)


def expand(name):
    out = []
    for line in "".join(chunks[name]).splitlines(keepends=True):
        ref = re.fullmatch(r"<<(.+)>>\n?", line)
        out.append(expand(ref[1]) if ref else line)
    return "".join(out)


stale = []
for name in files:
    path, text = pathlib.Path(name), expand(name)
    if "--check" in sys.argv:
        if not path.exists() or path.read_text() != text:
            stale.append(name)
    else:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
print(f"{len(files)} files, {len(stale)} out of date: {stale}" if "--check" in sys.argv else f"wrote {len(files)} files")
sys.exit(1 if stale else 0)
