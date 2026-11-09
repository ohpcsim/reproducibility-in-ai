---
title: Set up your environment
---


+++ {"tags": ["track-binder"]}

- Each exercise needs a terminal, Git and the packages in its environment file.
- You get them in your browser with Binder.
- You read the exercise pages on this site and paste the commands into the terminal.
- You don't need Jupyter or a GPU.
- [Tools and documentation](tools.md) lists each tool, with links to its documentation.

## Binder and BinderHub: how it works

- A Binder is a Git repository with code or content to run, and configuration files that declare its environment. ([What is a Binder?](https://mybinder.readthedocs.io/en/latest/introduction.html#what-is-a-binder))
- repo2docker reads those files and builds a container image from them. ([repo2docker](https://repo2docker.readthedocs.io/en/latest/))
- repo2docker looks for the files in a `binder/` or `.binder/` folder first. If that folder exists, it ignores configuration files in the root of the repository. ([Where to put configuration files](https://repo2docker.readthedocs.io/en/latest/use/repository.html#where-to-put-configuration-files-in-a-repository))
- BinderHub is the service that builds the images and serves them. It uses repo2docker to build, a Docker registry to store the images, Kubernetes to manage the cloud machines, and JupyterHub to run a temporary container for each user. ([The BinderHub architecture](https://binderhub.readthedocs.io/en/latest/overview.html))
- mybinder.org is a free public service. It's a federation of BinderHub deployments that the Binder community maintains, and it has limited resources. ([What is mybinder.org?](https://mybinder.readthedocs.io/en/latest/introduction.html#what-is-mybinder-org), [Is mybinder.org free to use?](https://mybinder.readthedocs.io/en/latest/about/user-guidelines.html#is-mybinder-org-free-to-use))

### What's in each exercise branch

Each exercise branch has four files in `.binder/`:

- `environment.yml` lists the conda packages. repo2docker installs them into its own base environment, not into one named `repro-environments`, so you don't run `conda activate` in Binder. ([environment.yml](https://repo2docker.readthedocs.io/en/latest/configuration/research.html))
- `postBuild` runs once, at build time, after the packages are installed. Ours builds the `project` folder, loads the JupyterLab layout and makes new terminals start in `project`. ([postBuild](https://repo2docker.readthedocs.io/en/latest/configuration/actions.html))
- `workspace.json` is the JupyterLab layout: a terminal on the left and the exercise page on the right. ([JupyterLab on Binder](https://jupyterlab.readthedocs.io/en/stable/user/binder.html#customize-the-layout))
- `exercise.ipynb` is the Binder copy of the page. `postBuild` turns it into the panel on the right.
- In exercises 2 to 4, the root `pyproject.toml`, `uv.lock` and `.python-version` don't change Binder's environment. See [where to put configuration files](https://repo2docker.readthedocs.io/en/latest/use/repository.html#where-to-put-configuration-files-in-a-repository).
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

- Copy and paste a command: Ctrl+C, then Ctrl+V in the terminal. On a Mac, Cmd+C and Cmd+V.
- Edit a file: double-click it in the file panel on the far left. Save with Ctrl+S, or Cmd+S on a Mac.
- Or edit it in the terminal with `nano <file>`, `vi <file>` or `vim <file>`. nano is the simplest. Ctrl+O, then Enter, saves. Ctrl+X quits.
- The environment is active and `project` is built, so you start at the exercise's first step.

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

+++ {"tags": ["track-mac"]}

- This page gets your Mac ready for the exercises: a terminal, conda and Git, and if you want them, uv and a container tool. You don't need administrator access.
+++ {"tags": ["track-linux"]}

- This page gets your Linux machine ready for the exercises: a terminal, conda and Git, and if you want them, uv and a container tool. You don't need administrator access, except to install Podman for 1b and Apptainer for 1c.
+++ {"tags": ["track-wsl2"]}

- This page gets your Windows PC ready for the exercises: Ubuntu in WSL2, conda and Git, and if you want them, uv, Podman and Apptainer. You need administrator access to turn on WSL2, and `sudo` in Ubuntu to install Podman and Apptainer.
+++ {"tags": ["track-hpc"]}

- This page gets your account on a shared Linux machine or cluster ready for the exercises: a shell, conda and Git, and if you want them, uv and Apptainer. You don't need administrator access.
+++ {"tags": ["track-mac", "track-linux", "track-wsl2", "track-hpc"]}

- Each exercise page then clones its own copy of the exercise and builds its own environment.

+++ {"tags": ["track-mac", "track-linux", "track-wsl2", "track-hpc"]}

## Step 1: get a shell

+++ {"tags": ["track-mac"]}

- Open Terminal.
- It's in Applications, under Utilities.
- We ran these pages on Apple silicon, not on an Intel Mac.

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

## Step 2: install conda

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

+++ {"tags": ["track-mac"]}

- Optional: to turn conda on in every new window, run `conda init zsh` once. It adds a block to `~/.zshrc`.

+++ {"tags": ["track-linux", "track-wsl2"]}

- Optional: to turn conda on in every new window, run `conda init bash` once. It adds a block to `~/.bashrc`.

+++ {"tags": ["track-hpc"]}

- Don't run `conda init` on a cluster. It edits `~/.bashrc`, which can clash with the cluster's modules. Use the `source` line, or your site's conda module, instead.

+++ {"tags": ["track-mac", "track-linux", "track-wsl2", "track-hpc"]}

## Step 3: check for Git

```bash
git --version
```

If that fails, install Git into conda's base environment:

```bash
conda install --yes git
```

(install-uv)=
## Optional: uv

- uv installs Python and a project's packages from its `pyproject.toml` and `uv.lock`.
- Exercise 1a's conda environment already has uv.
+++ {"tags": ["track-mac"]}

- You need it for the "With uv instead of conda" option in Exercises 2 to 4.
+++ {"tags": ["track-linux", "track-wsl2", "track-hpc"]}

- You need it for the "With uv instead of conda" option in Exercises 2 to 4, and for step 2 of 1c.
+++ {"tags": ["track-mac", "track-linux", "track-wsl2", "track-hpc"]}

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source "$HOME/.local/bin/env"
uv --version
```

(container-tool)=
## Optional: a container tool

+++ {"tags": ["track-mac"]}

- Only Exercise 1b uses one.
- Install [Podman Desktop](https://podman-desktop.io/). It runs a small Linux VM.
- Open a new Terminal window after installing, so `podman` is on your `PATH`.
- Start the Podman machine from Podman Desktop, or with `podman machine init` and then `podman machine start`. Check that `podman machine list` says `Currently running`.
- The default 2 GiB machine is enough for Exercise 1b.

+++ {"tags": ["track-linux"]}

- Only Exercises 1b and 1c use one.
- For 1b, install Podman from your distribution's packages, with `sudo`. [Podman's install page](https://podman.io/docs/installation) lists the steps for each distribution. Check with `podman --version`. Run `podman` itself without `sudo`.
- For 1c, install Apptainer. [Apptainer's install page](https://apptainer.org/docs/admin/main/installation.html) has the steps. Check with `apptainer --version`.

+++ {"tags": ["track-wsl2"]}

- Only Exercises 1b and 1c use one.
- For 1b, install Podman in the same Ubuntu window: `sudo apt update && sudo apt install -y podman`. Check with `podman --version`. Run `podman` itself without `sudo`.
- For 1c, install Apptainer inside WSL2, in the Ubuntu window, with `sudo`. [Apptainer's install page](https://apptainer.org/docs/admin/main/installation.html#install-ubuntu-packages) has the Ubuntu steps. Check with `apptainer --version`.

+++ {"tags": ["track-hpc"]}

- Only Exercises 1b and 1c use one.
- Apptainer is usually installed by your admins. Check with `apptainer --version`. ([Apptainer](https://apptainer.org/docs/user/main/))

+++ {"tags": ["track-mac", "track-linux", "track-wsl2", "track-hpc"]}

(messages-you-can-ignore)=
## Messages you can ignore

- The Miniforge installer may print `warning  libmamba Security Warning: This transaction includes executing package scripts (pre/post-link/unlink) if present.` It's harmless. The installer may run setup scripts that come with conda-forge's packages, and the warning says so.
- The uv installer may print `WARN: The following commands are shadowed by other commands in your PATH: uv uvx` when an exercise's conda environment is active. That environment's own uv comes first in `PATH`. Either uv works.
- `conda env create` may print `WARNING conda.conda_pypi...` and a "Did you know? ... conda-pypi" tip with current Miniforge. Both are harmless.

+++

Next: [Exercise 1a](exercises/01-environments/environments.ipynb)
