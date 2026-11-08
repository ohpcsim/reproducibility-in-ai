---
title: The uv route
---

- uv manages Python, virtual environments and packages from PyPI.
- It is very fast at resolving and installing Python packages. See [uv's benchmarks](https://docs.astral.sh/uv/#highlights).
- It downloads Python itself, so this route needs neither conda nor a system Python.
- `pyproject.toml` declares the packages. `uv.lock` records their versions and hashes in one cross-platform file.
- conda also handles non-Python packages, including R, C/C++ libraries, CUDA, MPI and GDAL. That's why the exercises lead with conda.
- Binder stays on conda. This route is for your own machine. Exercise 1's Binder session includes uv, for the exercise's uv step.

## Install uv and Git

- Open a terminal on Linux or macOS. On Windows, use Ubuntu through WSL2, as described in [setup](setup.md).
- On Windows, keep the exercises in your WSL2 home, not under `/mnt/c`.
- Run the [official uv installer](https://docs.astral.sh/uv/getting-started/installation/):

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source "$HOME/.local/bin/env"
uv --version
```

- Git comes from your system. uv does not install Git.
- Check before you start:

```bash
git --version
```

- If Git is missing, use `sudo apt install git` on Ubuntu or `xcode-select --install` on macOS.
- Exercises 2 to 4 each pin Python 3.12.12 in `.python-version` and require Python 3.12 in `pyproject.toml`.
- Their uv configuration requires managed Python. `uv sync --locked` downloads that Python, builds `.venv` and installs the locked packages.
- The lock chooses wheels for your platform. The target platforms are Linux x86_64 and aarch64, and macOS Intel and Apple silicon.

- DVC requires ANTLR 4.9.3, which has no PyPI wheel. uv builds this pure Python dependency from its source archive. It needs no C/C++ compiler.
- Snakemake requires connection-pool 0.0.3, which also has no PyPI wheel. uv builds it from its pure Python source archive.
- The DataOps and registry configurations constrain cryptography below 49 to keep Intel macOS wheels available.

## Get an exercise

- Pick one block below. Each clones a separate exercise branch.
- Run the block from the folder where you keep your work.

### Exercise 1: Software environments

- uv is part of the lesson. The [exercise page](exercises/01-environments/environments.ipynb) does the same task with conda and then with uv.
- Its setup uses conda, because the first step needs it.

### Exercise 2: Workflows

```bash
git clone --branch binder-02-workflows --single-branch https://github.com/ohpcsim/reproducibility-in-ai.git workflows
cd workflows
uv sync --locked
source .venv/bin/activate
uv run python scripts/setup_project.py
cd project
```

- Continue at step 1 on the [Workflows page](exercises/02-workflows/workflows.ipynb).

### Exercise 3: Versioning data

```bash
git clone --branch binder-03-dataops --single-branch https://github.com/ohpcsim/reproducibility-in-ai.git dataops
cd dataops
uv sync --locked
source .venv/bin/activate
uv run python scripts/setup_project.py
cd project
```

- Continue at step 1 on the [Versioning data page](exercises/03-dataops/dataops.ipynb).

### Exercise 4: model registry

```bash
git clone --branch binder-04-registry --single-branch https://github.com/ohpcsim/reproducibility-in-ai.git registry
cd registry
uv sync --locked
source .venv/bin/activate
uv run python scripts/setup_project.py
cd project
```

- Continue at step 1 on the [model registry page](exercises/04-registry/registry.ipynb).

- For exercises 2 to 4, activation puts Python, Snakemake, DVC and GTO on your path. The page's own commands then work as written.
- If you reopen a terminal, go to the exercise folder, run `source .venv/bin/activate`, then `cd project`.
- Check your setup with `python ../check.py --short`. Failures on the starter project are expected.

## Binder keeps its conda environment

- Each exercise has a `.binder/` folder.
- repo2docker reads configuration there and ignores configuration at the repository root when that folder exists. See [where to put configuration files](https://repo2docker.readthedocs.io/en/latest/use/repository.html#where-to-put-configuration-files-in-a-repository).
- In exercises 2 to 4, the root `pyproject.toml`, `uv.lock` and `.python-version` do not change Binder's environment.
