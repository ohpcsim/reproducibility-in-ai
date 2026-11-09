---
title: 1c. PyTorch with a GPU
---

- This is part 1c of [Exercise 1](../exercises/01-environments/environments.ipynb). It's optional, and none of the other exercises need it.
+++ {"tags": ["track-linux"]}

- You run it yourself, on your Linux machine with an NVIDIA GPU.

+++ {"tags": ["track-wsl2"]}

- You run it yourself, in WSL2 with an NVIDIA GPU.

+++ {"tags": ["track-hpc"]}

- You run it yourself, on a GPU node with an NVIDIA GPU.

+++

- There's no Binder for it, because Binder has no GPU.
- The output on this page is a recording from real runs, labeled with the machine, architecture, GPU and driver.
- The machines that build this site have no GPU, so this page doesn't rerun when the site is published.

## Learning objectives

- Install PyTorch with CUDA three ways: with conda, with uv, and in a container.
- Check each route with the same script, which fails if it can't reach the GPU.
- Choose a route for your own project.

## The problem

- A CUDA build can install and still fail to reach the GPU.
- The usual trap is a CUDA build that doesn't match your GPU or your driver.
- It may install fine, then crash when it does real work, or quietly fall back to the CPU.
- So you check it the same way on every route.

## What you'll do

1. Step 1, conda: build the environment from `environment.yml`, write the lock and run the check.
2. Step 2, uv: sync the environment from `uv.lock` and run the check.
3. Step 3, containers: carry the conda lock into a container, on [the container page](container.md).

- Steps 1 and 2 take a few minutes each, mostly downloading. Step 3 takes longer.
- Each environment uses 5 to 6 GB of disk.

## What you need

- An NVIDIA GPU, and its driver, already installed. No route here installs the driver.
- `nvidia-smi` prints your driver version, and the newest CUDA version it supports, at the top right.
- [conda](../setup.md) for step 1, [uv](../setup.md#install-uv) for step 2, and about 15 GB of free disk for both.
+++ {"tags": ["track-hpc"]}

- On a cluster, do this on a GPU node, for example in a session from `srun --gpus=1 --pty bash`, because a login node has no GPU driver. The flags vary by site.
- The GPU node needs network access for the clone and the installs.
- We haven't run this on an HPC cluster. The recorded runs are from a DGX Spark and a Windows PC with WSL2.

+++

Get the files:

```bash
git clone --depth 1 https://github.com/ohpcsim/reproducibility-in-ai.git repro-gpu
cd repro-gpu/gpu
```

## The check

- If CUDA isn't there, this script exits with an error, so a setup that misses the GPU can't pass quietly.
- The seed makes the checksum comparable between routes on the same machine.
- `synchronize` makes the timer measure the GPU's work, and not just the time to queue it.

```{literalinclude} verify_gpu.py
:language: python
```

## Step 1: conda

**Problem:** you need PyTorch built for your GPU, with CUDA libraries that match your driver.

**Facts**

- `pytorch-gpu` comes from conda-forge, and it brings the CUDA libraries as conda packages.
- This file doesn't name a CUDA version. Conda looks at your driver and your architecture, and picks a build they support.
- The lock lists exactly what you got on this machine. It covers one platform, so each platform needs its own lock.

```{literalinclude} environment.yml
:language: yaml
```

**Steps**

- Build it, write the lock, and run the check.
- The build took about a minute on our machines, and the environment is about 6 GB.
- Commit the lock to your own project, and write down the kernel, driver and GPU next to it.

```bash
conda env create --quiet --file environment.yml
conda list -n repro-gpu --explicit --md5 > lock.txt
conda run -n repro-gpu python verify_gpu.py
nvidia-smi --query-gpu=name,driver_version --format=csv
uname -m -r
```

You'll see your own versions and device. Recorded November 7, 2026, and the same on aarch64 when we ran it again on November 8:

**NVIDIA DGX Spark: aarch64, NVIDIA GB10, driver 580.178.04, Ubuntu 24.04:**

```text
torch           2.14.1
cuda runtime    13.4
cuda available  True
device          NVIDIA GB10
capability      (12, 1)
matmul 4096^2   0.0607 s, checksum -4.8324e+05
host            Linux-7.0.0-1024-nvidia-aarch64-with-glibc2.39
```

**Windows PC with WSL2: x86_64, NVIDIA GeForce RTX 3070, driver 610.74, Ubuntu 24.04:**

```text
torch           2.14.1
cuda runtime    13.4
cuda available  True
device          NVIDIA GeForce RTX 3070
capability      (8, 6)
matmul 4096^2   0.1214 s, checksum 3.7091e+04
host            Linux-5.15.167.4-microsoft-standard-WSL2-x86_64-with-glibc2.39
```

- The checksums differ because these are different machines with different builds.
- Compare a checksum only between routes on the same machine.
- Each lock is good only for its own platform. The first says `linux-aarch64` and the second says `linux-64`, and the PyTorch builds in them are different files.

If the check fails, choose the CUDA version yourself. Add `- cuda-version=X.Y` to `environment.yml`, with the version `nvidia-smi` reports, and start clean:

```bash
conda env remove --yes --name repro-gpu
conda env create --quiet --file environment.yml
conda list -n repro-gpu --explicit --md5 > lock.txt
conda run -n repro-gpu python verify_gpu.py
```

## Step 2: uv

**Problem:** the same PyTorch with CUDA, from Python packages only, with one lock for every platform.

**Facts**

- On PyPI, `torch` for Linux comes with one CUDA version, which PyTorch picks for each release.
- PyTorch's own index, `download.pytorch.org`, has one index per CUDA version, so you pick. `cu130` is CUDA 13.0.
- `[[tool.uv.index]]` names that index. `explicit = true` means uv uses it only for packages that point to it.
- `[tool.uv.sources]` points `torch` at that index on Linux. On macOS and Windows, `torch` comes from PyPI, and it has no CUDA there.
- The wheels carry the CUDA runtime libraries, as `nvidia-*` packages such as `nvidia-cuda-runtime` and `nvidia-cublas`. They don't carry the driver.
- The CUDA 13.0 build needs driver 580 or newer. Its x86_64 wheel has code for compute capability 7.5 and up, and its aarch64 wheel for 8.0 and up. The GB10, at 12.1, runs the 12.0 code.
- `numpy` is there because `torch` warns when it's missing.
- This follows [uv's PyTorch guide](https://docs.astral.sh/uv/guides/integration/pytorch/). [PyTorch's install page](https://pytorch.org/get-started/locally/) lists the CUDA builds.

```{literalinclude} pyproject.toml
:language: toml
```

- `uv.lock` is one file, with entries for each platform. It has two `torch` entries.
- On Linux it's `2.14.1+cu130` from PyTorch's index, with one wheel for x86_64 and one for aarch64.
- On macOS and Windows it's `2.15.0` from PyPI, with one wheel for Apple silicon and one for Windows on x86_64. PyTorch's `cu130` index stops at 2.14.1.
- So the same lock gives different `torch` versions on Linux and on a Mac.

**Steps**

- `uv lock` keeps the versions in the committed `uv.lock` unless you changed `pyproject.toml`.
- `uv sync --locked` builds `.venv` from the lock, and stops if the lock doesn't match `pyproject.toml`.
- `python-preference = "only-managed"` and `.python-version` make uv download Python 3.12.12 itself, as in Exercises 2 to 4, rather than use a Python on your system.

```bash
uv lock
uv sync --locked
uv run --locked python verify_gpu.py
```

- With an empty uv cache, the sync downloaded 3.2 GB on aarch64 and 3.0 GB on x86_64, in about 30 seconds on each machine. Your network sets the time.
- `.venv` is about 5 GB, and uv's cache holds the same files. When the cache and the project are on the same file system, uv hardlinks the files, and the two took 5.3 GB together on WSL2's ext4. On different file systems, uv copies the files, and the two take about 10 GB.
- On aarch64, every `uv sync` and `uv run` prints `Uninstalled 1 package` and `Installed 1 package`. That's `nvidia-cusparselt-cu13`, whose wheel has a platform tag, `manylinux2014_sbsa`, that uv doesn't match to the installed copy. It takes a few milliseconds, and the check still passes.

Recorded November 8, 2026, with uv 0.12.11, Python 3.12, and the `uv.lock` in this folder. Your uv version may be newer:

**NVIDIA DGX Spark: aarch64, NVIDIA GB10, driver 580.178.04, Ubuntu 24.04:**

```text
torch           2.14.1+cu130
cuda runtime    13.0
cuda available  True
device          NVIDIA GB10
capability      (12, 1)
matmul 4096^2   0.1274 s, checksum -4.8324e+05
host            Linux-7.0.0-1024-nvidia-aarch64-with-glibc2.39
```

**Windows PC with WSL2: x86_64, NVIDIA GeForce RTX 3070, driver 610.74, Ubuntu 24.04:**

```text
torch           2.14.1+cu130
cuda runtime    13.0
cuda available  True
device          NVIDIA GeForce RTX 3070
capability      (8, 6)
matmul 4096^2   0.0876 s, checksum 3.7091e+04
host            Linux-5.15.167.4-microsoft-standard-WSL2-x86_64-with-glibc2.39
```

- On each machine, the checksum matches the conda route's.
- The CUDA runtime is 13.0 here and 13.4 with conda. The two routes chose different CUDA builds of the same PyTorch version.
- The time varies from run to run. The checksum is the check.

If the check fails:

- If `nvidia-smi` reports a CUDA version below 13.0, or your GPU's capability is below what the wheel has code for, use the `cu126` index.
- Change `cu130` to `cu126` in both places in `pyproject.toml`, then run `uv lock`, `uv sync --locked` and the check again.

## Step 3: containers

- A container carries the whole stack, apart from the driver, to the next system.
- [The container page](container.md) builds an Apptainer SIF from your conda lock with a `.def` file, and runs the same check inside.
+++ {"tags": ["track-wsl2"]}

- On WSL2, Apptainer's `--nv` doesn't reach the GPU. [The WSL2 section](container.md#on-wsl2) has the fix, `--bind /usr/lib/wsl`.
+++

## Which to use

- Use conda when you need CUDA and system libraries managed as packages. Lock each platform.
- Use uv when the machine's driver is right and you only need Python packages. One lock covers every platform, with per-platform entries inside it.
- Use a container to carry the whole stack to a cluster. Build it from a lock, and record the SIF's hash.

| Route | aarch64, GB10, Linux | x86_64, RTX 3070, WSL2 |
|---|---|---|
| conda | Passed | Passed |
| uv | Passed | Passed |
| Containers | See [what we ran where](container.md#gpu-what-we-ran-where) | See [what we ran where](container.md#gpu-what-we-ran-where) |

## When you're done

- The environments are cattle, and your locks can rebuild them.
- `conda env remove --yes --name repro-gpu` removes the conda environment.
- `rm -rf .venv` removes the uv environment. `uv cache dir` shows where uv keeps its downloads, and `uv cache clean` empties that cache for every project.
- `cd ../.. && rm -rf repro-gpu` removes the clone.
