#!/bin/sh
# Build the site with every exercise notebook run untouched.
# Usage: ./build_site.sh <env of 01-gitops> <env of 02-dataops> <env of 03-registry>
# Run it from a clean copy, because running the notebooks writes project/ folders.
#
# Each notebook has to run in its own exercise environment: exercise 1's failure
# needs pandas to be missing, and exercise 2 needs it present. So each one builds
# alone first, as a one-page project. Jupyter Book caches the results by the
# notebook's code, and the final strict build of the whole site reuses them.
set -eu
JUPYTER_BOOK=${JUPYTER_BOOK:-jupyter-book}

run_notebook() (
    cd "exercises/$2"
    printf 'version: 1\nproject:\n  toc:\n    - file: %s\n' "$3" > myst.yml
    trap 'rm -f myst.yml' EXIT
    PATH="$1/bin:$PATH" "$JUPYTER_BOOK" build --site --execute --strict
)

run_notebook "$1" 01-gitops gitops.ipynb
run_notebook "$2" 02-dataops dataops.ipynb
run_notebook "$3" 03-registry registry.ipynb
"$JUPYTER_BOOK" build --site --html --execute --strict
