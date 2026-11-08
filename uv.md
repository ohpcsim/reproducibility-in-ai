---
title: The uv route
---

- uv manages Python, virtual environments and packages from PyPI.
- It is very fast at resolving and installing Python packages. See [uv's benchmarks](https://docs.astral.sh/uv/#highlights).
- It downloads Python itself, so this route needs neither conda nor a system Python.
- `pyproject.toml` declares the packages. `uv.lock` records their versions and hashes in one cross-platform file.
- conda also handles non-Python packages, including R, C/C++ libraries, CUDA, MPI and GDAL. That's why the exercises lead with conda.
- Binder stays on conda. This route is for your own machine.

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
- Each exercise pins Python 3.12.12 in `.python-version` and requires Python 3.12 in `pyproject.toml`.
- Its uv configuration requires managed Python. `uv sync --locked` downloads that Python, builds `.venv` and installs the locked packages.
- The lock chooses wheels for your platform. The target platforms are Linux x86_64 and aarch64, and macOS Intel and Apple silicon.

- DVC requires ANTLR 4.9.3, which has no PyPI wheel. uv builds this pure Python dependency from its source archive. It needs no C/C++ compiler.
- The DataOps and registry configurations constrain cryptography below 49 to keep Intel macOS wheels available.

## Get an exercise

- Pick one block below. Each clones a separate exercise branch.
- Run the block from the folder where you keep your work.
- Exercise 2, Workflows with Snakemake, gets its uv setup when it lands.

### Exercise 1: GitOps

```bash
git clone --branch binder-01-gitops --single-branch https://github.com/ohpcsim/reproducibility-in-ai.git gitops
cd gitops
uv sync --locked
uv run python scripts/setup_project.py --uv
cd project
```

- Follow the GitOps variant below. It replaces the conda steps on the [main exercise page](exercises/01-gitops/gitops.ipynb).
- `gitops/.venv` holds the exercise tools. `gitops/project/.venv` will hold the CO2 project's environment.
- To start over, from `gitops` run `uv run python scripts/setup_project.py --uv --reset`. This deletes your work and the local stand-in remote.

### Exercise 3: DataOps

```bash
git clone --branch binder-03-dataops --single-branch https://github.com/ohpcsim/reproducibility-in-ai.git dataops
cd dataops
uv sync --locked
source .venv/bin/activate
uv run python scripts/setup_project.py
cd project
```

- Continue at step 1 on the [DataOps page](exercises/03-dataops/dataops.ipynb).

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

### Exercise 5: LLM documentation

```bash
git clone --branch binder-05-llm --single-branch https://github.com/ohpcsim/reproducibility-in-ai.git llm
cd llm
uv sync --locked
source .venv/bin/activate
uv run python scripts/setup_project.py
cd project
```

- Continue at step 1 on the [LLM documentation page](exercises/05-llm/llm.ipynb).
- For exercises 3 to 5, activation puts Python, DVC and GTO on your path. The page's own commands then work as written.
- If you reopen a terminal, go to the exercise folder, run `source .venv/bin/activate`, then `cd project`.
- Check your setup with `python ../check.py --short`. Failures on the starter project are expected.

## GitOps with uv

- Run these commands from `gitops/project`, after the setup above.
- This is the same CO2 project, history, missing dependency and stale result as the conda lesson.
- This route commits `pyproject.toml` and `uv.lock`, instead of `environment.yml` and `explicit-<platform>.txt`.

### Step 1: make it run

**Problem**

- The README says to run the analysis, and it fails because pandas is missing.

```bash
uv run python analyze.py
```

**Facts**

- `uv run` builds the project's environment before running the command.
- The starter `pyproject.toml` does not declare pandas.
- Installing pandas somewhere else does not declare it here.
- `uv add pandas` declares it, updates `uv.lock` and installs it into `project/.venv`.
- One `uv.lock` covers the supported platforms. There is no separate explicit lock per platform.

**Steps**

1. Declare the package, inspect the declaration and commit both files.

```bash
uv add pandas
git diff pyproject.toml
git add pyproject.toml uv.lock
git commit -m "Declare pandas and lock the environment"
```

2. Run the analysis, inspect the changed number and undo it. Don't commit `metrics.json` yet.

```bash
uv run python analyze.py
git diff metrics.json
git restore metrics.json
```

3. Check the short path.

```bash
uv run python ../check.py --short
```

- On the untouched starter, the check reports three failures and `0 of 3 parts pass.`
- After step 1, it checks that the committed declaration and lock cover every import, that `.venv` matches the lock, and that a clean clone runs.
- When it passes, that's the end of the short path.

### Step 2, optional: find out why the number moved

**Problem**

- A rerun does not reproduce the committed `metrics.json`.
- The unit tests pass anyway.

```bash
uv run python check_fresh.py
uv run python -m pytest -q
```

**Facts**

- One commit changed a parameter without rerunning the analysis.
- `git bisect run` finds the first failing commit.
- Bisect checks out old dependency files too. Keep the current environment active during the search, so it does not change at each commit.
- The holdout comparison scores years the fit never saw. Choosing the degree is your decision.

**Steps**

1. Activate the project environment, find the commit, note its ID and end the search.

```bash
source .venv/bin/activate
git bisect start HEAD $(git rev-list --max-parents=0 HEAD)
git bisect run python check_fresh.py
git bisect reset
```

2. Read that commit with `git show COMMIT_ID`, using the ID bisect found. Read the holdout table.

```bash
uv run python holdout.py
```

3. Edit `params.yaml` to set a degree you can defend. Rerun and stage the result.

```bash
uv run python analyze.py
git add params.yaml metrics.json
uv run python check_fresh.py
```

4. Commit with the ID, the degree and your reason. Replace the placeholder text.

```bash
git commit -m "REPLACE THIS with the commit ID bisect found, the degree you chose, and why"
```

5. Install the hook. It uses `python` from the environment you activated.

```bash
cp hooks/pre-commit .git/hooks/pre-commit
```

6. Change `degree` again, save it, then try a stale commit. The hook should refuse it. Restore the file afterward.

```bash
git add params.yaml
git commit -m "Try to commit a stale number"
git restore --staged params.yaml
git restore params.yaml
```

### Step 3, optional: delete everything that runs it

**Problem**

- A working laptop alone is not enough. Someone else needs to rebuild the environment and reproduce the result.

**Facts**

- `remote/co2.git` stands in for GitHub. These pushes stay on your own machine.
- Push before deleting the clone.
- Deleting `project` deletes its `.venv` too. The exercise tools in `gitops/.venv` remain.
- `uv sync --locked` rebuilds from the committed lock and refuses an outdated lock.
- A clone does not carry hooks. Install the hook again.

**Steps**

1. Push, leave the active environment, delete the clone and its environment, and clone again.

```bash
git push origin main
deactivate
cd ..
rm -rf project
git clone --config user.name="Workshop Learner" --config user.email="learner@example.org" remote/co2.git project
cd project
uv sync --locked
source .venv/bin/activate
uv run python analyze.py
git status --short
```

- `git status --short` should print nothing.

2. Tag the release and install the hook again.

```bash
git tag -a v1.0 -m "Publication version"
git push origin v1.0
cp hooks/pre-commit .git/hooks/pre-commit
```

3. Check everything.

```bash
uv run python ../check.py --short
uv run python ../check.py
```

- The checker detects the committed `pyproject.toml` and checks `uv.lock` for this route.
- The full check also rebuilds a new environment from a fresh clone of tag `v1.0`.
- It keeps the salted growth-rate digest. It does not contain a readable answer key.

## Binder keeps its conda environment

- Each exercise has a `.binder/` folder.
- repo2docker reads configuration there and ignores configuration at the repository root when that folder exists. See [where to put configuration files](https://repo2docker.readthedocs.io/en/latest/use/repository.html#where-to-put-configuration-files-in-a-repository).
- The new root `pyproject.toml`, `uv.lock` and `.python-version` do not change Binder's environment.
