#!/bin/sh
# Store real output in each exercise's notebook, so the Binder page reads correctly without running anything.
# Usage: ./store_outputs.sh <env of 01-gitops> <env of 02-dataops> <env of 03-registry> <env of 04-llm>
# Each env is its exercise's .binder/environment.yml plus ipykernel and nbconvert. Commit the result.
set -eu

store() (
    cd "exercises/$2"
    PATH="$1/bin:$PATH" jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.timeout=600 "$3"
)

store "$1" 01-gitops gitops.ipynb
store "$2" 02-dataops dataops.ipynb
store "$3" 03-registry registry.ipynb
store "$4" 04-llm llm.ipynb
