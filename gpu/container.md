---
title: If you need a container
---

- This is step 3 of [1c, PyTorch with a GPU](gpu.md). It's optional, and none of the other exercises need it.
- You run it yourself, after step 1 there, on the machine where the check passed, because the container is built from the conda lock you made there.
- There's no Binder for it.

- A container carries your software to the next system.
- A tag such as `ubuntu:24.04` can move, and a sha256 digest can't, so the definition file pins the base image by digest and the installer by version.
- The digest is for a multi-architecture image, and Apptainer pulls the right one for your machine.
- `uname -m` picks the matching installer.
- The environment comes from your lock, so the container has exactly what you tested.
- You need about 20 GB of free disk.

(with-apptainer)=
## Build and run with Apptainer

- Apptainer runs as you, with no daemon.
+++ {"tags": ["track-linux", "track-wsl2"]}

- The build uses Apptainer's `--fakeroot`.
+++ {"tags": ["track-hpc"]}

- If your site has it as a module, load it first, for example `module load apptainer`. Your center's documentation names it.
- The build needs Apptainer's `--fakeroot`, which your center may or may not allow. If it doesn't, build the SIF on a Linux machine where `--fakeroot` works, with the same architecture as your cluster, and copy the SIF over. It's one file.

+++

From the `gpu` folder, with your `lock.txt` in it:

```{literalinclude} repro-gpu.def
```

```bash
apptainer build --fakeroot --force repro-gpu.sif repro-gpu.def
apptainer exec --nv repro-gpu.sif python /opt/verify_gpu.py
```

- The `--nv` flag brings in the host's NVIDIA driver, the one thing the container doesn't carry.
- Optional: with Apptainer 1.5 or newer, add `--reproducible` to `apptainer build`. Apptainer 1.4 doesn't have it.
- Every build stamps a new ID and build time into the SIF, so the hash changes each time, unless you used `--reproducible`. Record the hash of the SIF you run, with `sha256sum repro-gpu.sif`.
+++ {"tags": ["track-hpc"]}

- On a cluster, run it on a GPU node, in a job, the same way you run any program.

+++ {"tags": ["track-linux", "track-hpc"]}

## With a pre-built image

- You don't have to build your own.
- NVIDIA's [NGC catalog](https://catalog.ngc.nvidia.com) has PyTorch images with CUDA already configured, and they're tested by NVIDIA.
- Pick a tag recent enough for your GPU. A tag can move, so record the SIF's hash.
- Run the same check on it.
- We did not run this one, so treat these commands as a starting point.

```bash
apptainer pull ngc-pytorch.sif docker://nvcr.io/nvidia/pytorch:YY.MM-py3
sha256sum ngc-pytorch.sif
apptainer exec --nv ngc-pytorch.sif python verify_gpu.py
```

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

+++ {"tags": ["track-linux"]}

| Step | aarch64, GB10, Linux |
|---|---|
| `apptainer build --fakeroot` from `repro-gpu.def` | Ran, and passed |
| `apptainer exec --nv` | Passed |

- The machine is an NVIDIA DGX Spark, driver 580.178.04. We recorded that the check passed, not its output.
+++ {"tags": ["track-wsl2"]}

| Step | x86_64, RTX 3070, WSL2 |
|---|---|
| `apptainer build --fakeroot` from `repro-gpu.def` | Ran, and passed |
| `apptainer exec --nv` | Failed, as shown above |
| `apptainer exec --bind /usr/lib/wsl` | Passed |

+++ {"tags": ["track-hpc"]}

| Step | aarch64, GB10, Linux | An HPC cluster |
|---|---|---|
| `apptainer build --fakeroot` from `repro-gpu.def` | Ran, and passed | Not run |
| `apptainer exec --nv` | Passed | Not run |

- The Linux machine is an NVIDIA DGX Spark, driver 580.178.04. We recorded that the check passed, not its output.

+++

- When you're done, remove what you made.
- `rm -f repro-gpu.sif` removes the SIF. `apptainer cache list` shows the base images Apptainer keeps, and `apptainer cache clean` empties its cache.
