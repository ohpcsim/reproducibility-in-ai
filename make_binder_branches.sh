#!/bin/sh
# Make each exercise's Binder branch from the committed site branch: the branch's
# files are the exercise folder, with that folder at the root, plus .binder/exercise.ipynb,
# the Binder panel's copy of the page, which tracks.py writes from the exercise's notebook.
# It only touches local branches. Push them yourself. Usage: ./make_binder_branches.sh [source-ref]
set -eu
source_ref=${1:-site}
tracks=$(mktemp)
trap 'rm -f "$tracks"' EXIT
for exercise in 01-environments 02-workflows 03-dataops 04-registry; do
    branch="binder-$exercise"
    page=${exercise#*-}
    git show "$source_ref:tracks.py" > "$tracks"
    panel=$(git show "$source_ref:exercises/$exercise/$page.ipynb" | python3 "$tracks" --panel "$page" | git hash-object -w --stdin)
    binder=$({ git ls-tree "$source_ref:exercises/$exercise/.binder"; printf '100644 blob %s\texercise.ipynb\n' "$panel"; } | git mktree)
    tree=$(git ls-tree "$source_ref:exercises/$exercise" | awk -v b="$binder" 'BEGIN { FS = OFS = "\t" } $2 == ".binder" { $1 = "040000 tree " b } 1' | git mktree)
    parent=$(git rev-parse --quiet --verify "refs/heads/$branch" || true)
    if [ -n "$parent" ] && [ "$(git rev-parse "$parent^{tree}")" = "$tree" ]; then
        echo "$branch: already up to date"
        continue
    fi
    commit=$(git commit-tree "$tree" ${parent:+-p "$parent"} -m "Exercise $exercise from $source_ref $(git rev-parse --short "$source_ref")" -m "$(git log -1 --format=%B "$source_ref")")
    git update-ref "refs/heads/$branch" "$commit"
    echo "$branch: $commit"
done
