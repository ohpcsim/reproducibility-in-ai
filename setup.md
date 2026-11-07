---
title: Set up your laptop
---

- You can do every exercise in Binder with nothing installed.
- Set up your laptop if you want to keep your work.
- You'll read the exercise pages on this site in your browser, and paste the commands into your terminal.
- You need about 3 GB of free disk for the four exercises, and no administrator access except to turn on WSL2.
- You don't need Jupyter or a GPU.

## Step 1: get a shell

::::{tab-set}

:::{tab-item} Mac
- Open Terminal.
- It's in Applications, under Utilities.
- This works on Apple silicon and on Intel Macs.
:::

:::{tab-item} Windows through WSL2
- The exercises run in Linux, and WSL2 gives you Linux on Windows.

Open PowerShell as an administrator and run this, then restart if it asks you to:

```powershell
wsl --install -d Ubuntu
```

- Open Ubuntu from the Start menu and choose a user name and password.
- Run everything below in that Ubuntu window.

- Keep your work in your Linux home folder, not under `/mnt/c`.
- Git hooks and DVC need a Linux file system.
:::

:::{tab-item} Linux
- Open a terminal.
- This works on x86_64 and on ARM.
:::

::::

## Step 2: install conda

- The exercises use conda to build their environments.
- [Miniforge](https://github.com/conda-forge/miniforge) is a small installer that gets its packages from conda-forge, and it installs in your home folder.
- If you already have conda or mamba, skip this step.

```bash
curl -L -O "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh"
bash "Miniforge3-$(uname)-$(uname -m).sh" -b -p ~/miniforge3
source ~/miniforge3/bin/activate
```

- The last line turns conda on in this window.
- Run it again each time you open a new one.

## Step 3: check for Git

```bash
git --version
```

If that fails, install Git into conda's base environment:

```bash
conda install --yes git
```

## Step 4: get an exercise

- Each exercise is its own branch of one repository, with its own environment.
- Pick the row you want.
- Building an environment takes a few minutes the first time.

| Exercise | Branch | Environment |
|---|---|---|
| 1. GitOps | `binder-01-gitops` | `repro-gitops` |
| 2. DataOps | `binder-02-dataops` | `repro-dataops` |
| 3. Model registry | `binder-03-registry` | `repro-registry` |
| 4. LLM documentation | `binder-04-llm` | `repro-llm` |

For exercise 1, that looks like this:

```bash
git clone --branch binder-01-gitops --single-branch https://github.com/ohpcsim/reproducibility-in-ai.git gitops
cd gitops
conda env create --quiet --file .binder/environment.yml
conda activate repro-gitops
python scripts/setup_project.py
cd project
```

- You're now in the `project` folder, ready for the [exercise's first step](exercises/01-gitops/gitops.ipynb).
- If you close the window, open a new one and turn conda on, then run `conda activate repro-gitops` and `cd gitops/project`.

- To edit files, use any text editor.
- If you're not sure, `nano environment.yml` works in the terminal.
- Press Control-O to save and Control-X to leave.

## When you're done

- Everything an exercise makes is in its folder or its environment.

To remove it all, go to the folder above `gitops` and paste this:

```bash
conda deactivate
conda env remove --yes --name repro-gitops
rm -rf gitops
```

- The environment is cattle, and you can rebuild it from the file in the repository.
