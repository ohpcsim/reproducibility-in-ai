---
title: 1b. Environments in containers
---

## Who it's for

- Anyone who wants to carry [Exercise 1](environments.ipynb)'s environment to another machine, such as a cluster.
- It's optional, and none of the other exercises need it.
+++ {"tags": ["track-mac", "track-linux", "track-wsl2"]}

- You run it on your own machine, after Exercise 1, because the images are built from the locks you committed there.

+++ {"tags": ["track-hpc"]}

- You run it on the cluster, after Exercise 1, because the images are built from the locks you committed there.

+++

- There's no Binder for it. A Binder session is already a container, and it has no container tool.
+++ {"tags": ["track-mac", "track-wsl2"]}

- We cover Linux containers. They need a Linux kernel, so a Mac or Windows PC runs them in a VM.

+++
- [Tools and documentation](../../tools.md#containers-on-shared-machines) says which container tool to use on each kind of machine.
- The site doesn't run this page. The output below was recorded from real runs, listed in [What we ran where](#containers-what-we-ran-where).

## The problem

- Your locks rebuild the environment on a machine that has conda or uv.
- The next machine may have neither, or a different operating system, or no way to install anything.
- A container carries the environment, the code and the data together, and runs the same way on any machine with a container tool.

+++ {"tags": ["track-hpc"]}

## Apptainer on the cluster

- Apptainer builds and runs the containers on the cluster. You build two SIF files from Apptainer's own recipes, the `.def` files, with `--fakeroot`.

+++

## Get ready

- Do [Exercise 1](environments.ipynb) in your own terminal, not in Binder, so `project` has both locks committed.
- Every command below runs in that `project` folder. The recipes are in `containers`, next to it.
- Keep Exercise 1's result to compare against:

```bash
git log --oneline
cp metrics.json ../metrics-ex1.json
```

- If `metrics.json` is missing, run `uv run python analyze.py` first.

## The recipes

+++ {"tags": ["track-mac", "track-linux", "track-wsl2"]}

- An image is the built container. You build it once from a recipe, a `Dockerfile`. Podman builds Dockerfiles.
- The conda image builds from your `explicit-<platform>.txt`, and the uv image from your `uv.lock`.
+++ {"tags": ["track-hpc"]}

- An image is the built container. Apptainer builds it once from a recipe, a `.def` file, into one SIF file.
- The conda image builds from your `explicit-<platform>.txt`, and the uv image from your `uv.lock`.
- The Mac, Linux and WSL2 tracks build the same images with Podman, from Dockerfiles in the same folder. A `.def` and its Dockerfile declare the same steps for two different tools, and our runs show they give the same results.

+++ {"tags": ["track-mac", "track-wsl2"]}

- A container is Linux, even on a Mac or Windows PC. So the conda image needs a Linux lock: `explicit-linux-64.txt` on x86_64 or `explicit-linux-aarch64.txt` on ARM. One `uv.lock` builds on both.

+++ {"tags": ["track-linux", "track-hpc"]}

- A container is Linux, so the conda image needs a Linux lock: `explicit-linux-64.txt` on x86_64 or `explicit-linux-aarch64.txt` on ARM. One `uv.lock` builds on both.

+++
- A tag such as `miniforge3:26.9.4-2` can move, and a sha256 digest can't. Every recipe pins its base image by digest. Each digest covers x86_64 and ARM, and the tool pulls the one for your machine.
+++ {"tags": ["track-hpc"]}

- Each `.def` file's `From:` line pins its base image by digest, the same digest as its Dockerfile.
- To get the digest for another image, use a machine with Podman:
+++ {"tags": ["track-mac", "track-linux", "track-wsl2"]}

- To get the digest for another image, pull it, then print its digest:

+++

```bash
podman pull docker.io/library/ubuntu:24.04
podman inspect --format '{{.Digest}}' docker.io/library/ubuntu:24.04
```

+++ {"tags": ["track-linux", "track-wsl2", "track-hpc"]}

- With Podman 4.9.3 on our ARM machine and in x86_64 WSL2, that printed `sha256:fe81560990fae86dc4743202b2cb4d3df98d0bcf949173cecef15ce1127ef852`, the digest 1c's GPU recipe pins. Pin that digest. It covers every platform.

+++ {"tags": ["track-mac"]}

- On our Linux machines, ARM and x86_64, with Podman 4.9.3, that printed `sha256:fe81560990fae86dc4743202b2cb4d3df98d0bcf949173cecef15ce1127ef852`. Pin that digest. It covers every platform.

+++

- Don't use `podman inspect --format '{{index .RepoDigests 0}}'`. On the ARM machine it printed a different digest, for the ARM image only.

+++ {"tags": ["track-mac", "track-linux", "track-wsl2"]}

`containers/Dockerfile.conda`:

```{literalinclude} containers/Dockerfile.conda
:language: dockerfile
```

`containers/Dockerfile.uv`:

```{literalinclude} containers/Dockerfile.uv
:language: dockerfile
```

+++ {"tags": ["track-hpc"]}

`containers/penguins-conda.def`:

```{literalinclude} containers/penguins-conda.def
```

`containers/penguins-uv.def`:

```{literalinclude} containers/penguins-uv.def
```

+++

- They copy only the files they need, so your `.venv` and `.git` stay out of the image.
- The conda recipes pick the lock with the same `conda config --show subdir` command as Exercise 1.
- `uv sync --locked` stops with an error if `uv.lock` doesn't match `pyproject.toml`, as in Exercise 1.
- They put the environment first on `PATH` and run `python analyze.py`.
+++ {"tags": ["track-hpc"]}

- The uv image doesn't start with `uv run`. Under Apptainer, which runs in your folder, `uv run` found the project's own `.venv` and used it instead of the container's environment.

+++ {"tags": ["track-mac"]}

## Build and run with Podman

- Install Podman Desktop and start the Podman machine, as [Set up your environment](../../setup.md#container-tool) says.
+++ {"tags": ["track-linux", "track-wsl2"]}

## Build and run with Podman

+++ {"tags": ["track-wsl2"]}

- Run these commands inside WSL2, in the Ubuntu window.
+++ {"tags": ["track-linux", "track-wsl2"]}

- Install Podman as [Set up your environment](../../setup.md#container-tool) says. Podman runs rootless, as you, with no daemon. Don't use `sudo` with these commands.
+++ {"tags": ["track-mac"]}

**A Mac needs a Linux lock first.** Your conda lock is `explicit-osx-arm64.txt`, and it doesn't install in a Linux container. Write a Linux lock inside the Miniforge container and commit it:

```bash
podman run --rm -v "$PWD":/work -w /work docker.io/condaforge/miniforge3:26.9.4-2@sha256:dfb274710eee2bb062c87b15c10fde6ea91f71b763796b5de489df87b08cf678 \
  sh -c 'conda env create --quiet --prefix /tmp/env --file environment.yml && conda list --prefix /tmp/env --explicit --md5 > explicit-$(conda config --show subdir | cut -d" " -f2).txt'
git add explicit-linux-*.txt
git commit -m "Lock the conda environment for Linux"
```

- That's a new solve from `environment.yml`, so compare its versions with your Mac lock. `grep /pandas- explicit-*.txt` prints the pandas line from both locks. The versions should match.
- With Podman 6.1.4 on a Mac with Apple silicon, it wrote the same 38 packages as the lock from Linux on ARM.

+++ {"tags": ["track-mac", "track-linux", "track-wsl2"]}

**Build, run and compare:**

```bash
podman build -f ../containers/Dockerfile.conda -t penguins-conda:v1 .
podman build -f ../containers/Dockerfile.uv -t penguins-uv:v1 .
podman run --rm penguins-conda:v1 > ../metrics-image-conda.json
podman run --rm penguins-uv:v1 > ../metrics-image-uv.json
diff ../metrics-ex1.json ../metrics-image-conda.json
diff ../metrics-ex1.json ../metrics-image-uv.json
```

+++ {"tags": ["track-mac", "track-linux", "track-wsl2"]}

- `analyze.py` prints the same JSON it writes to `metrics.json`, so each run's file is the container's `metrics.json`.
- `diff` prints nothing when the files match exactly. That's the check.
- Podman needs the full image name, with the registry. The recipes have it: `docker.io/condaforge/miniforge3` and `ghcr.io/astral-sh/uv`. Without `docker.io/`, Podman 4.9.3 on our Linux machine stopped with `short-name ... did not resolve to an alias`.
+++ {"tags": ["track-mac"]}

- The Linux-lock step pulls the Miniforge image, so the conda build reuses it.
+++ {"tags": ["track-wsl2"]}

- The first `podman` command may print `"/" is not a shared mount, this could cause issues or missing mounts with rootless containers`. Our builds and runs worked with it.
+++ {"tags": ["track-linux"]}

- Rootless, Podman's conda build printed warnings such as `can't raise ambient capability CAP_CHOWN`. The build still succeeded.

+++ {"tags": ["track-hpc"]}

(build-apptainer)=
## Build and run with Apptainer

- Apptainer runs as you, in your current folder, with no daemon.
- If your site has it as a module, load it first, for example `module load apptainer`. Your center's documentation names it.

**Build the SIF files** from the `.def` files:

```bash
apptainer build --fakeroot ../penguins-conda.sif ../containers/penguins-conda.def
apptainer build --fakeroot ../penguins-uv.sif ../containers/penguins-uv.def
```

- If the build stops because `--fakeroot` isn't allowed, build the SIF files on a machine where it works, with the same architecture as the cluster, and copy them over.
- Every build stamps a new ID and build time into the SIF, so the hash changes each time.
- Optional: with Apptainer 1.5 or newer, add `--reproducible` to `apptainer build`. Apptainer 1.4 doesn't have it. With it, two builds of the uv `.def` gave the same sha256 on our machine.

**Run and compare:**

```bash
apptainer exec ../penguins-conda.sif python analyze.py > ../metrics-sif-conda.json
apptainer exec ../penguins-uv.sif python analyze.py > ../metrics-sif-uv.json
diff ../metrics-ex1.json ../metrics-sif-conda.json
diff ../metrics-ex1.json ../metrics-sif-uv.json
sha256sum ../penguins-*.sif
```

- `apptainer exec IMAGE.sif python analyze.py` runs your `analyze.py` on your `data`, with the container's environment, and writes `metrics.json` in your folder.
- `diff` prints nothing when the files match exactly.
- A SIF is one file. Copy it to another machine with your `project` folder, and run it there with the same `apptainer exec` command.
- On a cluster, run it in a job, the same way you run any program.
- Record the `sha256sum` of the SIF you run.

+++

(containers-what-we-ran-where)=
## What we ran where

+++ {"tags": ["track-linux"]}

- **NVIDIA DGX Spark, aarch64, Ubuntu 24.04.5, Linux 7.0.0, with Podman 4.9.3 rootless.** Recorded November 8, 2026. The locks were `explicit-linux-aarch64.txt` and `uv.lock`, from Exercise 1 on that machine. We have root there, but ran Podman without sudo.
+++ {"tags": ["track-hpc"]}

- **NVIDIA DGX Spark, aarch64, Ubuntu 24.04.5, Linux 7.0.0, with Apptainer 1.5.5.** Recorded November 8, 2026. The locks were `explicit-linux-aarch64.txt` and `uv.lock`, from Exercise 1 on that machine. We have root there, but ran Apptainer without sudo.
+++ {"tags": ["track-mac"]}

- **A Mac with Apple silicon, with Podman Desktop and Podman 6.1.4.** Recorded November 8, 2026. The locks were `explicit-linux-aarch64.txt`, written there with this page's Linux-lock step and identical to the lock from Linux on ARM, and `uv.lock` from Exercise 1 on the Mac.
+++ {"tags": ["track-wsl2"]}

- **A Windows 11 PC, x86_64, WSL2 with Ubuntu 24.04.1, with rootless Podman 4.9.3.** Recorded November 8, 2026.

+++

- Every run printed this, and every `diff` printed nothing:

```text
{
  "dimorphism_g_adelie": 648.9,
  "dimorphism_g_chinstrap": 250.0,
  "dimorphism_g_gentoo": 934.2,
  "n_rows": 103
}
```

- Both images have Python 3.12.16, pandas 3.1.1 and numpy 2.5.4, the same versions as Exercise 1's locks.

+++ {"tags": ["track-linux"]}

| Tool | Machine | conda | uv |
|---|---|---|---|
| Podman rootless | DGX Spark, aarch64 Linux | Ran and matched. 1.06 GB image, 14 s build | Ran and matched. 288 MB image, 4 s build |

- Build times include pulling the base image. They depend on your network.

+++ {"tags": ["track-mac"]}

| Tool | Machine | conda | uv |
|---|---|---|---|
| Podman Desktop | MacBook, Apple silicon, macOS, Podman 6.1.4 (libkrun, 2 GiB VM) | Ran and matched. 1.06 GB image, 11 s build (Linux lock first, 12 s with the pull) | Ran and matched. 288 MB image, 6 s build |

- The uv build time includes pulling the base image. The conda build reused the image the Linux-lock step pulled. Times depend on your network.

+++ {"tags": ["track-wsl2"]}

| Tool | Machine | conda | uv |
|---|---|---|---|
| Podman rootless | Windows 11 PC, x86_64 WSL2 | Ran and matched. 1.06 GB image, 17 s build | Ran and matched. 270 MB image, 5 s build |

- Build times include pulling the base image. They depend on your network.

+++ {"tags": ["track-hpc"]}

| Tool | Machine | conda | uv |
|---|---|---|---|
| Apptainer `--fakeroot`, from the `.def` files | DGX Spark, aarch64 Linux | Ran and matched. 320 MB SIF, 21 s build | Ran and matched. 87 MB SIF, 5 s build |
| Apptainer `--fakeroot`, from the `.def` files | An HPC cluster | Not run | Not run |

- Build times include pulling the base image. They depend on your network.

+++

## Things that trip people up

- The uv image's build may print `warning: Failed to hardlink files; falling back to full copy`. It's harmless. uv copies the files instead.
+++ {"tags": ["track-mac", "track-linux"]}

- Disk space. The two images took 1.3 GB. The conda image is almost four times the uv image, because the Miniforge base image alone is about 600 MB.
+++ {"tags": ["track-wsl2"]}

- Disk space. The two images took 1.3 GB. Podman keeps images in your WSL2 home, under `~/.local/share/containers`.
+++ {"tags": ["track-hpc"]}

- Disk space. The two SIF files took 0.4 GB, and Apptainer's cache in your home folder keeps the base images, so check your quota. The conda SIF is almost four times the uv SIF, because of the Miniforge base image.
+++ {"tags": ["track-linux"]}

- Rootless Podman keeps images in your home folder, under `~/.local/share/containers`, so check your free disk space.
+++ {"tags": ["track-hpc"]}

- `--fakeroot`. Building a SIF from a `.def` file needs it, and some centers don't allow it. Then build the SIF where it works and copy it over.
+++ {"tags": ["track-mac"]}

- The Mac lock. `explicit-osx-arm64.txt` doesn't install in a Linux container. Write a Linux lock first, with the Linux-lock step above.
+++ {"tags": ["track-mac"]}

- Podman Desktop runs a Linux VM. Its memory and disk come out of your Mac's, and Podman Desktop's settings set how much. On Apple silicon, the containers are Linux on ARM, so they use the `linux-aarch64` lock.
+++ {"tags": ["track-wsl2"]}

- On Windows, keep the project in your WSL2 home, not under `/mnt/c`, and run the commands in the WSL2 terminal.

+++

## When you're done

- Remove what you made.
+++ {"tags": ["track-mac", "track-linux", "track-wsl2"]}

```bash
podman rmi penguins-conda:v1 penguins-uv:v1
rm -f ../metrics-ex1.json ../metrics-image-conda.json ../metrics-image-uv.json
```

- The base images stay. `podman image ls` lists them, and `podman rmi IMAGE_ID` removes one.
+++ {"tags": ["track-hpc"]}

```bash
rm -f ../penguins-conda.sif ../penguins-uv.sif
rm -f ../metrics-ex1.json ../metrics-sif-conda.json ../metrics-sif-uv.json
```

- The base images stay in Apptainer's cache. `apptainer cache clean --force` empties it. Without `--force` it asks first.
