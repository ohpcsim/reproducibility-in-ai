#!/usr/bin/env python3
"""Write each track's pages from one source per page, then check them.

A track is the machine a learner is on. Each page's source holds every track's text.
A notebook cell, or a block of a .md page that starts with a line such as
+++ {"tags": ["track-mac", "track-linux"]}, belongs to the tracks it names. Untagged cells
and blocks go to every track of the page. "site-only" keeps a Binder cell out of the
Binder panel, and "panel-only" puts a cell only in the panel.

The first track listed for a page keeps the source's file name, so its URL doesn't change.
The others get <name>-<track> next to it. Labels such as (build-apptainer)= get -<track> on
those copies, because MyST labels are site-wide.

Usage:
  tracks.py                     write every track's pages into this tree. It overwrites the
                                sources with their first track's copy, so run it only in a
                                build copy, as build_site.sh does in CI.
  tracks.py --panel NAME < NB   print the Binder panel's notebook for exercise notebook NAME.ipynb.
"""
import json
import re
import sys
from pathlib import PurePosixPath as P
from posixpath import normpath, relpath

TRACKS = {
    "binder": "Binder",
    "mac": "Your Mac",
    "linux": "Your Linux machine",
    "wsl2": "Windows (WSL2)",
    "hpc": "Shared Linux or HPC",
}
ALL = list(TRACKS)
OWN = ["mac", "linux", "wsl2", "hpc"]
PAGES = {
    "setup.md": ALL,
    "exercises/01-environments/environments.ipynb": ALL,
    "exercises/01-environments/containers.md": ["linux", "mac", "wsl2", "hpc"],
    "gpu/gpu.md": ["linux", "wsl2", "hpc"],
    "gpu/container.md": ["linux", "wsl2", "hpc"],
    "exercises/02-workflows/workflows.ipynb": ALL,
    "exercises/02-workflows/nextflow.md": ["linux", "mac", "wsl2", "hpc"],
    "exercises/03-dataops/dataops.ipynb": ALL,
    "exercises/04-registry/registry.ipynb": ALL,
}
OURS = {"site-only", "panel-only"} | {f"track-{t}" for t in TRACKS}
DONE = "Wrong machine? Pick another"
LINK = re.compile(r"\]\((?![a-z]+:)([^)\s#]*)(#[^)\s]*)?\)")
LABEL = re.compile(r"^\(([\w-]+)\)=$", re.M)
SPLIT = re.compile(r"^\+\+\+[ \t]*(\{.*\})?[ \t]*$")


def page_path(src, track):
    if track == PAGES[src][0]:
        return src
    p = P(src)
    return str(p.with_name(f"{p.stem}-{track}{p.suffix}"))


def tracks_of(tags, src):
    named = [t[6:] for t in tags if t.startswith("track-")]
    for t in named:
        assert t in TRACKS, f"{src}: unknown tag track-{t}"
    return named or PAGES[src]


def read(src, text=None):
    """Return (frontmatter, cells). A cell is a dict with cell_type, source as one string, and tags."""
    text = open(src, encoding="utf-8").read() if text is None else text
    assert DONE not in text, f"{src} is already a generated page. Run this in a fresh copy."
    if src.endswith(".ipynb"):
        nb = json.loads(text)
        for c in nb["cells"]:
            c["source"] = "".join(c["source"])
            c["tags"] = c.get("metadata", {}).get("tags", [])
        return nb, nb["cells"]
    front, body = re.match(r"((?:---\n.*?\n---\n)?)(.*)", text, re.S).groups()  # setup.md has none: each track has its own title
    cells, lines, tags, fence = [], [], [], False
    for line in body.split("\n"):
        if line.startswith("```"):
            fence = not fence
        m = None if fence else SPLIT.match(line)
        if m:
            cells.append({"cell_type": "markdown", "source": "\n".join(lines).strip("\n"), "tags": tags})
            lines, tags = [], json.loads(m[1]).get("tags", []) if m[1] else []
        else:
            lines.append(line)
    cells.append({"cell_type": "markdown", "source": "\n".join(lines).strip("\n"), "tags": tags})
    return front, [c for c in cells if c["source"]]


def relink(text, src, track, labels):
    """Point links at this track's copy of each page, and add -<track> to its labels."""
    def link(m):
        path, anchor = m[1], m[2] or ""
        target = normpath(str(P(src).parent / path)) if path else src
        if target in PAGES:
            assert track in PAGES[target], f"{src} ({track}): links to {target}, which isn't in this track"
            if anchor[1:] in labels.get(target, ()) and track != PAGES[target][0]:
                anchor += f"-{track}"
            if path:
                path = relpath(page_path(target, track), str(P(src).parent))
        return f"]({path}{anchor})"
    text = LINK.sub(link, text)
    if track != PAGES[src][0]:
        text = LABEL.sub(lambda m: f"({m[1]}-{track})=", text)
    return text


def select(cells, src, track, panel=False):
    """The cells of one track, or of the Binder panel, in order."""
    out = []
    for c in cells:
        if c["cell_type"] == "code":
            assert not OURS & set(c["tags"]), f"{src}: code cells go to every track, so every copy shares one execution cache"
            out.append(c)
        elif track in tracks_of(c["tags"], src) and ("site-only" if panel else "panel-only") not in c["tags"]:
            out.append(c)
    return out


def first_line(src, track):
    up = "../" * src.count("/")
    return f"Track: {TRACKS[track]}. [{DONE}]({up}index.md#pick-your-machine)"


def with_line(cells, line, tags):
    """Put the line right under the page's title."""
    new = {"cell_type": "markdown", "id": f"{cells[0].get('id')}-track", "metadata": {}, "source": line, "tags": tags}
    if cells[0]["source"].startswith("# "):
        title, _, rest = cells[0]["source"].partition("\n")
        cells = [{**cells[0], "id": f"{cells[0].get('id')}-title", "source": title}, new,
                 {**cells[0], "source": rest.strip("\n")}] + cells[1:]
    else:
        cells = [new] + cells
    return [c for c in cells if c["source"] or c["cell_type"] == "code"]


def dump_nb(nb, cells):
    out = []
    for c in cells:
        meta = dict(c.get("metadata", {}))
        tags = [t for t in meta.pop("tags", []) if t not in OURS]
        c = {**{k: v for k, v in c.items() if k != "tags"}, "metadata": {**meta, "tags": tags} if tags else meta,
             "source": c["source"].splitlines(keepends=True)}
        out.append(c)
    return json.dumps({**nb, "cells": out}, indent=1, ensure_ascii=False) + "\n"


def write(src, track, front, cells, labels):
    cells = with_line(select(cells, src, track), first_line(src, track), ["site-only"] if track == "binder" else [])
    cells = [{**c, "source": relink(c["source"], src, track, labels)} if c["cell_type"] == "markdown" else c for c in cells]
    dest = page_path(src, track)
    if src.endswith(".ipynb"):
        # Cell IDs become site-wide identifiers too. The execution cache keys on code only, so the copies still share it.
        if track != PAGES[src][0]:
            cells = [{**c, "id": f"{c['id']}-{track}"} for c in cells]
        text = dump_nb(front, cells)
    else:
        text = relink(front, src, track, labels) + "\n" + "\n\n".join(c["source"] for c in cells) + "\n"
    open(dest, "w", encoding="utf-8").write(text)
    return dest, text


def build():
    sources = {src: read(src) for src in PAGES}
    labels = {src: set(LABEL.findall("\n".join(c["source"] for c in cells))) for src, (_, cells) in sources.items()}
    for src, (front, cells) in sources.items():
        pages = {t: write(src, t, front, cells, labels)[1] for t in PAGES[src]}
        for c in cells:
            if c["cell_type"] == "code":
                continue
            homes = [t for t in tracks_of(c["tags"], src) if t in PAGES[src]]
            assert homes, f"{src}: a cell lands in no track: {c['source'][:80]!r}"
            assert "panel-only" not in c["tags"] or homes == ["binder"], f"{src}: a panel-only cell must be for Binder only"
            for t in PAGES[src]:
                if t not in homes:
                    kept = "\n".join(x["source"] for x in select(cells, src, t))
                    text = c["source"].strip()
                    if text not in kept:
                        assert text not in pages[t], f"{page_path(src, t)} has another track's cell: {text[:80]!r}"
        print(f"{src}: {', '.join(page_path(src, t) for t in PAGES[src])}")


ANSI = re.compile(r"\x1b\[[0-9;]*m")
STEP = re.compile(r"^(## Step |[2-9]\. |1[0-9]\. )")


def panel_markdown(text):
    """Label each command block and put a rule before each step, so steps don't run together in the Markdown Preview."""
    out, fence, prev = [], False, ""
    for line in text.split("\n"):
        if not fence and line.lstrip().startswith("```bash"):
            out += [line[:len(line) - len(line.lstrip())] + "**Run:**", ""]
        elif not fence and STEP.match(line) and not re.match(r"\d+\. ", prev):
            out += ["---", ""]  # after a blank line, so it can't turn the line above into a heading
        if line.lstrip().startswith("```"):
            fence = not fence
        out.append(line)
        if line.strip():
            prev = line
    return "\n".join(out)


def recorded(cell):
    """A recorded output, as a labelled text block in a markdown cell, without the code that printed it."""
    text = ANSI.sub("", "".join("".join(o.get("text", "")) for o in cell.get("outputs", []))).rstrip()
    ticks = "````" if "```" in text else "```"
    return {"cell_type": "markdown", "id": cell.get("id"), "metadata": {}, "tags": [],
            "source": f"**Recorded output:**\n\n{ticks}text\n{text}\n{ticks}"}


def panel(name):
    src = f"exercises/{name}.ipynb"
    PAGES[src] = ALL
    nb, cells = read(src, sys.stdin.read())
    cells = with_line(select(cells, src, "binder", panel=True), f"This is the Binder copy of [the full page]({name}.ipynb).", [])
    # Every code cell on these pages is a recorded output. The panel shows it as text; the site keeps its output area.
    for c in cells:
        assert c["cell_type"] == "markdown" or "Recorded output" in c["source"], f"{src}: a code cell that isn't a recorded output"
    cells = [recorded(c) if c["cell_type"] == "code" else {**c, "source": panel_markdown(c["source"])} for c in cells]
    sys.stdout.write(dump_nb(nb, cells))


if __name__ == "__main__":
    if sys.argv[1:2] == ["--panel"]:
        panel(sys.argv[2])
    else:
        build()
