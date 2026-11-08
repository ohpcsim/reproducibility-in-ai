---
title: Environments in containers
---

## Who it's for

- Anyone who wants to carry [Exercise 1](environments.ipynb)'s environment to another machine, such as a cluster.
- It's optional, and none of the other exercises need it.
- You run it on your own machine, after Exercise 1, because the images are built from the locks you committed there.
- There's no Binder for it. A Binder session is already a container, and it has no container tool.
- We cover Linux containers. They need a Linux kernel, so a Mac or Windows PC runs them in a VM.
- The site doesn't run this page. The output below was recorded from real runs, on the machines named in [What we ran where](#containers-what-we-ran-where).

## The problem

- Your locks rebuild the environment on a machine that has conda or uv.
- The next machine may have neither, or a different operating system, or no way to install anything.
- A container carries the environment, the code and the data together, and runs the same way on any machine with a container tool.

(what-to-run-where)=
## Step 0: pick your route

| Where you are | What to use | Why | What we ran |
|---|---|---|---|
| Your Mac | Docker Desktop, Podman Desktop, OrbStack, Colima, or Apple's `container` (macOS 26) | Each runs a small Linux VM. (Darwin containers such as [rund](https://github.com/darwin-containers/rund) run macOS software natively; not covered here) | Not run |
| Your Windows PC | Docker Desktop or Podman Desktop, or Podman and Apptainer inside WSL2 | WSL2 provides the Linux kernel | Apptainer 1.4.5 in WSL2, x86_64 |
| Your own Linux machine | Docker, Podman or Apptainer | You have root, so any of them works | Docker 29.6.2, Podman 4.9.3 and Apptainer 1.5.5, aarch64 |
| A shared Linux machine, without root | Podman (rootless) or Apptainer | Neither needs root or a daemon | Rootless Podman and Apptainer, without sudo, on the aarch64 machine. It isn't shared |
| An HPC cluster | Apptainer | It runs as you, with no daemon. The image is one SIF file, with no registry needed. It works with the scheduler, MPI and GPUs | Not run |
| Binder | None | The session is already a container | Nothing to run |

- [Tools and documentation](../../tools.md#containers-on-shared-machines) has the same table.

+++ {"tags": ["track-hpc"]}

Pick one route. Each one is complete on its own and ends with the same check.

+++ {"tags": ["track-mac", "track-linux", "track-hpc"]}

- **Route A: your own Mac, Windows or Linux machine, with Docker or Podman.** You build two images and run them.
+++ {"tags": ["track-wsl2"]}

- **Route B: Apptainer inside WSL2.** You build two SIF files from `.def` files and run them. The build uses Apptainer's `--fakeroot`.
+++ {"tags": ["track-hpc"]}

- **Route B: a shared Linux machine or an HPC cluster, without root, with Apptainer.** You build two SIF files from `.def` files and run them. The build needs Apptainer's `--fakeroot`, which your center may or may not allow.
+++ {"tags": ["track-hpc"]}

- **From A to B: build where you have root, run on the cluster.** You build the images with Route A, copy them to the cluster as files, and convert them to SIF files there. Use this when the cluster doesn't allow `--fakeroot`.

+++

## Get ready, for every route

- Do [Exercise 1](environments.ipynb) in your own terminal, not in Binder, so `project` has both locks committed.
- Every command below runs in that `project` folder. The recipes are in `containers`, next to it.
- Keep Exercise 1's result to compare against:

```bash
git log --oneline
cp metrics.json ../metrics-ex1.json
```

- If `metrics.json` is missing, run `uv run python analyze.py` first.
+++ {"tags": ["track-hpc"]}

- On a cluster, clone your `project` and the `containers` folder next to each other, as on your machine.

+++

## The recipes

- An image is the built container. You build it once from a recipe: a `Dockerfile` for Docker and Podman, or a `.def` file for Apptainer.
- Both kinds of recipe do the same steps. The conda image builds from your `explicit-<platform>.txt`, and the uv image from your `uv.lock`.
- A container is Linux, even on a Mac or Windows PC. So the conda image needs a Linux lock: `explicit-linux-64.txt` on x86_64 or `explicit-linux-aarch64.txt` on ARM. One `uv.lock` builds on both.
- A tag such as `miniforge3:26.9.4-2` can move, and a sha256 digest can't. Every recipe pins its base image by digest. Each digest covers x86_64 and ARM, and the tool pulls the one for your machine.
+++ {"tags": ["track-mac", "track-linux", "track-hpc"]}

- To get a digest for another image, run `docker pull`, then `docker inspect --format '{{index .RepoDigests 0}}' IMAGE`.

`containers/Dockerfile.conda`:

```{literalinclude} containers/Dockerfile.conda
:language: dockerfile
```

`containers/Dockerfile.uv`:

```{literalinclude} containers/Dockerfile.uv
:language: dockerfile
```

+++ {"tags": ["track-wsl2", "track-hpc"]}

```{literalinclude} containers/penguins-conda.def
```

```{literalinclude} containers/penguins-uv.def
```

+++

- They copy only the files they need, so your `.venv` and `.git` stay out of the image.
- The conda recipes pick the lock with the same `conda config --show subdir` command as Exercise 1.
- `uv sync --locked` stops with an error if `uv.lock` doesn't match `pyproject.toml`, as in Exercise 1.
- They put the environment first on `PATH` and run `python analyze.py`.
- The uv image doesn't start with `uv run`. Under Apptainer, which runs in your folder, `uv run` found the project's own `.venv` and used it instead of the container's environment.

+++ {"tags": ["track-mac", "track-linux", "track-hpc"]}

## Route A: your own machine, Docker or Podman

- Install one of the tools in the table for your machine. [Set up your environment](../../setup.md#container-tool) links to each one.
- The commands are the same with `podman`: write `podman` where this says `docker`.
+++ {"tags": ["track-linux", "track-hpc"]}

- On Linux, `docker` needs root or membership in the `docker` group. Podman runs rootless, with no daemon.

+++ {"tags": ["track-mac"]}

**A Mac needs a Linux lock first.** Your conda lock is `explicit-osx-arm64.txt`, and it doesn't install in a Linux container. Skip the conda image, or write a Linux lock inside the Miniforge container and commit it:

```bash
docker run --rm -v "$PWD":/work -w /work docker.io/condaforge/miniforge3:26.9.4-2@sha256:dfb274710eee2bb062c87b15c10fde6ea91f71b763796b5de489df87b08cf678 \
  sh -c 'conda env create --quiet --prefix /tmp/env --file environment.yml && conda list --prefix /tmp/env --explicit --md5 > explicit-$(conda config --show subdir | cut -d" " -f2).txt'
git add explicit-linux-aarch64.txt
git commit -m "Lock the conda environment for Linux on ARM"
```

- That's a new solve from `environment.yml`, so compare its versions with your Mac lock.
- We ran this command with Podman on Linux on ARM, where it wrote the same 38 packages as the lock from Exercise 1. We haven't run it on a Mac.

+++ {"tags": ["track-mac", "track-linux", "track-hpc"]}

**Build, run and compare:**

```bash
docker build -f ../containers/Dockerfile.conda -t penguins-conda:v1 .
docker build -f ../containers/Dockerfile.uv -t penguins-uv:v1 .
docker run --rm penguins-conda:v1 > ../metrics-image-conda.json
docker run --rm penguins-uv:v1 > ../metrics-image-uv.json
diff ../metrics-ex1.json ../metrics-image-conda.json
diff ../metrics-ex1.json ../metrics-image-uv.json
```

- `analyze.py` prints the same JSON it writes to `metrics.json`, so each run's file is the container's `metrics.json`.
- `diff` prints nothing when the files match exactly. That's the check.
- Podman needs the full image name, with the registry. The recipes have it: `docker.io/condaforge/miniforge3` and `ghcr.io/astral-sh/uv`. Without `docker.io/`, Podman 4.9.3 on Ubuntu stopped with `short-name ... did not resolve to an alias`.
+++ {"tags": ["track-linux", "track-hpc"]}

- Rootless, Podman's conda build printed warnings such as `can't raise ambient capability CAP_CHOWN`. The build still succeeded.

+++ {"tags": ["track-wsl2", "track-hpc"]}

(route-b)=
## Route B: Apptainer

- Apptainer runs as you, in your current folder, with no daemon.
+++ {"tags": ["track-hpc"]}

- If your site has it as a module, load it first, for example `module load apptainer`. Your center's documentation names it.

+++ {"tags": ["track-wsl2", "track-hpc"]}

**Build the SIF files** from the `.def` files:

```bash
apptainer build --fakeroot ../penguins-conda.sif ../containers/penguins-conda.def
apptainer build --fakeroot ../penguins-uv.sif ../containers/penguins-uv.def
```

- Optional: with Apptainer 1.5 or newer, add `--reproducible` to `apptainer build`. Apptainer 1.4 doesn't have it.

+++ {"tags": ["track-hpc"]}

- If the build stops because `--fakeroot` isn't allowed, use [From A to B](#from-a-to-b).

+++ {"tags": ["track-wsl2", "track-hpc"]}

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
- A SIF is one file. Copy it to another machine and run it there with the same `apptainer exec` command.
+++ {"tags": ["track-hpc"]}

- On a cluster, run it in a job, the same way you run any program.

+++ {"tags": ["track-hpc"]}

(from-a-to-b)=
## From A to B: build where you have root, run on the cluster

- Converting an image to a SIF doesn't need `--fakeroot`.
- The image has to match the cluster's architecture, usually x86_64. On an Apple-silicon Mac, or any ARM machine, add `--platform linux/amd64` to each `docker build`. The conda image then needs `explicit-linux-64.txt`, the conda lock for x86_64 Linux. Write it with Exercise 1's steps on an x86_64 Linux machine. We haven't run `--platform linux/amd64` on a Mac.

**On your machine**, build the images as in Route A, then save each one to a file:

```bash
docker save -o ../penguins-conda.tar penguins-conda:v1
docker save -o ../penguins-uv.tar penguins-uv:v1
```

- With Podman, save with `podman save --format docker-archive -o ...`.
- Copy the two `.tar` files to the folder next to your `project` on the cluster, for example with `scp`.

**On the cluster**, convert each file to a SIF:

```bash
apptainer build --force ../penguins-conda.sif docker-archive://../penguins-conda.tar
apptainer build --force ../penguins-uv.sif docker-archive://../penguins-uv.tar
```

- `--force` writes over the SIF files from Route B, if you made them.
- Then run and compare as in [Route B](#route-b).
- Every build stamps a new ID and build time into the SIF, so the hash changes each time.
- With Apptainer 1.5 or newer, `apptainer build --reproducible` gives the same hash every time.
- Either way, record the hash of the SIF you run.

+++

(containers-what-we-ran-where)=
## What we ran where

- **NVIDIA DGX Spark, aarch64, Ubuntu 24.04.5, Linux 7.0.0, with Docker 29.6.2, Podman 4.9.3 rootless and Apptainer 1.5.5.** Recorded November 8, 2026. The locks were `explicit-linux-aarch64.txt` and `uv.lock`, from Exercise 1 on that machine. We have root there, but ran Podman and Apptainer without sudo.
- **A Windows 11 PC, x86_64, WSL2 with Ubuntu 24.04.1, with Apptainer 1.4.5.** Recorded November 8, 2026. It has no Docker or Podman. The locks were `explicit-linux-64.txt`, made there with Exercise 1's steps, and the same `uv.lock` as on the ARM machine, byte for byte.
- Every run printed this, and every `diff` printed nothing:

```text
{
  "dimorphism_g_adelie": 648.9,
  "dimorphism_g_chinstrap": 250.0,
  "dimorphism_g_gentoo": 934.2,
  "n_rows": 103
}
```

- On the ARM machine, both images have Python 3.12.16, pandas 3.1.1 and numpy 2.5.4, the same versions as Exercise 1's locks.

| Route | Machine | conda | uv |
|---|---|---|---|
| A, Docker | DGX Spark, aarch64 Linux | Ran and matched. 1.03 GB image, 7 s build | Ran and matched. 282 MB image, 3 s build |
| A, Podman rootless | DGX Spark, aarch64 Linux | Ran and matched. 1.06 GB image, 14 s build | Ran and matched. 288 MB image, 4 s build |
| A | A Mac | Not run | Not run |
| A | A Windows PC, Docker Desktop or Podman Desktop | Not run | Not run |
| B, Apptainer `--fakeroot` | DGX Spark, aarch64 Linux | Ran and matched. 320 MB SIF, 21 s build | Ran and matched. 87 MB SIF, 5 s build |
| B, Apptainer `--fakeroot` | Windows 11 PC, x86_64 WSL2 | Ran and matched. 331 MB SIF, 23 s build | Ran and matched. 89 MB SIF, 6 s build |
| B | An HPC cluster | Not run | Not run |
| From A to B, Docker's or Podman's image | DGX Spark, aarch64 Linux, both ends | Ran and matched. 320 MB SIF, 20 to 28 s to save and convert | Ran and matched. 87 MB SIF, 5 to 7 s to save and convert |

- Build times include pulling the base image, except Docker's, which had it already. They depend on your network.
- Our From A to B run built and converted on the same machine, so the architecture already matched.

## Clean up

- When you're done, remove what you made.
+++ {"tags": ["track-mac", "track-linux"]}

```bash
docker rmi penguins-conda:v1 penguins-uv:v1
rm -f ../metrics-ex1.json ../metrics-image-conda.json ../metrics-image-uv.json
```

- With Podman, run `podman rmi penguins-conda:v1 penguins-uv:v1` instead of `docker rmi`.
- The base images stay. `docker image ls` or `podman image ls` lists them, and `docker rmi IMAGE_ID` or `podman rmi IMAGE_ID` removes one.
+++ {"tags": ["track-wsl2"]}

```bash
rm -f ../penguins-conda.sif ../penguins-uv.sif ../metrics-ex1.json ../metrics-sif-conda.json ../metrics-sif-uv.json
```

- Apptainer keeps the base images it pulled in its cache. `apptainer cache list` shows it, and `apptainer cache clean` empties it.
+++ {"tags": ["track-hpc"]}

```bash
rm -f ../penguins-conda.tar ../penguins-uv.tar ../penguins-conda.sif ../penguins-uv.sif
rm -f ../metrics-ex1.json ../metrics-image-conda.json ../metrics-image-uv.json ../metrics-sif-conda.json ../metrics-sif-uv.json
```

- `rm -f` skips the files your route didn't make.
- If you used Route A or From A to B, remove the images on the machine where you built them, with `docker rmi penguins-conda:v1 penguins-uv:v1` or `podman rmi penguins-conda:v1 penguins-uv:v1`.
- The base images stay. `docker image ls` or `podman image ls` lists them, and `apptainer cache clean` empties Apptainer's cache.

+++

## Things that trip people up

+++ {"tags": ["track-mac", "track-linux"]}

- Disk space. The two images took 1.3 GB. The conda image is almost four times the uv image, because the Miniforge base image alone is about 600 MB.
+++ {"tags": ["track-wsl2"]}

- Disk space. The two SIF files took 0.4 GB. The conda SIF is almost four times the uv SIF, because it holds the Miniforge base image.
+++ {"tags": ["track-hpc"]}

- Disk space. The two images took 1.3 GB, the files saved from them another 1.3 GB, and the two SIF files 0.4 GB. The conda image is almost four times the uv image, because the Miniforge base image alone is about 600 MB.
+++ {"tags": ["track-linux", "track-hpc"]}

- Rootless Podman keeps images in your home folder, under `~/.local/share/containers`, so check your quota.
+++ {"tags": ["track-wsl2"]}

- `--fakeroot`. Building a SIF from a `.def` file needs it.
+++ {"tags": ["track-hpc"]}

- `--fakeroot`. Building a SIF from a `.def` file needs it, and some centers don't allow it. Converting an image doesn't, so use From A to B.
+++ {"tags": ["track-mac"]}

- The Mac lock. `explicit-osx-arm64.txt` doesn't install in a Linux container. Write a Linux lock first, as in Route A.
+++ {"tags": ["track-mac"]}

- Docker Desktop, Podman Desktop and the other Mac tools run a Linux VM. The VM's memory and disk come out of your machine's, and its settings set how much. On a Mac with Apple silicon, the containers are Linux on ARM, so they use the `linux-aarch64` lock.
+++ {"tags": ["track-wsl2"]}

- On Windows, keep the project in your WSL2 home, not under `/mnt/c`, and run the commands in the WSL2 terminal.
