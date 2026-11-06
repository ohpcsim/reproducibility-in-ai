#!/usr/bin/env bash
# Needs run/gpu.sh first, for gpu/lock.txt, plus Docker and Apptainer on this machine. Run from the repository folder.
set -euo pipefail

docker build -t repro-gpu:v1 gpu
docker save -o repro-gpu.tar repro-gpu:v1
apptainer build --force repro-gpu.sif docker-archive://repro-gpu.tar
sha256sum repro-gpu.sif
apptainer exec --nv repro-gpu.sif python /opt/verify_gpu.py
