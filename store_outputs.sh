#!/bin/sh
# Store real output in each exercise's notebook, so the Binder page reads correctly without running anything.
# Usage: ./store_outputs.sh <env of 01-environments> <env of 02-workflows> <env of 03-dataops> <env of 04-registry> <env of 05-llm>
# Each env is its exercise's .binder/environment.yml plus ipykernel and nbconvert. Commit the result.
set -eu

store() (
    cd "exercises/$2"
    PATH="$1/bin:$PATH" jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.timeout=600 "$3"
)

store "$1" 01-environments environments.ipynb
store "$2" 02-workflows workflows.ipynb
store "$3" 03-dataops dataops.ipynb
store "$4" 04-registry registry.ipynb
store "$5" 05-llm llm.ipynb
