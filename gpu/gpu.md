---
title: If you need a GPU
---

This page is optional, and none of the exercises need it. You run it yourself, on a Linux machine or WSL2 with an NVIDIA GPU. It won't work on a Mac, and there's no Binder for it, because Binder has no GPU.

An environment that installs isn't an environment that works. The usual trap is a CUDA build that doesn't match your GPU. It may install fine, then crash when it does real work, or quietly fall back to the CPU. So you check it the same way on every system.

The output on this page is a recording from real runs, labeled with the architecture and GPU. The machines that build this site have no GPU, so this page doesn't rerun when the site is published.

## What you need

You need [conda](../setup.md), an NVIDIA driver, and about 10 GB of free disk. On a cluster, do this on a GPU node, for example in a session from `srun --gpus=1 --pty bash`, because a login node has no driver for conda to look at. The flags vary by site.

Get the files:

```bash
git clone --depth 1 https://github.com/ohpcsim/reproducibility-in-ai.git
cd reproducibility-in-ai/gpu
```

## The check

If CUDA isn't there, this script exits with an error, so a setup that misses the GPU can't pass quietly. The seed makes the checksum comparable between routes on the same machine. `synchronize` makes the timer measure the GPU's work, and not just the time to queue it.

```{literalinclude} verify_gpu.py
:language: python
```

## The environment

This file doesn't name a CUDA version. Conda looks at your driver and your architecture, and picks a build they support. `pytorch-gpu` comes from conda-forge.

```{literalinclude} environment.yml
:language: yaml
```

Build it, write the lock, and run the check. The build took about a minute on our machines, and the environment is about 6 GB. The lock lists exactly what you got on this machine, so commit it to your own project, and write down the kernel, driver and GPU next to it.

```bash
conda env create --quiet --file environment.yml
conda list -n repro-gpu --explicit --md5 > lock.txt
conda run -n repro-gpu python verify_gpu.py
nvidia-smi --query-gpu=name,driver_version --format=csv
uname -m -r
```

## What it printed

You'll see your own versions and device. These two runs used the same file, and conda chose a build for each machine. Recorded November 7, 2026.

**aarch64, NVIDIA GB10, driver 580.178.04, Linux:**

```text
torch           2.14.1
cuda runtime    13.4
cuda available  True
device          NVIDIA GB10
capability      (12, 1)
matmul 4096^2   0.0607 s, checksum -4.8324e+05
host            Linux-7.0.0-1024-nvidia-aarch64-with-glibc2.39
```

**x86_64, NVIDIA GeForce RTX 3070, driver 610.74, WSL2:**

```text
torch           2.14.1
cuda runtime    13.4
cuda available  True
device          NVIDIA GeForce RTX 3070
capability      (8, 6)
matmul 4096^2   0.1214 s, checksum 3.7091e+04
host            Linux-5.15.167.4-microsoft-standard-WSL2-x86_64-with-glibc2.39
```

The checksums differ because these are different machines with different builds. Compare a checksum only between routes on the same machine. Each lock is good only for its own platform: the first says `linux-aarch64` and the second says `linux-64`, and the PyTorch builds in them are different files.

## If the check fails

Choose the CUDA version yourself. Run `nvidia-smi`, and add `- cuda-version=X.Y` to `environment.yml`, with the version it reports. Then start clean:

```bash
conda env remove --yes --name repro-gpu
conda env create --quiet --file environment.yml
conda list -n repro-gpu --explicit --md5 > lock.txt
conda run -n repro-gpu python verify_gpu.py
```

When you're done, `conda env remove --yes --name repro-gpu` gets the disk back. The environment is cattle, and your lock can rebuild it. If you need to carry it to another system, go on to [the container page](container.md).
