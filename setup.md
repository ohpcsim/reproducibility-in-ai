---
title: Set up your environment
---

- Each exercise needs a terminal, Git and the packages in its environment file.
- You can get them in your browser with Binder, or on your own machine: a Mac, Windows through WSL2, or Linux.
- Either way, you read the exercise pages on this site and paste the commands into the terminal.
- You don't need Jupyter or a GPU.

- For an optional Python-only setup on your own machine, use [the uv route](uv.md).

## Your choices

| | Binder | Your own machine |
|---|---|---|
| What you install | Nothing. You need a browser. | Miniforge and Git. On Windows, WSL2 too. |
| Where your work lives | A temporary session on mybinder.org | A folder in your home directory |
| How long a session lasts | It shuts down after 10 minutes idle, and aims to last up to six hours | As long as you want |
| Memory | At least 1 GB, at most 2 GB | Your machine's |
| Disk | Nothing on your machine | About 3 GB for all five exercises |
| First start | A few minutes when the image isn't built or cached yet | A few minutes to build each environment |
| Keeping your work | Only the files you download | Everything stays |

- To try an exercise, use Binder.
- To keep your work, use your own machine.
- [Tools and documentation](tools.md) lists each tool, with links to its documentation.
- The Binder numbers are from the [mybinder.org usage guidelines](https://mybinder.readthedocs.io/en/latest/about/user-guidelines.html#resources-available).

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
3. JupyterLab opens. The terminal is on the left, already in the `project` folder. The exercise page is on the right.

- Copy a command: select it and press Ctrl+C, or Cmd+C on a Mac.
- Paste it in the terminal: Ctrl+Shift+V, or right-click and choose Paste. Cmd+V on a Mac is untested, so right-click if it doesn't work.
- Edit a file: double-click it in the file panel on the far left. Save with Ctrl+S.
- The environment is active and `project` is built, so skip to [Check your setup](#check-your-setup).

### Download your work

Pack the `project` folder into one file:

```bash
cd ~ && tar -czf my-work.tar.gz project && cd project
```

- In the file panel, go up to the top folder.
- Right-click `my-work.tar.gz` and choose Download. ([Uploading and downloading](https://jupyterlab.readthedocs.io/en/stable/user/files.html#uploading-and-downloading))
- The file has your commits too, because `project` is a Git repository.
- To unpack it on your own machine, run `tar -xzf my-work.tar.gz`.

## Your own machine

- Disk use is about 3 GB for all five exercises.
- You don't need administrator access, except to turn on WSL2.

### Step 1: get a shell

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
- DVC needs a Linux file system.
:::

:::{tab-item} Linux
- Open a terminal.
- This works on x86_64 and on ARM.
:::

::::

### Step 2: install conda

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
| 3. Data | `binder-03-dataops` | `repro-dataops` |
| 4. Model registry | `binder-04-registry` | `repro-registry` |
| 5. LLM documentation | `binder-05-llm` | `repro-llm` |

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

(messages-you-can-ignore)=
### Messages you can ignore

- `conda env create` may print `WARNING conda.conda_pypi...` with current Miniforge. It's harmless.
- It may also print a "Did you know? ... conda-pypi" tip. It's harmless.
- In exercise 3, DVC may print "Waiting to acquire lock. If DVC froze, see hardlink_lock" several times. It's harmless, and the command finishes.

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

(check-your-setup)=
## Check your setup

Run the exercise's short check from the `project` folder, in Binder or on your own machine:

```bash
python ../check.py --short
```

- It prints one line per part, each starting with PASS or FAIL, and a count at the end.
- On a fresh project, most parts fail. That's expected, because the failures are the exercise.
- For exercise 1 on a fresh project, it prints six FAIL lines and `0 of 6 parts pass.`
- If Python says it can't open `check.py`, you're not in the `project` folder. Run `cd ~/project` in Binder, or `cd environments/project` on your own machine.
- If Python says `ModuleNotFoundError`, the exercise's environment isn't active. On your own machine, turn conda on and run `conda activate` with the environment from the table.
