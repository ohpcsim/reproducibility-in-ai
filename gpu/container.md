---
title: If you need a container
---

- This page is optional, and none of the exercises need it.
- You run it yourself, after [the GPU page](gpu.md), on the machine where the check passed, because the container is built from the lock you made there.
- There's no Binder for it.

- A container carries your software to the next system.
- A tag such as `ubuntu:24.04` can move, and a sha256 digest can't, so this file pins the base image by digest and the installer by version.
- The digest is for a multi-architecture image, and Docker or Podman pulls the right one for your machine.
- `uname -m` picks the matching installer.
- The environment comes from your lock, so the container has exactly what you tested.
- You need about 20 GB of free disk.

```{literalinclude} Dockerfile
:language: dockerfile
```

- To get a digest for another image, run `docker pull`, then `docker inspect --format '{{index .RepoDigests 0}}' IMAGE`.

(with-docker-and-apptainer)=
## With Docker and Apptainer

- Most HPC centers run Apptainer rather than Docker.
- So build with Docker on a machine you control, with the same architecture as your cluster, then save the image to one file.

From the `gpu` folder, with your `lock.txt` in it:

```bash
docker build -t repro-gpu:v1 .
docker run --rm --gpus all repro-gpu:v1
docker save -o repro-gpu.tar repro-gpu:v1
```

- `docker run --gpus all` needs NVIDIA's container toolkit on that machine.
- Copy `repro-gpu.tar` to your cluster and convert it to a SIF, a single file you can hash and move.
- Build one per architecture.
- On a GPU node, run the same check.
- The `--nv` flag brings in the host's NVIDIA driver, the one thing the container doesn't carry.

```bash
apptainer build --force repro-gpu.sif docker-archive://repro-gpu.tar
sha256sum repro-gpu.sif
apptainer exec --nv repro-gpu.sif python /opt/verify_gpu.py
```

- Converting the same image twice gave SIFs with different hashes when we tried it.
- So the hash identifies one file, not the recipe.
- Keep the SIF you ran, or at least its hash.

- **Recorded November 7, 2026, on aarch64, NVIDIA GB10, driver 580.178.04, Linux, with Apptainer 1.5.5.** The conda route on this machine gave the same checksum.
- That's the check, not the time.

```text
torch           2.14.1
cuda runtime    13.4
cuda available  True
device          NVIDIA GB10
capability      (12, 1)
matmul 4096^2   0.0962 s, checksum -4.8324e+05
host            Linux-7.0.0-1024-nvidia-aarch64-with-glibc2.39
```

## With Podman

- Use this on a shared Linux machine where you don't have root and can't use Docker.
- Podman has no daemon and runs rootless, and it builds from the same Dockerfile with the same commands.
- Rootless Podman keeps images in your home folder, under `~/.local/share/containers`. Our image was 6.8 GB and the saved file 6.4 GB, so check your quota.
- [Tools and documentation](../tools.md#containers-on-shared-machines) says which container tool to use where.

From the `gpu` folder, with your `lock.txt` in it:

```bash
podman build -t repro-gpu:v1 .
podman run --rm --device nvidia.com/gpu=all repro-gpu:v1
podman save --format docker-archive -o repro-gpu.tar repro-gpu:v1
```

- `--device nvidia.com/gpu=all` asks for the GPU through CDI, the Container Device Interface.
- It needs a CDI spec that an administrator makes with `nvidia-ctk cdi generate`, in `/etc/cdi` or `/var/run/cdi`. ([NVIDIA's CDI guide](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/cdi-support.html))
- `nvidia-ctk cdi list` shows the devices the spec names.
- Then convert `repro-gpu.tar` to a SIF and run it, with the same `apptainer` commands as [the Docker route](#with-docker-and-apptainer).

- **Recorded November 8, 2026, on aarch64, NVIDIA GB10, driver 580.178.04, Ubuntu 24.04, with Podman 4.9.3 rootless and Apptainer 1.5.5.**
- `podman build` and `podman save` worked.
- `podman run` with the GPU didn't. The machine's CDI spec came from NVIDIA Container Toolkit 1.20.1 in CDI format 0.7.0, and Podman 4.9.3 couldn't read it:

```text
Error: setting up CDI devices: unresolvable CDI devices nvidia.com/gpu=all
```

- `podman --log-level=debug run ...` shows the reason, `json: unknown field "additionalGids"`.
- We didn't try a newer Podman, so we can't say which version reads this spec.
- Without `--device`, the container runs, and the check fails as it should when there's no GPU:

```text
torch           2.14.1
cuda runtime    13.4
cuda available  False
FAIL: CUDA is not available; this route did not reach the GPU
```

- The SIF converted from Podman's file reached the GPU with `apptainer exec --nv`. The conda route on this machine gave the same checksum.

```text
torch           2.14.1
cuda runtime    13.4
cuda available  True
device          NVIDIA GB10
capability      (12, 1)
matmul 4096^2   0.0914 s, checksum -4.8324e+05
host            Linux-7.0.0-1024-nvidia-aarch64-with-glibc2.39
```

- So on this machine, Podman built the image and Apptainer ran it on the GPU.
- We haven't seen `podman run` reach a GPU.

## With Apptainer and no Docker

- If you don't have Docker, this definition file does the same steps.
- It needs Apptainer's `--fakeroot`, which your center may or may not allow.

From the `gpu` folder, with your `lock.txt` in it:

```{literalinclude} repro-gpu.def
```

```bash
apptainer build --fakeroot --force repro-gpu.sif repro-gpu.def
apptainer exec --nv repro-gpu.sif python /opt/verify_gpu.py
```

## With a pre-built image

- You don't have to build your own.
- NVIDIA's [NGC catalog](https://catalog.ngc.nvidia.com) has PyTorch images with CUDA already configured, and they're tested by NVIDIA.
- Pick a tag recent enough for your GPU, then record and use its digest rather than the tag, the same way as above.
- Run the same check on it.
- We did not run this one, so treat these commands as a starting point.

```bash
docker pull nvcr.io/nvidia/pytorch:YY.MM-py3
docker inspect --format '{{index .RepoDigests 0}}' nvcr.io/nvidia/pytorch:YY.MM-py3
apptainer pull ngc-pytorch.sif docker://nvcr.io/nvidia/pytorch@sha256:THE_DIGEST
sha256sum ngc-pytorch.sif
apptainer exec --nv ngc-pytorch.sif python verify_gpu.py
```

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

## What we ran where

| Step | aarch64, GB10, Linux | x86_64, RTX 3070, WSL2 |
|---|---|---|
| `docker build`, `docker run --gpus all`, `docker save` | Ran, and passed | Not run, because this machine has no Docker |
| `apptainer build` from `docker-archive://` | Ran, and passed | Not run, because it needs the Docker file |
| `podman build`, `podman save`, rootless | Ran, and passed | Not run |
| `podman run --device nvidia.com/gpu=all` | Failed, because Podman 4.9.3 couldn't read the CDI spec | Not run |
| `podman run` without the GPU | Ran, and the check failed as expected | Not run |
| `apptainer build` from Podman's `docker-archive://`, then `apptainer exec --nv` | Ran, and passed | Not run |
| `apptainer build --fakeroot` from `repro-gpu.def` | Ran, and passed | Ran, and passed |
| `apptainer exec --nv` | Passed | Failed, as shown above |
| `apptainer exec --bind /usr/lib/wsl` | Not needed | Passed |

- So the `docker-archive://` route, from Docker or Podman, has only run on aarch64.
- We expect it to work on x86_64 too, because the Dockerfile picks its installer with `uname -m` and the base image's digest covers both architectures, but we haven't run it there.

- When you're done, remove what you made.
- `docker rmi repro-gpu:v1` or `podman rmi repro-gpu:v1` removes the image, and `rm repro-gpu.tar repro-gpu.sif` removes the files.
