#!/bin/sh
# Build the site with every exercise notebook run untouched.
# Usage: ./build_site.sh <env of 01-environments> <env of 02-workflows> <env of 03-dataops> <env of 04-registry> <env of results>
# Each exercise env is its .binder/environment.yml plus ipykernel and jupyter_server.
# The results env is results/environment.yml plus jupyter_server.
# Run it from a clean copy, because running the notebooks writes project/ folders.
#
# Each notebook has to run in its own exercise environment: exercise 1's failure
# needs pandas to be missing, and the results page needs matplotlib. So each one builds
# alone first, as a one-page site. Jupyter Book caches the results by the
# notebook's code, under the one-page site's _build/execute. We copy them to the
# root's _build/execute, and the final strict build of the whole site reuses them.
set -eu
JUPYTER_BOOK=${JUPYTER_BOOK:-jupyter-book}
ROOT=$(pwd)
mkdir -p _build/execute

run_notebook() (
    cd "$2"
    # Without a site: section, jupyter-book prints "No site configuration found" and runs nothing.
    printf 'version: 1\nproject:\n  toc:\n    - file: %s\nsite:\n  template: book-theme\n' "$3" > myst.yml
    trap 'rm -rf myst.yml _build' EXIT
    PATH="$1/bin:$PATH" "$JUPYTER_BOOK" build --site --execute --strict
    cp _build/execute/* "$ROOT/_build/execute/"
)

run_notebook "$1" exercises/01-environments environments.ipynb
run_notebook "$2" exercises/02-workflows workflows.ipynb
run_notebook "$3" exercises/03-dataops dataops.ipynb
run_notebook "$4" exercises/04-registry registry.ipynb
run_notebook "$5" results results.ipynb
"$JUPYTER_BOOK" build --site --html --execute --strict
