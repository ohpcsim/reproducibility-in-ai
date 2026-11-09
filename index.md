---
title: Reproducibility in AI
subject: Hands-on exercises
---

## Which machine are you on?

- Pick one. Each track has its own setup page and its own copy of each exercise, with the commands for that machine only.
- Not sure? Use Binder, the workshop default.

| Track | Who it's for | Exercises |
|---|---|---|
| [Binder](setup.md), the workshop default | Anyone. Nothing to install, you need a browser. | 1a, 2a, 3, 4 |
| [Your Mac](setup-mac.md) | A Mac you own, with Apple silicon | 1a, 1b, 2a, 2b, 3, 4 |
| [Your Linux machine](setup-linux.md) | Linux you own, with root | 1a, 1b, 1c with an NVIDIA GPU, 2a, 2b, 3, 4 |
| [Windows (WSL2)](setup-wsl2.md) | A Windows PC you own | 1a, 1b, 1c with an NVIDIA GPU, 2a, 2b, 3, 4 |
| [Shared Linux or HPC](setup-hpc.md) | An account with no root, such as a campus cluster | 1a, 1b with Apptainer, 1c on a GPU node, 2a, 2b, 3, 4 |

### Binder or your own machine

| | Binder | Your own machine |
|---|---|---|
| What you install | Nothing. You need a browser. | Miniforge and Git. On Windows, WSL2 too. |
| Where your work lives | A temporary session on mybinder.org | A folder in your home directory |
| How long a session lasts | It shuts down after 10 minutes idle, and aims to last up to six hours | As long as you want |
| Memory | At least 1 GB, at most 2 GB | Your machine's |
| Disk | Nothing on your machine | About 3 GB for all four exercises |
| First start | A few minutes when the image isn't built or cached yet | A few minutes to build each environment |
| Keeping your work | Only the files you download | Everything stays |

- To try an exercise, use Binder.
- To keep your work, use your own machine.
- The Binder numbers are from the [mybinder.org usage guidelines](https://mybinder.readthedocs.io/en/latest/about/user-guidelines.html#resources-available).

## About the workshop

- The exercises from the Reproducibility in AI workshop at Rice Research Computing Day.
- You do them on your own time, with these pages and a terminal.
- Each exercise adds one thing to the penguin project: a locked environment, a workflow step, versioned data, a model registry.
- A check script tells you when you're done.
- You don't need a GPU, a cluster or an account.

## The idea: literate science

- In 1984 Donald Knuth proposed writing a program as one document, for people and for the machine. Literate science puts the claims, the code, the environment and the data in one project, and every published result comes from running it.
- Your research products (papers, code, data) are the pets. Everything that runs them is cattle, so you can delete it and build it again from what's in the project.
- This site works the same way. The exercise notebooks rerun every time the site is published, so the output on them is real.
- [The premise](premise.md) has the full argument.
- [Literate Science Results: sexual dimorphism in Palmer penguins](results/results.ipynb) is one such document. The build runs the finished project's code, and the page shows what it printed and drew.
- [How this site is built](build.md) shows its configuration, the command that builds it and the automation that reruns every notebook.

## The exercises

- The four exercises use one project, [a study of Palmer penguins](project.md), and add a capability in each exercise.
- Each exercise stands on its own, and takes 15 to 20 minutes.
- Only reading? Each page shows the failure and how to approach the fix.

::::{grid} 1 1 2 2

:::{card} 1. Software environments
**How do you declare and lock what the penguin project needs, with conda and with uv?**

- **Problem:** a script imports a package that the project's dependency files don't declare.
- **You'll learn:** declare and lock an environment with conda, then with uv, and why a conda lock is per platform and a uv lock isn't.
- **Data:** Palmer penguins, the 2007 field season.
- About 20 minutes.

{button}`Open in Binder <https://mybinder.org/v2/gh/ohpcsim/reproducibility-in-ai/binder-01-environments?urlpath=lab/workspaces/exercise>` [Read the page](exercises/01-environments/environments.ipynb)
:::

:::{card} 2. Workflows
**How do you add a step to the penguin project's working workflow, so one command builds the numbers and the figure, with Snakemake or Nextflow?**

- **Problem:** the project's workflow builds its numbers, and its README shows a figure that nothing builds.
- **You'll learn:** run a workflow you were given, add a step with Snakemake, and watch the tool run only what's new or stale, and a changed parameter rerun only the step that reads it. The same exercise in Nextflow, [2b](exercises/02-workflows/nextflow.md), for your own machine.
- **Data:** Palmer penguins, the 2007 field season.
- About 15 to 20 minutes.

{button}`Open in Binder <https://mybinder.org/v2/gh/ohpcsim/reproducibility-in-ai/binder-02-workflows?urlpath=lab/workspaces/exercise>` [Read the page](exercises/02-workflows/workflows.ipynb)
:::

:::{card} 3. Versioning data
**Do the 2008 and 2009 seasons change how much heavier male penguins are?**

- **Problem:** the data is in Git, and a new field season is coming.
- **You'll learn:** version data with DVC and a bucket, rerun the declared steps on a new version, and bring back an old version with its numbers and its figure.
- **Data:** Palmer penguins, the 2007 season, then 2007 to 2009.
- About 15 minutes.

{button}`Open in Binder <https://mybinder.org/v2/gh/ohpcsim/reproducibility-in-ai/binder-03-dataops?urlpath=lab/workspaces/exercise>` [Read the page](exercises/03-dataops/dataops.ipynb)
:::

:::{card} 4. Model registry
**Which penguin model is live?**

- **Problem:** a trained penguin model has no registered version or live stage.
- **You'll learn:** register two versions with GTO, promote the better validation score and restore every model with DVC.
- **Data:** Palmer penguins, 2007 to 2009.
- About 15 to 20 minutes.

{button}`Open in Binder <https://mybinder.org/v2/gh/ohpcsim/reproducibility-in-ai/binder-04-registry?urlpath=lab/workspaces/exercise>` [Read the page](exercises/04-registry/registry.ipynb)
:::

::::

- Exercise 1 has two optional parts you run on your own machine: [1b, Environments in containers](exercises/01-environments/containers.md), and [1c, PyTorch with a GPU](gpu/gpu.md) on Linux or WSL2 with an NVIDIA GPU.

## How to start

It works the same way everywhere: read the page, and paste the commands into a terminal.

1. Pick your machine at the top of this page, and follow its setup page.
2. Pick an exercise in that track. If you're not sure, start with the first.
3. On Binder, the first start can take a few minutes. A session has 2 GB of memory and ends when it sits idle, so download anything you want to keep.
4. Do the steps on the page, then run its check, `python ../check.py`.
5. To learn a tool, [Tools and documentation](tools.md) links to its documentation and its introduction.

The code here is MIT licensed. Each exercise names its data, its license and how to cite it.
