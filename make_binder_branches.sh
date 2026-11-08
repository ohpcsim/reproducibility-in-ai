#!/bin/sh
# Make each exercise's Binder branch from the committed site branch: the branch's
# files are exactly the exercise folder, with that folder at the root.
# It only touches local branches. Push them yourself. Usage: ./make_binder_branches.sh [source-ref]
set -eu
source_ref=${1:-site}
for exercise in 01-gitops 02-workflows 03-dataops 04-registry 05-llm; do
    branch="binder-$exercise"
    tree=$(git rev-parse "$source_ref:exercises/$exercise")
    parent=$(git rev-parse --quiet --verify "refs/heads/$branch" || true)
    if [ -n "$parent" ] && [ "$(git rev-parse "$parent^{tree}")" = "$tree" ]; then
        echo "$branch: already up to date"
        continue
    fi
    commit=$(git commit-tree "$tree" ${parent:+-p "$parent"} -m "Exercise $exercise from $source_ref $(git rev-parse --short "$source_ref")" -m "$(git log -1 --format=%B "$source_ref")")
    git update-ref "refs/heads/$branch" "$commit"
    echo "$branch: $commit"
done
