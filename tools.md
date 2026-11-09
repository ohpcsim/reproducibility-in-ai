---
title: Tools and documentation
---

- This page lists every tool the exercises and the optional pages use.
- Each row says what the tool is, where the workshop uses it, and where its official documentation and introduction are.
- You don't install these one by one. Each exercise's environment file installs what it needs, and your track's Set up page, from [the home page](index.md), has the steps.
- Exercise links on this page open the Binder copy. Links to 1b, 1c and 2b open the Linux copy unless the link names another track. Your track's menu has your machine's copy.

## Code

| Tool | What it is | Where we use it | Documentation | Start here |
|---|---|---|---|---|
| Git | Version control. It records each change to a project as a commit. | Every exercise. | [Reference](https://git-scm.com/docs) | [About version control](https://git-scm.com/book/en/v2/Getting-Started-About-Version-Control), from the Pro Git book |
| GitHub | A service that hosts Git repositories. | This site's repository. Binder builds each exercise from its branch there. | [GitHub Docs](https://docs.github.com/en) | [Hello World](https://docs.github.com/en/get-started/using-github/hello-world) |

## Environments

| Tool | What it is | Where we use it | Documentation | Start here |
|---|---|---|---|---|
| conda | A package and environment manager. It builds an environment from `environment.yml`, with Python and non-Python packages. | Every exercise, [1c](gpu/gpu.md) and [the container page](gpu/container.md). | [Conda documentation](https://docs.conda.io/projects/conda/en/latest/) | [Getting started with conda](https://docs.conda.io/projects/conda/en/latest/user-guide/getting-started.html) |
| Miniforge | A small conda installer that gets its packages from conda-forge. | Your track's Set up page, from [the home page](index.md), step 2 on the Mac, Linux, WSL2 and HPC tracks. | [README](https://github.com/conda-forge/miniforge) | The README has the install steps. |
| conda-forge | A community channel of conda packages. | Every environment file lists it first. Exercise 2's files add bioconda. | [conda-forge documentation](https://conda-forge.org/docs/) | [A brief introduction](https://conda-forge.org/docs/user/introduction/) |
| uv | A Python package and project manager, written in Rust. | [Exercise 1](exercises/01-environments/environments-linux.ipynb), [1c](gpu/gpu.md), and the "With uv instead of conda" option in Exercises 2a, 3 and 4. | [uv documentation](https://docs.astral.sh/uv/) | [Getting started](https://docs.astral.sh/uv/getting-started/) |

## conda and uv

- conda is the established choice in research computing.
- uv is newer and growing fast. In its first year, 11% of surveyed Python developers used it, in the Python Developers Survey 2024 by JetBrains and the Python Software Foundation, published August 2025. ([The State of Python 2025](https://blog.jetbrains.com/pycharm/2025/08/the-state-of-python-2025/), [heise's coverage](https://www.heise.de/en/news/Rust-becomes-Python-s-performance-co-pilot-10560471.html))

| | Pros | Cons |
|---|---|---|
| conda | Any language: Python, R, C/C++ libraries, CUDA, MPI. conda-forge, a large community channel. Established on HPC systems. | Slower than uv. One lock file per platform. Large environments. |
| uv | Very fast. One cross-platform lock file, `uv.lock`. Installs Python itself. Uses the standard `pyproject.toml`. | Python packages only. Non-Python libraries come from the system or from wheels. Newer, and less familiar on HPC systems. |

1a and 1c teach both. Exercises 2a, 3 and 4 use conda and give the same steps with uv. 2b uses conda, which installs Nextflow and Java.

## Workflows

| Tool | What it is | Where we use it | Documentation | Start here |
|---|---|---|---|---|
| Snakemake | A workflow manager. You declare rules with inputs and outputs, and it runs the steps whose outputs are missing or out of date. | [2a. Snakemake](exercises/02-workflows/workflows-linux.ipynb): you add a step to a working Snakefile. | [Snakemake documentation](https://snakemake.readthedocs.io/en/stable/) | [Tutorial](https://snakemake.readthedocs.io/en/stable/tutorial/tutorial.html) |
| Nextflow | Another workflow manager. | [2b. Nextflow](exercises/02-workflows/nextflow.md), outside Binder: you add a process to a working `main.nf`. It's an alternative to Snakemake. | [Nextflow documentation](https://docs.seqera.io/nextflow/) | [Nextflow training](https://training.nextflow.io/latest/) |

## Data and models

| Tool | What it is | Where we use it | Documentation | Start here |
|---|---|---|---|---|
| DVC | Data Version Control. Git keeps small pointer files, and the data goes to a separate store. | Exercises [3](exercises/03-dataops/dataops-linux.ipynb) and [4](exercises/04-registry/registry-linux.ipynb). | [DVC documentation](https://doc.dvc.org/) | [Get started](https://doc.dvc.org/start) |
| Git LFS | A Git extension that keeps large files on a separate server and leaves pointers in the repository. | Not used. Git LFS needs a server. DVC, in [Exercise 3](exercises/03-dataops/dataops-linux.ipynb), doesn't. | [Documentation](https://github.com/git-lfs/git-lfs/tree/main/docs) | [Getting started](https://git-lfs.com/), on the home page |
| GTO | Git Tag Ops. It records model versions and stages as Git tags, so the registry lives in the repository. | [Exercise 4](exercises/04-registry/registry-linux.ipynb). | [GTO documentation](https://mlem.ai/doc/gto) | [Get started](https://mlem.ai/doc/gto/get-started) |
| OSN | The Open Storage Network, object storage for research data that you reach from laptops, clusters and cloud platforms. | Exercises [3](exercises/03-dataops/dataops-linux.ipynb) and [4](exercises/04-registry/registry-linux.ipynb) use a local folder that stands in for an OSN bucket. | [OSN user documentation](https://openstoragenetwork.github.io/docs/) | [Why use OSN?](https://openstoragenetwork.github.io/docs/why-osn/) |
| pandas | Data tables for Python. | Exercises 2 to 4 read and summarize the penguin table with it. In [Exercise 1](exercises/01-environments/environments-linux.ipynb), the project imports it without declaring it, and you declare it. | [pandas documentation](https://pandas.pydata.org/docs/) | [Getting started](https://pandas.pydata.org/docs/getting_started/index.html) |
| scikit-learn | Machine learning for Python. | [Exercise 4](exercises/04-registry/registry-linux.ipynb) trains its penguin sex classifier with it. | [scikit-learn documentation](https://scikit-learn.org/stable/) | [Getting started](https://scikit-learn.org/stable/getting_started.html) |
| PyTorch | Deep learning for Python, with GPU support. | [1c, PyTorch with a GPU](gpu/gpu.md) and [its container page](gpu/container.md). | [PyTorch documentation](https://docs.pytorch.org/docs/stable/) | [Learn the basics](https://docs.pytorch.org/tutorials/beginner/basics/intro.html) |

## Containers

| Tool | What it is | Where we use it | Documentation | Start here |
|---|---|---|---|---|
| Podman | Builds and runs containers from Dockerfiles, with no daemon and without root. | [1b](exercises/01-environments/containers.md) on the Mac, Linux and WSL2 tracks. | [Podman documentation](https://docs.podman.io/en/latest/) | [Get started](https://podman.io/get-started), and the [rootless tutorial](https://github.com/podman-container-tools/podman/blob/main/docs/tutorials/rootless_tutorial.md) |
| Apptainer | Runs containers on HPC systems, from one SIF file, as your own user. Formerly Singularity. | [1b](exercises/01-environments/containers-hpc.md) on the HPC track, and [the GPU container page](gpu/container-hpc.md). It builds from its own recipe, a `.def` file. | [Apptainer user guide](https://apptainer.org/docs/user/latest/) | [Quick start](https://apptainer.org/docs/user/latest/quick_start.html) |
| NVIDIA NGC | NVIDIA's catalog of GPU container images, including PyTorch. | Not used here. Its PyTorch images are an alternative to building your own on [the GPU container page](gpu/container.md). | [NGC documentation](https://docs.nvidia.com/ngc/) | [NGC catalog](https://catalog.ngc.nvidia.com) |

## Containers on shared machines

- Shared HPC and lab machines don't give users root.
- Podman has no daemon and runs rootless. It builds from Dockerfiles.
- Why Podman and not Docker: Docker Desktop needs a paid plan in larger organizations. Podman is free and open source, runs without root or a daemon, and takes the same commands.
- Apptainer is the HPC standard. A container is one SIF file, it runs as your user, and there's no daemon.
- Apptainer is the original Singularity project, renamed when it joined the Linux Foundation, and it still provides a `singularity` command. Sylabs' separate fork, SingularityCE, reached end of life on October 25, 2026, and [its repository](https://github.com/sylabs/singularity) is archived. If your site still says Singularity, use Apptainer. ([CIQ's announcement](https://ciq.com/blog/singularityce-end-of-life-apptainer))
- A container that needs the GPU gets the host's NVIDIA driver through Apptainer's `--nv`. On WSL2, `--nv` alone didn't reach the GPU. [The WSL2 container page](gpu/container-wsl2.md) binds `/usr/lib/wsl` instead.

- We cover Linux containers. They need a Linux kernel, so a Mac or Windows PC runs them in a VM.

| Where you are | What to use | Why | What we ran |
|---|---|---|---|
| Your Mac | Podman Desktop | It runs a small Linux VM. (Darwin containers such as [rund](https://github.com/darwin-containers/rund) run macOS software natively; not covered here) | Podman 6.1.4 through Podman Desktop (libkrun VM, 5 CPU, 2 GiB), macOS arm64 |
| Your Windows PC | Podman inside WSL2 for 1b, Apptainer for 1c | WSL2 provides the Linux kernel | Rootless Podman 4.9.3 and Apptainer 1.4.5 in WSL2, x86_64 |
| Your own Linux machine | Podman for 1b, Apptainer for 1c | Both run as you, with no daemon. Apptainer reaches the GPU with `--nv` | Rootless Podman 4.9.3 and Apptainer 1.5.5, aarch64 |
| A shared Linux machine, without root | Apptainer, for 1b and 1c | It needs no root or daemon | Apptainer 1.5.5, without sudo, on the aarch64 machine. It isn't shared |
| An HPC cluster | Apptainer | It runs as you, with no daemon. The image is one SIF file, with no registry needed. It works with the scheduler, MPI and GPUs | Not run |
| Binder | None | The session is already a container | Nothing to run |

- 1b builds Exercise 1's conda and uv environments [with Podman](exercises/01-environments/containers.md), or [with Apptainer](exercises/01-environments/containers-hpc.md) on a shared machine or cluster, with recorded output. "What we ran" is from there.
- [The GPU container page](gpu/container.md) does the same for PyTorch with CUDA.

## Documentation and Binder

| Tool | What it is | Where we use it | Documentation | Start here |
|---|---|---|---|---|
| Jupyter Book (mystmd) | Builds a website from Markdown files and notebooks. Jupyter Book 2 runs on mystmd, the MyST Markdown tools. | This site. The exercise notebooks rerun when the site is published. [How this site is built](build.md) has the details. | [Jupyter Book](https://jupyterbook.org/stable/), [MyST guide](https://mystmd.org/guide) | [Get started with MyST](https://mystmd.org/guide/quickstart) |
| JupyterLab | A browser interface for notebooks, terminals and files. | Binder sessions open in it, with a terminal and the exercise page side by side. | [JupyterLab documentation](https://jupyterlab.readthedocs.io/en/stable/) | [Get started](https://jupyterlab.readthedocs.io/en/stable/getting_started/overview.html) |
| Binder and mybinder.org | Opens a Git repository as a temporary session in your browser. mybinder.org is the free public service. | **Launch in Binder** on each exercise card and on [the Binder page](setup.md). [How this site is built](build.md#binder) explains how it works. | [Binder documentation](https://mybinder.readthedocs.io/en/latest/) | [Get started with Binder](https://mybinder.readthedocs.io/en/latest/introduction.html) |
| BinderHub | The service behind Binder. It builds the images and starts the sessions. | mybinder.org runs it. | [BinderHub documentation](https://binderhub.readthedocs.io/en/latest/) | [The BinderHub architecture](https://binderhub.readthedocs.io/en/latest/overview.html) |
| repo2docker | Builds a container image from a repository's configuration files. | It reads each exercise branch's `.binder/` folder. | [repo2docker documentation](https://repo2docker.readthedocs.io/en/latest/) | [Using source repositories](https://repo2docker.readthedocs.io/en/latest/use/repository/) |
