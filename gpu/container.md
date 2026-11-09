---
title: If you need a container
---

- This is step 3 of [1c, PyTorch with a GPU](gpu.md). It's optional, and none of the other exercises need it.
- You run it yourself, after step 1 there, on the machine where the check passed, because the container is built from the conda lock you made there.
- There's no Binder for it.

- A container carries your software to the next system.
- The environment comes from your lock, so the container has exactly what you tested.
- You need about 20 GB of free disk.

## The recipe

- Apptainer builds the image from its own recipe, a `.def` file, into one SIF file.
+++ {"tags": ["track-linux", "track-wsl2"]}

- [1b](../exercises/01-environments/containers.md) builds with Podman from Dockerfiles on the Mac, Linux and WSL2 tracks. A `.def` and a Dockerfile declare the same steps for two different tools, and our runs show they give the same results.

+++ {"tags": ["track-hpc"]}

- [1b](../exercises/01-environments/containers.md) builds the same way, with Apptainer from `.def` files.

+++

- A tag such as `ubuntu:24.04` can move, and a sha256 digest can't, so `repro-gpu.def` pins the base image by digest and the installer by version.
- The digest is for a multi-architecture image, and Apptainer pulls the right one for your machine.
- `uname -m` picks the matching installer.

`repro-gpu.def`:

```{literalinclude} repro-gpu.def
```

- To get the digest for another image, pull it on a machine with Podman, then print its digest:

```bash
podman pull docker.io/library/ubuntu:24.04
podman inspect --format '{{.Digest}}' docker.io/library/ubuntu:24.04
```

- With Podman 4.9.3 on our ARM machine, that printed `sha256:fe81560990fae86dc4743202b2cb4d3df98d0bcf949173cecef15ce1127ef852`, the digest in `repro-gpu.def`. Pin that digest. It covers every platform.
- Don't use `podman inspect --format '{{index .RepoDigests 0}}'`. On the same machine it printed a different digest, for the ARM image only.

(gpu-build-apptainer)=
## Build and run with Apptainer

+++ {"tags": ["track-hpc"]}

- The build needs Apptainer's `--fakeroot`, which your center may or may not allow. If it doesn't, build the SIF on a machine where it works, with the same architecture as the cluster, and copy it over.

+++ {"tags": ["track-linux", "track-wsl2"]}

- The build uses Apptainer's `--fakeroot`.

+++

- Build one SIF per architecture.

From the `gpu` folder, with your `lock.txt` in it:

```bash
apptainer build --fakeroot --force repro-gpu.sif repro-gpu.def
sha256sum repro-gpu.sif
```

+++ {"tags": ["track-linux", "track-hpc"]}

Run the check:

```bash
apptainer exec --nv repro-gpu.sif python /opt/verify_gpu.py
```

- The `--nv` flag brings in the host's NVIDIA driver, the one thing the container doesn't carry.

+++ {"tags": ["track-hpc"]}

- On a cluster, run the check on a GPU node.

+++ {"tags": ["track-wsl2"]}

Run the check:

```bash
apptainer exec --bind /usr/lib/wsl --env LD_LIBRARY_PATH=/usr/lib/wsl/lib repro-gpu.sif python /opt/verify_gpu.py
```

- On WSL2, `--nv` alone doesn't reach the GPU. [On WSL2](#on-wsl2) shows why.

+++

- Every build stamps a new ID and build time into the SIF, so the hash changes each time.
- Optional: with Apptainer 1.5 or newer, add `--reproducible` to `apptainer build`. Apptainer 1.4 doesn't have it.
- `--reproducible` gave the same sha256 twice for 1b's small uv image. For this image, two builds still gave different hashes, because files such as the apt and dpkg logs, conda's history and the ldconfig cache change on every build.
- Either way, record the `sha256sum` of the SIF you run.
+++ {"tags": ["track-linux", "track-hpc"]}

- **Recorded November 8, 2026, on aarch64, NVIDIA GB10, Linux, with Apptainer 1.5.5.** The check passed with torch 2.14.1 and CUDA runtime 13.4, and printed checksum -4.8324e+05, the same as the conda route on this machine.
- The build took 75 s and made a 3.9 GB SIF.

+++ {"tags": ["track-hpc"]}

- We haven't run this on an HPC cluster. The recorded runs are from one DGX Spark.

+++ {"tags": ["track-wsl2"]}

(on-wsl2)=
## On WSL2

- On WSL2, `--nv` alone doesn't reach the GPU.
- WSL2 exposes it differently, through `/dev/dxg` and `/usr/lib/wsl`, and there's no `/dev/nvidia0`.

Here's what the check printed, which is why the check exists:

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

- **The same machine, with that command.** The conda route on this machine gave the same checksum.

```text
torch           2.14.1
cuda runtime    13.4
cuda available  True
device          NVIDIA GeForce RTX 3070
capability      (8, 6)
matmul 4096^2   0.1312 s, checksum 3.7091e+04
host            Linux-5.15.167.4-microsoft-standard-WSL2-x86_64-with-glibc2.39
```

+++

(gpu-what-we-ran-where)=
## What we ran where

+++ {"tags": ["track-linux", "track-hpc"]}

| Step | aarch64, GB10, Linux |
|---|---|
| `apptainer build --fakeroot` from `repro-gpu.def` | Ran, and passed. Apptainer 1.5.5, 75 s, 3.9 GB SIF |
| `apptainer exec --nv` | Passed |
| `apptainer build --reproducible`, twice | The hashes differed |

+++ {"tags": ["track-wsl2"]}

| Step | aarch64, GB10, Linux | x86_64, RTX 3070, WSL2 |
|---|---|---|
| `apptainer build --fakeroot` from `repro-gpu.def` | Ran, and passed. Apptainer 1.5.5, 75 s, 3.9 GB SIF | Ran, and passed. Apptainer 1.4.5 |
| `apptainer exec --nv` | Passed | Failed, as shown above |
| `apptainer exec --bind /usr/lib/wsl` | Not needed | Passed |
| `apptainer build --reproducible`, twice | The hashes differed | Not run, because Apptainer 1.4 doesn't have it |

+++

## When you're done

- `rm -f repro-gpu.sif` removes the SIF, and `apptainer cache clean` empties Apptainer's cache.
