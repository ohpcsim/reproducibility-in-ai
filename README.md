# Reproducibility in AI: Software, Data, and Research Practice

Examples from the Rice Research Computing Day 2026 workshop. They show a GPU software environment two ways, conda and a container, then a data pipeline another person can restore, recompute and compare.

These ran on an NVIDIA DGX Spark (GB10, aarch64, Linux). `Dockerfile` and `explicit-linux-aarch64.txt` are specific to aarch64. On another platform, generate your own lock file, change the installer in the Dockerfile, and choose the `cuda-version` your driver and GPU support.

Copy the repository to a working folder first, so the commands match the ones on the slides:

```bash
mkdir -p ~/rice-runs && cp -r . ~/rice-runs/ && cd ~/rice-runs
```

You need conda. Miniforge is the installer the slides recommend.

## 1. Conda

```bash
conda env create -f environment.yml
conda list -n repro-gpu --explicit --md5 > my-lock.txt
conda run -n repro-gpu python verify_gpu.py
nvidia-smi --query-gpu=name,driver_version --format=csv; uname -r
```

`environment.yml` lists what you asked for. The lock file lists what was installed, for one platform. `verify_gpu.py` exits with an error if CUDA isn't available.

## 2. Container

This needs Docker and Apptainer. The Dockerfile builds from `explicit-linux-aarch64.txt`, with its base image pinned by digest and its installer pinned by version.

```bash
docker build -t repro-gpu:v1 .
apptainer build repro-gpu.sif docker-daemon://repro-gpu:v1
sha256sum repro-gpu.sif
apptainer exec --nv repro-gpu.sif python /opt/verify_gpu.py
```

Record the digest, the SIF hash, the kernel, the driver and the GPU.

## 3. DVC: restore, recompute, compare

A local bare Git repository and a local DVC store stand in for GitHub and object storage. To use an S3 service such as the Open Storage Network, add `dvc-s3` to `dvc-demo/environment.yml`, point the remote at your bucket, and keep credentials in `--local` config so they're never committed.

```bash
cd ~/rice-runs
git init --bare -b main origin.git && mkdir -p dvc-store
cd dvc-demo && conda env create -q -f environment.yml && conda activate repro-dvc
git init -b main && git remote add origin ~/rice-runs/origin.git
python scripts/make_data.py
dvc init
dvc add data/train data/val
dvc remote add -d storage ~/rice-runs/dvc-store
dvc stage add -n train -d data/train -d data/val -d train.py \
  -o model/model.json -M metrics.json python train.py
dvc repro
conda list -n repro-dvc --explicit --md5 > explicit-linux-aarch64.txt
git add .dvc .dvcignore data/*.dvc data/.gitignore model/.gitignore dvc.yaml dvc.lock metrics.json train.py scripts environment.yml explicit-linux-aarch64.txt
git commit -m "Pipeline, data pointers and baseline metrics"
git push origin main
dvc push
```

Now be the collaborator, with a fresh clone:

```bash
cd ~/rice-runs && git clone --branch main origin.git collab && cd collab
conda create -q -y -n repro-dvc-collab --file explicit-linux-aarch64.txt && conda activate repro-dvc-collab
dvc pull            # restore the recorded data and outputs
dvc repro --force   # recompute from scratch
dvc metrics diff    # compare with the committed metrics (no output means no change)
dvc metrics show
```

Then a negative control. A known-wrong input has to move the result:

```bash
sed -i '2s/.*/5.000000,999.000000/' data/val/data.csv
dvc repro
dvc metrics diff    # val_rmse must change
git checkout data/val.dvc dvc.lock metrics.json && dvc checkout   # back to the recorded data
```

`dvc stage add` warns that it couldn't create `model/.gitignore`, and `dvc repro` creates it. `dvc repro --force` suggests a `git add`, though `git status` stays clean. Both messages are harmless.

## License

MIT. See `LICENSE`.
