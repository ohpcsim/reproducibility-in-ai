+++ {"tags": ["track-binder"]}

# Binder (workshop default)

Pick an exercise and launch it. You need a browser and nothing else.

- {button}`1. Software environments <https://mybinder.org/v2/gh/ohpcsim/reproducibility-in-ai/binder-01-environments?urlpath=lab/workspaces/exercise>` How do you declare and lock what the penguin project needs, with conda and with uv?
- {button}`2. Workflows <https://mybinder.org/v2/gh/ohpcsim/reproducibility-in-ai/binder-02-workflows?urlpath=lab/workspaces/exercise>` How do you add a step to the penguin project's workflow, so one command builds the numbers and the figure?
- {button}`3. Versioning data <https://mybinder.org/v2/gh/ohpcsim/reproducibility-in-ai/binder-03-dataops?urlpath=lab/workspaces/exercise>` Do the 2008 and 2009 seasons change how much heavier male penguins are?
- {button}`4. Model registry <https://mybinder.org/v2/gh/ohpcsim/reproducibility-in-ai/binder-04-registry?urlpath=lab/workspaces/exercise>` Which penguin model is live?

## What you'll see

- JupyterLab opens with a terminal on the left, already in the `project` folder, and the exercise on the right.
- The first launch can take a few minutes while the image builds.
- A session shuts down after 10 minutes idle and lasts at most about six hours, with 1 to 2 GB of memory.
- Download anything you want to keep. [Download your work](#download-your-work) shows how.
- Copy and paste: Ctrl+C and Ctrl+V. On a Mac, Cmd+C and Cmd+V.

(download-your-work)=
## Download your work

Pack the `project` folder into one file:

```bash
cd ~ && tar -czf my-work.tar.gz project && cd project
```

- In the file panel, go up to the top folder.
- Right-click `my-work.tar.gz` and choose Download.
- To unpack it on your own machine, run `tar -xzf my-work.tar.gz`.
- The file holds `project` and its commits only, not the exercise's `osn-bucket` folder or `check.py`. To carry on with Exercise 3 or 4 on your own machine, start that exercise again there.

+++ {"tags": ["track-mac", "track-linux", "track-wsl2", "track-hpc"]}

# Set up your environment

+++ {"tags": ["track-mac"]}

- This page gets your Mac ready for the exercises: a terminal, conda and Git, and if you want them, uv and a container tool. You don't need administrator access.
+++ {"tags": ["track-linux"]}

- This page gets your Linux machine ready for the exercises: a terminal, conda and Git, and if you want them, uv and a container tool. You don't need administrator access, except to install Podman for 1b and Apptainer for 1c.
+++ {"tags": ["track-wsl2"]}

- This page gets your Windows PC ready for the exercises: Ubuntu in WSL2, conda and Git, and if you want them, uv, Podman and Apptainer. You need administrator access to turn on WSL2, and `sudo` in Ubuntu to install Podman and Apptainer.
+++ {"tags": ["track-hpc"]}

- This page gets your account on a shared Linux machine or cluster ready for the exercises: a shell, conda and Git, and if you want them, uv and Apptainer. You don't need administrator access.
- We ran the HPC track on a Linux machine without root and with Apptainer, not on a real cluster. Your site's modules and policies may differ.
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

+++ {"tags": ["track-mac", "track-linux", "track-wsl2"]}

If that fails, install Git into conda's base environment:

```bash
conda install --yes git
```

+++ {"tags": ["track-hpc"]}

If that fails, load your site's Git module. Your center's documentation names it.

+++ {"tags": ["track-mac", "track-linux", "track-wsl2", "track-hpc"]}

(install-uv)=
## Optional: uv

- uv installs Python and a project's packages from its `pyproject.toml` and `uv.lock`.
- Exercise 1a's conda environment already has uv.
+++ {"tags": ["track-mac"]}

- You need it for the "With uv instead of conda" option in Exercises 2a, 3 and 4.
+++ {"tags": ["track-linux", "track-wsl2", "track-hpc"]}

- You need it for the "With uv instead of conda" option in Exercises 2a, 3 and 4, and for step 2 of 1c.
+++ {"tags": ["track-mac", "track-linux", "track-wsl2", "track-hpc"]}

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source "$HOME/.local/bin/env"
uv --version
```

+++ {"tags": ["track-mac"]}

- The installer adds `. "$HOME/.local/bin/env"` to `~/.zshrc` and `~/.profile`, so new windows find uv.

+++ {"tags": ["track-linux", "track-wsl2", "track-hpc"]}

- The installer adds `. "$HOME/.local/bin/env"` to `~/.bashrc`, `~/.profile` and `~/.zshrc`, so new windows find uv.

+++ {"tags": ["track-hpc"]}

- The uv installer's line only adds uv's folder to `PATH`, so it doesn't clash with your cluster's modules the way `conda init` can.

+++ {"tags": ["track-mac", "track-linux", "track-wsl2", "track-hpc"]}

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
- Apptainer is usually installed by your admins. Check with `apptainer --version`. ([Apptainer](https://apptainer.org/docs/user/latest/))

+++ {"tags": ["track-mac", "track-linux", "track-wsl2", "track-hpc"]}

(messages-you-can-ignore)=
## Messages you can ignore

- The Miniforge installer may print `warning  libmamba Security Warning: This transaction includes executing package scripts (pre/post-link/unlink) if present.` It's harmless. The installer may run setup scripts that come with conda-forge's packages, and the warning says so.
- The uv installer may print `WARN: The following commands are shadowed by other commands in your PATH: uv uvx` when an exercise's conda environment is active. That environment's own uv comes first in `PATH`. Either uv works.
- `conda env create` may print `WARNING conda.conda_pypi...` and a "Did you know? ... conda-pypi" tip with current Miniforge. Both are harmless.

+++ {"tags": ["track-mac", "track-linux", "track-wsl2", "track-hpc"]}

Next: [Exercise 1a](exercises/01-environments/environments.ipynb)
