#!/usr/bin/env bash
# Everything from "First, software" through "Break it on purpose". Run from the repository folder.
set -euo pipefail
eval "$(conda shell.bash hook)"
rm -rf ~/repro-demo
conda env remove -y -n repro-dvc 2>/dev/null || true
conda env remove -y -n repro-dvc-stranger 2>/dev/null || true

mkdir -p ~/repro-demo && cp -r study ~/repro-demo/ && cd ~/repro-demo/study
conda env create -f environment.yml
conda activate repro-dvc
conda list -n repro-dvc --explicit --md5 > lock.txt
grep -E '^# platform|/numpy-[0-9]' lock.txt
git init -b main
git init --bare -b main ~/repro-demo/origin.git
git remote add origin ~/repro-demo/origin.git
python scripts/make_data.py
dvc init
dvc remote add -d storage ~/repro-demo/store
dvc add data/train data/val
dvc stage add -n train -d data/train -d data/val -d train.py \
  -o model/model.json -M metrics.json python train.py
dvc repro
cat metrics.json
git add .
git commit -m "Pipeline, data pointers and baseline metrics"
git push -u origin main
dvc push
cd ~/repro-demo
git clone --branch main origin.git stranger
cd stranger
conda create -y -n repro-dvc-stranger --file lock.txt
conda activate repro-dvc-stranger
dvc pull
dvc repro --force
dvc metrics diff
dvc metrics show
python scripts/break_one_row.py
dvc repro
dvc metrics diff
git checkout data/val.dvc dvc.lock metrics.json
dvc checkout
