---
title: Tools and documentation
---

- This page lists every tool the exercises and the optional pages use.
- Each row says what the tool is, where the workshop uses it, and where its official documentation and introduction are.
- You don't install these one by one. Each exercise's environment file installs what it needs, and [Set up your environment](setup.md) has the steps.

## Code and tests

| Tool | What it is | Where we use it | Documentation | Start here |
|---|---|---|---|---|
| Git | Version control. It records each change to a project as a commit. | Every exercise. | [Reference](https://git-scm.com/docs) | [About version control](https://git-scm.com/book/en/v2/Getting-Started-About-Version-Control), from the Pro Git book |
| GitHub | A service that hosts Git repositories. | This site's repository. Binder builds each exercise from its branch there. | [GitHub Docs](https://docs.github.com/en) | [Hello World](https://docs.github.com/en/get-started/using-github/hello-world) |
| pytest | Runs Python tests. | Exercises [4](exercises/04-registry/registry.ipynb) and [5](exercises/05-llm/llm.ipynb). | [pytest documentation](https://docs.pytest.org/en/stable/) | [Get started](https://docs.pytest.org/en/stable/getting-started.html) |

## Environments

| Tool | What it is | Where we use it | Documentation | Start here |
|---|---|---|---|---|
| conda | A package and environment manager. It builds an environment from `environment.yml`, with Python and non-Python packages. | Every exercise, [1c](gpu/gpu.md) and [the container page](gpu/container.md). | [Conda documentation](https://docs.conda.io/projects/conda/en/latest/) | [Getting started with conda](https://docs.conda.io/projects/conda/en/latest/user-guide/getting-started.html) |
| Miniforge | A small conda installer that gets its packages from conda-forge. | [Set up your environment](setup.md), step 2. | [README](https://github.com/conda-forge/miniforge) | The README has the install steps. |
| conda-forge | A community channel of conda packages. | Every environment file in the workshop lists it as the only channel. | [conda-forge documentation](https://conda-forge.org/docs/) | [A brief introduction](https://conda-forge.org/docs/user/introduction/) |
| uv | A Python package and project manager, written in Rust. | [Exercise 1](exercises/01-environments/environments.ipynb), [1c](gpu/gpu.md) and [the uv route](uv.md). | [uv documentation](https://docs.astral.sh/uv/) | [Getting started](https://docs.astral.sh/uv/getting-started/) |

## conda and uv

- conda is the established choice in research computing.
- uv is newer and growing fast. In its first year, 11% of surveyed Python developers used it, in the Python Developers Survey 2024 by JetBrains and the Python Software Foundation, published August 2025. ([The State of Python 2025](https://blog.jetbrains.com/pycharm/2025/08/the-state-of-python-2025/), [heise's coverage](https://www.heise.de/en/news/Rust-becomes-Python-s-performance-co-pilot-10560471.html))

| | Pros | Cons |
|---|---|---|
| conda | Any language: Python, R, C/C++ libraries, CUDA, MPI. conda-forge, a large community channel. Established on HPC systems. | Slower than uv. One lock file per platform. Large environments. |
| uv | Very fast. One cross-platform lock file, `uv.lock`. Installs Python itself. Uses the standard `pyproject.toml`. | Python and PyPI packages only. Non-Python libraries come from the system or from wheels. Newer, and less familiar on HPC systems. |

The workshop uses conda. [The uv route](uv.md) shows the same exercises with uv.

## Workflows

| Tool | What it is | Where we use it | Documentation | Start here |
|---|---|---|---|---|
| Snakemake | A workflow manager. You declare rules with inputs and outputs, and it runs the steps whose outputs are missing or out of date. | [Exercise 2](exercises/02-workflows/workflows.ipynb). | [Snakemake documentation](https://snakemake.readthedocs.io/en/stable/) | [Tutorial](https://snakemake.readthedocs.io/en/stable/tutorial/tutorial.html) |
| Nextflow | Another workflow manager. | Not in the exercises. It's an alternative to Snakemake. | [Nextflow documentation](https://docs.seqera.io/nextflow/) | [Nextflow training](https://training.nextflow.io/latest/) |

## Data and models

| Tool | What it is | Where we use it | Documentation | Start here |
|---|---|---|---|---|
| DVC | Data Version Control. Git keeps small pointer files, and the data goes to a separate store. | Exercises [3](exercises/03-dataops/dataops.ipynb) and [4](exercises/04-registry/registry.ipynb). | [DVC documentation](https://doc.dvc.org/) | [Get started](https://doc.dvc.org/start) |
| Git LFS | A Git extension that keeps large files on a separate server and leaves pointers in the repository. | Not used. Git LFS needs a server. DVC, in [exercise 3](exercises/03-dataops/dataops.ipynb), doesn't. | [Documentation](https://github.com/git-lfs/git-lfs/tree/main/docs) | [Getting started](https://git-lfs.com/), on the home page |
| GTO | Git Tag Ops. It records model versions and stages as Git tags, so the registry lives in the repository. | [Exercise 4](exercises/04-registry/registry.ipynb). | [GTO documentation](https://mlem.ai/doc/gto) | [Get started](https://mlem.ai/doc/gto/get-started) |
| OSN | The Open Storage Network, object storage for research data that you reach from laptops, clusters and cloud platforms. | Exercises [3](exercises/03-dataops/dataops.ipynb) and [4](exercises/04-registry/registry.ipynb) use a local folder that stands in for an OSN bucket. | [OSN user documentation](https://openstoragenetwork.github.io/docs/) | [Why use OSN?](https://openstoragenetwork.github.io/docs/why-osn/) |
| pandas | Data tables for Python. | [Exercise 3](exercises/03-dataops/dataops.ipynb). In [exercise 1](exercises/01-environments/environments.ipynb), the project imports it without declaring it, and you declare it. | [pandas documentation](https://pandas.pydata.org/docs/) | [Getting started](https://pandas.pydata.org/docs/getting_started/index.html) |
| scikit-learn | Machine learning for Python. | [Exercise 4](exercises/04-registry/registry.ipynb) trains its digit classifiers with it. | [scikit-learn documentation](https://scikit-learn.org/stable/) | [Getting started](https://scikit-learn.org/stable/getting_started.html) |
| PyTorch | Deep learning for Python, with GPU support. | [1c, PyTorch with a GPU](gpu/gpu.md) and [its container page](gpu/container.md). | [PyTorch documentation](https://docs.pytorch.org/docs/stable/) | [Learn the basics](https://docs.pytorch.org/tutorials/beginner/basics/intro.html) |

## Containers

| Tool | What it is | Where we use it | Documentation | Start here |
|---|---|---|---|---|
| Docker | Builds and runs containers through a daemon. | [The container page](gpu/container.md). | [Docker Docs](https://docs.docker.com/) | [Get started](https://docs.docker.com/get-started/) |
| Podman | Builds and runs containers with no daemon, and without root. It takes the same commands and Dockerfiles as Docker. | [The container page](gpu/container.md), with Podman. | [Podman documentation](https://docs.podman.io/en/latest/) | [Get started](https://podman.io/get-started), and the [rootless tutorial](https://github.com/podman-container-tools/podman/blob/main/docs/tutorials/rootless_tutorial.md) |
| Apptainer | Runs containers on HPC systems, from one SIF file, as your own user. Formerly Singularity. | [The container page](gpu/container.md). | [Apptainer user guide](https://apptainer.org/docs/user/latest/) | [Quick start](https://apptainer.org/docs/user/latest/quick_start.html) |
| NVIDIA NGC | NVIDIA's catalog of GPU container images, including PyTorch. | [The container page](gpu/container.md), with a pre-built image. | [NGC documentation](https://docs.nvidia.com/ngc/) | [NGC catalog](https://catalog.ngc.nvidia.com) |

## Containers on shared machines

- Docker runs a daemon, and using it usually needs root or membership in the `docker` group.
- Shared HPC and lab machines don't give users either one.
- Podman has no daemon and runs rootless. It accepts the same commands and Dockerfiles as Docker.
- Apptainer is the HPC standard. A container is one SIF file, it runs as your user, and there's no daemon.
- Apptainer is the original Singularity project, renamed when it joined the Linux Foundation, and it still provides a `singularity` command. Sylabs' separate fork, SingularityCE, reached end of life on October 25, 2026, and [its repository](https://github.com/sylabs/singularity) is archived. If your site still says Singularity, use Apptainer. ([CIQ's announcement](https://ciq.com/blog/singularityce-end-of-life-apptainer))
- A container that needs the GPU gets it through NVIDIA's tools: `--gpus all` in Docker, a CDI spec in Podman, and `--nv` in Apptainer. ([NVIDIA's CDI guide](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/cdi-support.html))

| Where you are | What to use |
|---|---|
| Your own machine | Docker or Podman |
| A shared Linux machine without root | Podman, if it's installed, or Apptainer |
| An HPC cluster | Apptainer |

[The container page](gpu/container.md) has each route, with recorded output.

## Documentation and Binder

| Tool | What it is | Where we use it | Documentation | Start here |
|---|---|---|---|---|
| Jupyter Book (mystmd) | Builds a website from Markdown files and notebooks. Jupyter Book 2 runs on mystmd, the MyST Markdown tools. | This site. Each exercise page is a notebook that reruns when the site is published. | [Jupyter Book](https://jupyterbook.org/stable/), [MyST guide](https://mystmd.org/guide) | [Get started with MyST](https://mystmd.org/guide/quickstart) |
| JupyterLab | A browser interface for notebooks, terminals and files. | Binder sessions open in it, with a terminal and the exercise page side by side. | [JupyterLab documentation](https://jupyterlab.readthedocs.io/en/stable/) | [Get started](https://jupyterlab.readthedocs.io/en/stable/getting_started/overview.html) |
| Binder and mybinder.org | Opens a Git repository as a temporary session in your browser. mybinder.org is the free public service. | **Open in Binder** on each exercise. [Set up your environment](setup.md) explains how it works. | [Binder documentation](https://mybinder.readthedocs.io/en/latest/) | [Get started with Binder](https://mybinder.readthedocs.io/en/latest/introduction.html) |
| BinderHub | The service behind Binder. It builds the images and starts the sessions. | mybinder.org runs it. | [BinderHub documentation](https://binderhub.readthedocs.io/en/latest/) | [The BinderHub architecture](https://binderhub.readthedocs.io/en/latest/overview.html) |
| repo2docker | Builds a container image from a repository's configuration files. | It reads each exercise branch's `.binder/` folder. | [repo2docker documentation](https://repo2docker.readthedocs.io/en/latest/) | [Using source repositories](https://repo2docker.readthedocs.io/en/latest/use/repository/) |

## LLMs

- [The same task in five tools](tools/five-tools.md) shows Claude Code, Codex, Cursor, a local model and free models through OpenCode.
- For each tool, it has how to install and sign in, the exact command, what the tool wrote, and what the tests decided.
- [Exercise 5](exercises/05-llm/llm.ipynb) uses recordings of those runs, so you don't need any of the tools to do it.
