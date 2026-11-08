---
title: Environments in containers
---

- This page is optional. It puts the two environments from [Exercise 1](environments.ipynb) into containers, one built from the conda lock and one from the uv lock.
- You run it on your own machine, after Exercise 1, because the containers are built from the locks you committed there.
- There's no Binder for it. A Binder session is already a container, and it has no container tool.
- The site doesn't run this page. The output below was recorded from real runs, on the machines named with it.

## The problem

- Your locks rebuild the environment on a machine that has conda or uv.
- The next machine may have neither, or a different operating system, or no way to install anything.
- A container carries the environment, the code and the data together, and runs the same way on any machine with a container tool.

## Facts

- An image is the built container. You build it once from a recipe: a `Dockerfile` for Docker and Podman, or a `.def` file for Apptainer.
- Docker and Podman read the same `Dockerfile`, with the same commands. Apptainer converts their image to one SIF file, or builds the SIF from its own `.def` file.
- A tag such as `miniforge3:26.9.4-2` can move, and a sha256 digest can't. Both recipes pin the base image by digest.
- Each digest covers x86_64 and ARM, and the tool pulls the one for your machine.
- The conda image builds from your `explicit-<platform>.txt`. The conda lock is per platform, so you build one image per architecture, each from its own lock.
- The uv image builds from your `uv.lock`. One `uv.lock` builds on x86_64 and ARM.
- A container is Linux, even on a Mac or Windows PC. So the conda image needs a Linux lock: `explicit-linux-64.txt` on x86_64 or `explicit-linux-aarch64.txt` on ARM.
- To get a digest for another image, run `docker pull`, then `docker inspect --format '{{index .RepoDigests 0}}' IMAGE`.

(what-to-run-where)=
## What to run where

- We cover Linux containers. They need a Linux kernel, so a Mac or Windows PC runs them in a VM.

| Where you are | What to use | Why | What we ran |
|---|---|---|---|
| Your Mac | Docker Desktop, Podman Desktop, OrbStack, Colima, or Apple's `container` (macOS 26) | Each runs a small Linux VM. (Darwin containers such as [rund](https://github.com/darwin-containers/rund) run macOS software natively; not covered here) | Not run |
| Your Windows PC | Docker Desktop or Podman Desktop, or Podman and Apptainer inside WSL2 | WSL2 provides the Linux kernel | Apptainer 1.4.5 in WSL2, x86_64 |
| Your own Linux machine | Docker, Podman or Apptainer | You have root, so any of them works | Docker 29.6.2, Podman 4.9.3 and Apptainer 1.5.5, aarch64 |
| A shared Linux machine, without root | Podman (rootless) or Apptainer | Neither needs root or a daemon | Rootless Podman and Apptainer, without sudo, on the aarch64 machine. It isn't shared |
| An HPC cluster | Apptainer | It runs as you, with no daemon. The image is one SIF file, with no registry needed. It works with the scheduler, MPI and GPUs | Not run |
| Binder | None | The session is already a container | Nothing to run |

- [Tools and documentation](../../tools.md#containers-on-shared-machines) has the same table.
- Building a SIF from a `.def` file needs Apptainer's `--fakeroot`, which your center may or may not allow. Converting an image from Docker or Podman doesn't.

## Get ready

- Do [Exercise 1](environments.ipynb) in your own terminal, not in Binder, so `project` has both locks committed.
- Every command below runs in that `project` folder. The recipes are in `containers`, next to it.
- Keep Exercise 1's result to compare against:

```bash
git log --oneline
cp metrics.json ../metrics-ex1.json
```

- If `metrics.json` is missing, run `uv run python analyze.py` first.
- The two images took 1.3 GB, the files saved from them another 1.3 GB, and the two SIF files 0.4 GB.

**On a Mac.** Your conda lock is `explicit-osx-arm64.txt`, and it doesn't install in a Linux container. Use the uv image, or write a Linux lock inside the Miniforge container and commit it:

```bash
docker run --rm -v "$PWD":/work -w /work docker.io/condaforge/miniforge3:26.9.4-2@sha256:dfb274710eee2bb062c87b15c10fde6ea91f71b763796b5de489df87b08cf678 \
  sh -c 'conda env create --quiet --prefix /tmp/env --file environment.yml && conda list --prefix /tmp/env --explicit --md5 > explicit-$(conda config --show subdir | cut -d" " -f2).txt'
git add explicit-linux-aarch64.txt
git commit -m "Lock the conda environment for Linux on ARM"
```

- That's a new solve from `environment.yml`, so compare its versions with your Mac lock.
- We ran this command with Podman on Linux on ARM, where it wrote the same 38 packages as the lock from Exercise 1. We haven't run it on a Mac.

## The recipes

`containers/Dockerfile.conda`:

```{literalinclude} containers/Dockerfile.conda
:language: dockerfile
```

`containers/Dockerfile.uv`:

```{literalinclude} containers/Dockerfile.uv
:language: dockerfile
```

- Both copy only the files they need, so your `.venv` and `.git` stay out of the image.
- The conda recipe picks the lock with the same `conda config --show subdir` command as Exercise 1.
- `uv sync --locked` stops with an error if `uv.lock` doesn't match `pyproject.toml`, as in Exercise 1.
- Both put the environment first on `PATH` and run `python analyze.py`.
- The uv image doesn't start with `uv run`. Under Apptainer, which runs in your folder, `uv run` found the project's own `.venv` and used it instead of the container's environment.

## Step 1: build and run with Docker

```bash
docker build -f ../containers/Dockerfile.conda -t penguins-conda:v1 .
docker build -f ../containers/Dockerfile.uv -t penguins-uv:v1 .
docker run --rm penguins-conda:v1 > ../metrics-docker-conda.json
docker run --rm penguins-uv:v1 > ../metrics-docker-uv.json
diff ../metrics-ex1.json ../metrics-docker-conda.json
diff ../metrics-ex1.json ../metrics-docker-uv.json
```

- `analyze.py` prints the same JSON it writes to `metrics.json`, so each run's file is the container's `metrics.json`.
- `diff` prints nothing when the files match exactly.
- On Linux, `docker` needs root or membership in the `docker` group.

## Step 2: build and run with Podman

- Podman runs rootless, with no daemon, and reads the same `Dockerfile`.

```bash
podman build -f ../containers/Dockerfile.conda -t penguins-conda:v1 .
podman build -f ../containers/Dockerfile.uv -t penguins-uv:v1 .
podman run --rm penguins-conda:v1 > ../metrics-podman-conda.json
podman run --rm penguins-uv:v1 > ../metrics-podman-uv.json
diff ../metrics-ex1.json ../metrics-podman-conda.json
diff ../metrics-ex1.json ../metrics-podman-uv.json
```

- The recipes put the registry in each image name, `docker.io/condaforge/miniforge3` and `ghcr.io/astral-sh/uv`. Without `docker.io/`, Podman 4.9.3 on Ubuntu stopped with `short-name ... did not resolve to an alias`.
- Rootless, the conda build printed warnings such as `can't raise ambient capability CAP_CHOWN`. The build still succeeded.
- Rootless Podman keeps images in your home folder, under `~/.local/share/containers`, so check your quota.

## Step 3: run with Apptainer

- Apptainer runs as you, in your current folder.
- So `apptainer exec IMAGE.sif python analyze.py` runs your `analyze.py` on your `data`, with the container's environment, and writes `metrics.json` in your folder.

**From the Docker or Podman image.** Save the image to one file and convert it to a SIF:

```bash
docker save -o ../penguins-conda.tar penguins-conda:v1
docker save -o ../penguins-uv.tar penguins-uv:v1
apptainer build ../penguins-conda.sif docker-archive://../penguins-conda.tar
apptainer build ../penguins-uv.sif docker-archive://../penguins-uv.tar
```

- With Podman, save with `podman save --format docker-archive -o ...` and convert the same way.

**Without Docker or Podman.** Build the SIF from the `.def` file, which does the same steps as the `Dockerfile`:

```{literalinclude} containers/penguins-conda.def
```

```{literalinclude} containers/penguins-uv.def
```

```bash
apptainer build --fakeroot ../penguins-conda.sif ../containers/penguins-conda.def
apptainer build --fakeroot ../penguins-uv.sif ../containers/penguins-uv.def
```

**Run and compare**, for either kind of SIF:

```bash
apptainer exec ../penguins-conda.sif python analyze.py > ../metrics-apptainer-conda.json
apptainer exec ../penguins-uv.sif python analyze.py > ../metrics-apptainer-uv.json
diff ../metrics-ex1.json ../metrics-apptainer-conda.json
diff ../metrics-ex1.json ../metrics-apptainer-uv.json
sha256sum ../penguins-*.sif
```

- A SIF is one file. Copy it to a cluster and run it there with the same `apptainer exec` command.
- As [the GPU container page](../../gpu/container.md) found, converting the same image twice can give SIFs with different hashes. Keep the SIF you ran, or at least its hash.

## Recorded runs

- **Recorded November 8, 2026, on aarch64, NVIDIA DGX Spark, Ubuntu 24.04.5, Linux 7.0.0, with Docker 29.6.2, Podman 4.9.3 rootless and Apptainer 1.5.5.** The locks were `explicit-linux-aarch64.txt` and `uv.lock`, from Exercise 1 on that machine.
- **Recorded November 8, 2026, on x86_64, Windows 11 with WSL2, Ubuntu 24.04.1, with Apptainer 1.4.5.** That machine has no Docker or Podman, so both SIFs came from the `.def` files. The locks were `explicit-linux-64.txt`, made there with Exercise 1's steps, and the same `uv.lock` as on the ARM machine, byte for byte.
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

| Step | aarch64, Linux | x86_64, WSL2 |
|---|---|---|
| `docker build` and `docker run`, conda | Ran and matched. 1.03 GB image, 7 s build | Not run, no Docker |
| `docker build` and `docker run`, uv | Ran and matched. 282 MB image, 3 s build | Not run, no Docker |
| `podman build` and `podman run`, rootless, conda | Ran and matched. 1.06 GB image, 14 s build | Not run, no Podman |
| `podman build` and `podman run`, rootless, uv | Ran and matched. 288 MB image, 4 s build | Not run, no Podman |
| SIF from `docker-archive://`, Docker's or Podman's, conda | Ran and matched. 320 MB SIF, 20 to 28 s to save and convert | Not run |
| SIF from `docker-archive://`, Docker's or Podman's, uv | Ran and matched. 87 MB SIF, 5 to 7 s to save and convert | Not run |
| SIF from `penguins-conda.def` | Ran and matched. 320 MB SIF, 21 s build | Ran and matched. 331 MB SIF, 23 s build |
| SIF from `penguins-uv.def` | Ran and matched. 87 MB SIF, 5 s build | Ran and matched. 89 MB SIF, 6 s build |

- Build times include pulling the base image, except Docker's, which had it already. They depend on your network.
- The conda image is almost four times the uv image, because the Miniforge base image alone is about 600 MB.

## Clean up

- When you're done, remove what you made:

```bash
docker rmi penguins-conda:v1 penguins-uv:v1
podman rmi penguins-conda:v1 penguins-uv:v1
rm ../penguins-*.tar ../penguins-*.sif ../metrics-*.json
```

- The base images stay. `docker image ls` and `podman image ls` list them, and `docker rmi IMAGE_ID` removes one.

## On a Mac or Windows PC

- Docker Desktop, Podman Desktop and the other Mac tools run a Linux VM. The VM's memory and disk come out of your machine's, and its settings set how much.
- On a Mac with Apple silicon, the containers are Linux on ARM, so they use the `linux-aarch64` lock.
- On Windows, keep the project in your WSL2 home, not under `/mnt/c`, and run the commands in the WSL2 terminal.
