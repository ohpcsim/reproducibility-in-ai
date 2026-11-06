#!/usr/bin/env bash
# Needs an NVIDIA GPU. Run from the repository folder.
set -euo pipefail
eval "$(conda shell.bash hook)"
conda env remove -y -n repro-gpu 2>/dev/null || true

conda env create -f gpu/environment.yml
conda list -n repro-gpu --explicit --md5 > gpu/lock.txt
conda run -n repro-gpu python gpu/verify_gpu.py
nvidia-smi --query-gpu=name,driver_version --format=csv
uname -m -r
