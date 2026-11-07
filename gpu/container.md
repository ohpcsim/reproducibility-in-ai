---
title: If you need a container
---

This page is optional, and none of the exercises need it. You run it yourself, after [the GPU page](gpu.md), on the machine where the check passed, because the container is built from the lock you made there. There's no Binder for it.

A container carries your software to the next system. A tag such as `ubuntu:24.04` can move, and a sha256 digest can't, so this file pins the base image by digest and the installer by version. The digest is for a multi-architecture image, and Docker pulls the right one for your machine. `uname -m` picks the matching installer. The environment comes from your lock, so the container has exactly what you tested. You need about 20 GB of free disk.

```{literalinclude} Dockerfile
:language: dockerfile
```

To get a digest for another image, run `docker pull`, then `docker inspect --format '{{index .RepoDigests 0}}' IMAGE`.

## With Docker and Apptainer

Most HPC centers run Apptainer rather than Docker. So build with Docker on a machine you control, with the same architecture as your cluster, then save the image to one file. From the `gpu` folder, with your `lock.txt` in it:

```bash
docker build -t repro-gpu:v1 .
docker run --rm --gpus all repro-gpu:v1
docker save -o repro-gpu.tar repro-gpu:v1
```

`docker run --gpus all` needs NVIDIA's container toolkit on that machine. Copy `repro-gpu.tar` to your cluster and convert it to a SIF, a single file you can hash and move. Build one per architecture. On a GPU node, run the same check. The `--nv` flag brings in the host's NVIDIA driver, the one thing the container doesn't carry.

```bash
apptainer build --force repro-gpu.sif docker-archive://repro-gpu.tar
sha256sum repro-gpu.sif
apptainer exec --nv repro-gpu.sif python /opt/verify_gpu.py
```

Converting the same image twice gave SIFs with different hashes when we tried it. So the hash identifies one file, not the recipe. Keep the SIF you ran, or at least its hash.

**Recorded November 7, 2026, on aarch64, NVIDIA GB10, driver 580.178.04, Linux, with Apptainer 1.5.5.** The conda route on this machine gave the same checksum. That's the check, not the time.

```text
torch           2.14.1
cuda runtime    13.4
cuda available  True
device          NVIDIA GB10
capability      (12, 1)
matmul 4096^2   0.0962 s, checksum -4.8324e+05
host            Linux-7.0.0-1024-nvidia-aarch64-with-glibc2.39
```

## With Apptainer and no Docker

If you don't have Docker, this definition file does the same steps. It needs Apptainer's `--fakeroot`, which your center may or may not allow. From the `gpu` folder, with your `lock.txt` in it:

```{literalinclude} repro-gpu.def
```

```bash
apptainer build --fakeroot --force repro-gpu.sif repro-gpu.def
apptainer exec --nv repro-gpu.sif python /opt/verify_gpu.py
```

## On WSL2

On WSL2, `--nv` alone doesn't reach the GPU. WSL2 exposes it differently, through `/dev/dxg` and `/usr/lib/wsl`, and there's no `/dev/nvidia0`. Here's what the check printed, which is why the check exists:

**Recorded November 7, 2026, on x86_64, NVIDIA GeForce RTX 3070, driver 610.74, WSL2, with Apptainer 1.4.5:**

```text
torch           2.14.1
cuda runtime    13.4
cuda available  False
FAIL: CUDA is not available; this route did not reach the GPU
```

Bind WSL2's library folder instead, and point the container at it:

```bash
apptainer exec --bind /usr/lib/wsl --env LD_LIBRARY_PATH=/usr/lib/wsl/lib repro-gpu.sif python /opt/verify_gpu.py
```

**The same machine, with that command.** The conda route on this machine gave the same checksum.

```text
torch           2.14.1
cuda runtime    13.4
cuda available  True
device          NVIDIA GeForce RTX 3070
capability      (8, 6)
matmul 4096^2   0.1312 s, checksum 3.7091e+04
host            Linux-5.15.167.4-microsoft-standard-WSL2-x86_64-with-glibc2.39
```

## What we ran where

| Step | aarch64, GB10, Linux | x86_64, RTX 3070, WSL2 |
|---|---|---|
| `docker build`, `docker run --gpus all`, `docker save` | Ran, and passed | Not run, because this machine has no Docker |
| `apptainer build` from `docker-archive://` | Ran, and passed | Not run, because it needs the Docker file |
| `apptainer build --fakeroot` from `repro-gpu.def` | Ran, and passed | Ran, and passed |
| `apptainer exec --nv` | Passed | Failed, as shown above |
| `apptainer exec --bind /usr/lib/wsl` | Not needed | Passed |

So the `docker-archive://` route has only run on aarch64. We expect it to work on x86_64 too, because the Dockerfile picks its installer with `uname -m` and the base image's digest covers both architectures, but we haven't run it there.

When you're done, remove what you made. `docker rmi repro-gpu:v1` removes the image, and `rm repro-gpu.tar repro-gpu.sif` removes the files.
