---
title: Set up your environment
---

- Each exercise needs a terminal, Git and the packages in its environment file.

+++ {"tags": ["track-binder"]}

- You get them in your browser with Binder.

+++

- You read the exercise pages on this site and paste the commands into the terminal.
- You don't need Jupyter or a GPU.
- [Tools and documentation](tools.md) lists each tool, with links to its documentation.

+++ {"tags": ["track-binder"]}

## Binder and BinderHub: how it works

- A Binder is a Git repository with code or content to run, and configuration files that declare its environment. ([What is a Binder?](https://mybinder.readthedocs.io/en/latest/introduction.html#what-is-a-binder))
- repo2docker reads those files and builds a container image from them. ([repo2docker](https://repo2docker.readthedocs.io/en/latest/))
- repo2docker looks for the files in a `binder/` or `.binder/` folder first. If that folder exists, it ignores configuration files in the root of the repository. ([Where to put configuration files](https://repo2docker.readthedocs.io/en/latest/use/repository.html#where-to-put-configuration-files-in-a-repository))
- BinderHub is the service that builds the images and serves them. It uses repo2docker to build, a Docker registry to store the images, Kubernetes to manage the cloud machines, and JupyterHub to run a temporary container for each user. ([The BinderHub architecture](https://binderhub.readthedocs.io/en/latest/overview.html))
- mybinder.org is a free public service. It's a federation of BinderHub deployments that the Binder community maintains, and it has limited resources. ([What is mybinder.org?](https://mybinder.readthedocs.io/en/latest/introduction.html#what-is-mybinder-org), [Is mybinder.org free to use?](https://mybinder.readthedocs.io/en/latest/about/user-guidelines.html#is-mybinder-org-free-to-use))

### What's in each exercise branch

Each exercise branch has three files in `.binder/`:

- `environment.yml` lists the conda packages. repo2docker installs them into its own base environment, not into one named `repro-environments`, so you don't run `conda activate` in Binder. ([environment.yml](https://repo2docker.readthedocs.io/en/latest/configuration/research.html))
- `postBuild` runs once, at build time, after the packages are installed. Ours builds the `project` folder, loads the JupyterLab layout and makes new terminals start in `project`. ([postBuild](https://repo2docker.readthedocs.io/en/latest/configuration/actions.html))
- `workspace.json` is the JupyterLab layout: a terminal on the left and the exercise page on the right. ([JupyterLab on Binder](https://jupyterlab.readthedocs.io/en/stable/user/binder.html#customize-the-layout))
- In exercises 2 to 4, the root `pyproject.toml`, `uv.lock` and `.python-version` do not change Binder's environment. See [where to put configuration files](https://repo2docker.readthedocs.io/en/latest/use/repository.html#where-to-put-configuration-files-in-a-repository).
- The branches have no `start` file, the script repo2docker would run each time a session starts. ([start](https://repo2docker.readthedocs.io/en/latest/configuration/actions.html))

### What happens when you open a link

Exercise 1's link is:

```text
https://mybinder.org/v2/gh/ohpcsim/reproducibility-in-ai/binder-01-environments?urlpath=lab/workspaces/exercise
```

- `gh/ohpcsim/reproducibility-in-ai` is the GitHub repository.
- `binder-01-environments` is the branch. Each exercise has its own branch, so each has its own image.
- `?urlpath=lab/workspaces/exercise` opens JupyterLab with the workspace named `exercise`, the terminal and the page side by side. ([Configure the user interface](https://mybinder.readthedocs.io/en/latest/howto/user_interface.html), [JupyterLab URLs](https://jupyterlab.readthedocs.io/en/stable/user/urls.html))

When you open it, BinderHub does this ([what happens when a user clicks a Binder link](https://binderhub.readthedocs.io/en/latest/overview.html#what-happens-when-a-user-clicks-a-binder-link), [what affects start time](https://mybinder.readthedocs.io/en/latest/about/user-guidelines.html#performance-and-speed)):

1. It checks whether an image exists for the branch's latest commit.
2. If not, it builds one with repo2docker and stores it in the registry. This is the slowest step. It happens the first time anyone opens the link after the branch changes.
3. If the machine that will run your session doesn't have the image yet, it pulls it from the registry. This can also take a while.
4. JupyterHub starts a container for you from the image. This usually takes seconds.

- Once a branch is built, later clicks don't rebuild it until someone pushes a change. ([Build your repository](https://mybinder.readthedocs.io/en/latest/introduction.html#build-your-repository))

### Session facts

- Each session gets at least 1 GB of memory and at most 2 GB. If it goes over 2 GB, its kernel restarts. ([Memory](https://mybinder.readthedocs.io/en/latest/about/user-guidelines.html#how-much-memory-am-i-given-when-using-binder))
- Binder shuts down a session after more than 10 minutes of inactivity. A JupyterLab window open in the foreground generally counts as activity. ([Session length](https://mybinder.readthedocs.io/en/latest/about/user-guidelines.html#how-long-will-my-binder-session-last))
- Binder aims to give each session up to six hours, or up to one CPU-hour for heavy computing. It doesn't guarantee a session runs longer than that. ([Session length](https://mybinder.readthedocs.io/en/latest/about/user-guidelines.html#how-long-will-my-binder-session-last))
- There's no persistent storage. Everything in a session is destroyed when you leave or it goes idle. ([Security](https://mybinder.readthedocs.io/en/latest/about/user-guidelines.html#an-overview-of-binder-s-security), [Privacy](https://mybinder.readthedocs.io/en/latest/about/user-guidelines.html#how-we-ensure-user-privacy))
- Download anything you want to keep.
- Never put passwords, API keys or data that shouldn't be public into a Binder session. The exercises don't need any. ([How secure is mybinder.org?](https://mybinder.readthedocs.io/en/latest/about/user-guidelines.html#how-secure-is-mybinder-org))
- The Binder team strongly discourages pushing from a Binder session to GitHub. ([Pushing from a session](https://mybinder.readthedocs.io/en/latest/about/user-guidelines.html#can-i-push-data-from-my-binder-session-back-to-my-repository))

### The same idea as the talk

- The environment is declared in the repository, and anyone can rebuild it from there.
- So the Binder session is cattle. When it ends, you lose nothing that's in the repository.
- Your work is the pet. Download it, or do the exercise on your own machine.

## Using Binder

1. On the [home page](index.md), select **Open in Binder** on an exercise. Each exercise page has the same link under "Get a terminal".
2. mybinder.org shows its progress while it builds or starts the session. The first start can take a few minutes.
3. JupyterLab opens. The terminal is on the left, already in the `project` folder. A read-only copy of the exercise page is on the right.

- Copy a command: select it and press Ctrl+C, or Cmd+C on a Mac.
- Paste it in the terminal: Ctrl+Shift+V, or right-click and choose Paste. Cmd+V on a Mac is untested, so right-click if it doesn't work.
- Edit a file: double-click it in the file panel on the far left. Save with Ctrl+S, or Cmd+S on a Mac.
- Or edit it in the terminal with `nano <file>`, `vi <file>` or `vim <file>`. nano is the simplest. Ctrl+O, then Enter, saves. Ctrl+X quits.
- The environment is active and `project` is built, so skip to [Check your setup](#check-your-setup).

(download-your-work)=
### Download your work

Pack the `project` folder into one file:

```bash
cd ~ && tar -czf my-work.tar.gz project && cd project
```

- In the file panel, go up to the top folder.
- Right-click `my-work.tar.gz` and choose Download. ([Uploading and downloading](https://jupyterlab.readthedocs.io/en/stable/user/files.html#uploading-and-downloading))
- The file has your commits too, because `project` is a Git repository.
- To unpack it on your own machine, run `tar -xzf my-work.tar.gz`.

+++ {"tags": ["track-mac", "track-linux", "track-wsl2"]}

## Your own machine

+++ {"tags": ["track-hpc"]}

## Your account on a shared machine or cluster

+++ {"tags": ["track-mac", "track-linux", "track-wsl2", "track-hpc"]}

- Disk use is about 3 GB for all four exercises, with conda's package cache.

+++ {"tags": ["track-mac", "track-linux", "track-hpc"]}

- You don't need administrator access.

+++ {"tags": ["track-wsl2"]}

- You don't need administrator access, except to turn on WSL2.

+++ {"tags": ["track-mac", "track-linux", "track-wsl2", "track-hpc"]}

### Step 1: get a shell

+++ {"tags": ["track-mac"]}

- Open Terminal.
- It's in Applications, under Utilities.
- This works on Apple silicon and on Intel Macs.

+++ {"tags": ["track-wsl2"]}

- The exercises run in Linux, and WSL2 gives you Linux on Windows.

Open PowerShell as an administrator and run this, then restart if it asks you to:

```powershell
wsl --install -d Ubuntu
```

- Open Ubuntu from the Start menu and choose a user name and password.
- Run everything below in that Ubuntu window.

- Keep your work in your Linux home folder, not under `/mnt/c`.
- DVC needs a Linux file system.

+++ {"tags": ["track-linux", "track-hpc"]}

- Open a terminal.
- This works on x86_64 and on ARM.

+++ {"tags": ["track-hpc"]}

- On a cluster, log in with `ssh`, as you do for any job.

+++ {"tags": ["track-mac", "track-linux", "track-wsl2", "track-hpc"]}

### Step 2: install conda

- The exercises use conda to build their environments.
- [Miniforge](https://github.com/conda-forge/miniforge) is a small installer that gets its packages from conda-forge, and it installs in your home folder.
- If you already have conda or mamba, skip this step.

+++ {"tags": ["track-hpc"]}

- If your site has conda as a module, you can load that instead, for example `module load miniforge3`. Your center's documentation names it.

+++ {"tags": ["track-mac", "track-linux", "track-wsl2", "track-hpc"]}

```bash
curl -L -O "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh"
bash "Miniforge3-$(uname)-$(uname -m).sh" -b -p ~/miniforge3
source ~/miniforge3/bin/activate
```

- The last line turns conda on in this window.
- Run it again each time you open a new one.

### Step 3: check for Git

```bash
git --version
```

If that fails, install Git into conda's base environment:

```bash
conda install --yes git
```

### Step 4: get an exercise

- Each exercise is its own branch of one repository, with its own environment.
- Pick the row you want.
- Building an environment takes a few minutes the first time.

| Exercise | Branch | Environment |
|---|---|---|
| 1. Software environments | `binder-01-environments` | `repro-environments` |
| 2. Workflows | `binder-02-workflows` | `repro-workflows` |
| 3. Versioning data | `binder-03-dataops` | `repro-dataops` |
| 4. Model registry | `binder-04-registry` | `repro-registry` |

For exercise 1, that looks like this:

```bash
git clone --branch binder-01-environments --single-branch https://github.com/ohpcsim/reproducibility-in-ai.git environments
cd environments
conda env create --quiet --file .binder/environment.yml
conda activate repro-environments
python scripts/setup_project.py
cd project
```

- You're now in the `project` folder, ready for the [exercise's first step](exercises/01-environments/environments.ipynb).
- If you close the window, open a new one and turn conda on, then run `conda activate repro-environments` and `cd environments/project`.
- If `conda env create` says the prefix already exists, an environment with that name is left from an earlier run: `conda env remove -n repro-<name>` and create it again.

(container-tool)=
### Optional: a container tool (Exercises 1b and 1c only)

- Binder and Exercises 1, 2, 3 and 4 don't need one.

+++ {"tags": ["track-mac"]}

- Install [Docker Desktop](https://docs.docker.com/desktop/) or [Podman Desktop](https://podman-desktop.io/). Each runs a small Linux VM.

+++ {"tags": ["track-linux"]}

- Install Docker Engine or Podman from your distribution's packages. [Docker's install page](https://docs.docker.com/engine/install/) and [Podman's](https://podman.io/docs/installation) list the steps for each distribution.

+++ {"tags": ["track-wsl2"]}

- Install Apptainer inside WSL2, in the Ubuntu window. [Apptainer's install page](https://apptainer.org/docs/admin/main/installation.html#install-ubuntu-packages) has the Ubuntu steps. Check with `apptainer --version`.

+++ {"tags": ["track-hpc"]}

- Apptainer is usually installed by your admins; check with `apptainer --version`. ([Apptainer](https://apptainer.org/docs/user/main/))

+++ {"tags": ["track-mac", "track-linux", "track-wsl2", "track-hpc"]}

(install-uv)=
### Optional: uv

- uv manages Python, virtual environments and packages from PyPI.
- It is very fast at resolving and installing Python packages. See [uv's benchmarks](https://docs.astral.sh/uv/#highlights).
- It downloads Python itself, so this route needs neither conda nor a system Python.
- `pyproject.toml` declares the packages. `uv.lock` records their versions and hashes in one cross-platform file.
- conda also handles non-Python packages, including R, C/C++ libraries, CUDA, MPI and GDAL. That's why the exercises lead with conda.
- Exercises 2, 3 and 4 have a "With uv instead of conda" option. Exercise 1 uses uv as part of the lesson.
- Run the [official uv installer](https://docs.astral.sh/uv/getting-started/installation/):

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source "$HOME/.local/bin/env"
uv --version
```

- Git comes from your system. uv does not install Git.

+++ {"tags": ["track-mac"]}

- If Git is missing, use `xcode-select --install`.

+++ {"tags": ["track-linux", "track-wsl2"]}

- If Git is missing, use `sudo apt install git` on Ubuntu.

+++ {"tags": ["track-mac", "track-linux", "track-wsl2", "track-hpc"]}

- Exercises 2 to 4 each pin Python 3.12.12 in `.python-version` and require Python 3.12 in `pyproject.toml`.
- Their uv configuration requires managed Python. `uv sync --locked` downloads that Python, builds `.venv` and installs the locked packages.
- The lock chooses wheels for your platform. The target platforms are Linux x86_64 and aarch64, and macOS Intel and Apple silicon.
- DVC requires ANTLR 4.9.3, which has no PyPI wheel. uv builds this pure Python dependency from its source archive. It needs no C/C++ compiler.
- Snakemake requires connection-pool 0.0.3, which also has no PyPI wheel. uv builds it from its pure Python source archive.
- The DataOps and registry configurations constrain cryptography below 49 to keep Intel macOS wheels available.

+++

(messages-you-can-ignore)=
### Messages you can ignore

- `conda env create` may print `WARNING conda.conda_pypi...` with current Miniforge. It's harmless.
- It may also print a "Did you know? ... conda-pypi" tip. It's harmless.
- In exercises 3 and 4, DVC may print "Waiting to acquire lock. If DVC froze, see hardlink_lock" several times. It's harmless, and the command finishes.

+++ {"tags": ["track-mac", "track-linux", "track-wsl2", "track-hpc"]}

### Edit files

- Use any text editor.
- If you're not sure, `nano environment.yml` works in the terminal.
- Press Control-O to save and Control-X to leave.

### When you're done

- Everything an exercise makes is in its folder or its environment.

To remove it all, go to the folder above `environments` and paste this:

```bash
conda deactivate
conda env remove --yes --name repro-environments
rm -rf environments
```

- The environment is cattle, and you can rebuild it from the file in the repository.

+++

(check-your-setup)=
## Check your setup

Run the exercise's short check from the `project` folder:

```bash
python ../check.py --short
```

- It prints one line per part, each starting with PASS or FAIL, and a count at the end.
- On a fresh project, most parts fail. That's expected, because the failures are the exercise.
- For exercise 1 on a fresh project, it prints six FAIL lines and `0 of 6 parts pass.`
+++ {"tags": ["track-binder"]}

- If Python says it can't open `check.py`, you're not in the `project` folder. Run `cd ~/project`.

+++ {"tags": ["track-mac", "track-linux", "track-wsl2", "track-hpc"]}

- If Python says it can't open `check.py`, you're not in the `project` folder. Run `cd environments/project` from the folder above it.
- If Python says `ModuleNotFoundError`, the exercise's environment isn't active. Turn conda on and run `conda activate` with the environment from the table.

+++

## Your exercises

+++ {"tags": ["track-binder"]}

- [1. Software environments](exercises/01-environments/environments.ipynb)
- [2. Workflows](exercises/02-workflows/workflows.ipynb)
- [3. Versioning data](exercises/03-dataops/dataops.ipynb)
- [4. Model registry](exercises/04-registry/registry.ipynb)
- 1b and 2b run on your own machine: see Your Mac, Your Linux machine, Windows (WSL2) or Shared Linux or HPC.
- 1c needs an NVIDIA GPU: see Your Linux machine, Windows (WSL2) or Shared Linux or HPC.

+++ {"tags": ["track-mac", "track-linux", "track-wsl2", "track-hpc"]}

- 1. Software environments: [1a. conda and uv locks](exercises/01-environments/environments.ipynb) and [1b. Environments in containers](exercises/01-environments/containers.md)

+++ {"tags": ["track-linux", "track-wsl2", "track-hpc"]}

- [1c. PyTorch with a GPU](gpu/gpu.md), with an NVIDIA GPU

+++ {"tags": ["track-mac"]}

- 1c needs an NVIDIA GPU: see Your Linux machine, Windows (WSL2) or Shared Linux or HPC.

+++ {"tags": ["track-mac", "track-linux", "track-wsl2", "track-hpc"]}

- 2. Workflows: [2a. Snakemake](exercises/02-workflows/workflows.ipynb) and [2b. Nextflow](exercises/02-workflows/nextflow.md)
- [3. Versioning data](exercises/03-dataops/dataops.ipynb)
- [4. Model registry](exercises/04-registry/registry.ipynb)
