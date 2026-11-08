---
title: Reproducibility in AI
subject: Hands-on exercises
---

- The exercises from the Reproducibility in AI workshop at Rice Research Computing Day.
- You do them on your own time, with these pages and a terminal.
- Each one gives you a broken project. You fix it, and a script checks your work.
- You don't need a GPU, a cluster or an account.

## The idea: literate science

- In 1984 Donald Knuth proposed writing a program as one document, for people and for the machine. Literate science puts the claims, the code, the environment and the data in one project, and every published result comes from running it.
- The document and the data are the pets. Everything that runs them is cattle, so you can delete it and build it again from what's in the project.
- This site works the same way. Each exercise page is a notebook that reruns when the site is published, and the failures on it are real output.
- [The premise](premise.md) has the full argument.
- [Results: sexual dimorphism in Palmer penguins](results/results.ipynb) is one such document. The build runs the finished project's code, and the page shows what it printed and drew.
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
**How do you declare the penguin project's steps so one command rebuilds the result, with Snakemake or Nextflow?**

- **Problem:** a README says "run these in this order", and nothing records which step reads what.
- **You'll learn:** declare each step's inputs, outputs and parameters with Snakemake, rebuild from the raw data with one command, and watch a changed parameter rerun only the step that reads it. The same exercise in Nextflow, [2b](exercises/02-workflows/nextflow.md), for your own machine.
- **Data:** Palmer penguins, the 2007 field season.
- About 15 to 20 minutes.

{button}`Open in Binder <https://mybinder.org/v2/gh/ohpcsim/reproducibility-in-ai/binder-02-workflows?urlpath=lab/workspaces/exercise>` [Read the page](exercises/02-workflows/workflows.ipynb)
:::

:::{card} 3. Versioning data
**Do the 2008 and 2009 seasons change how much heavier male penguins are?**

- **Problem:** the data is in Git, and a new field season is coming.
- **You'll learn:** version data with DVC and a bucket, rerun the declared steps on a new version, and bring back an old version and its result.
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

1. Pick an exercise. If you're not sure, start with the first.
2. Select **Open in Binder**. Your browser opens a free temporary session with a terminal on the left and the instructions on the right, with everything installed. The first start can take a few minutes. A session has 2 GB of memory and ends when it sits idle, so download anything you want to keep.
3. Or [set up your environment](setup.md) on your own machine and use your own terminal with these pages. You don't need Jupyter, and your work stays with you.
4. Do the steps on the page, then run its check, `python ../check.py`.
5. To learn a tool, [Tools and documentation](tools.md) links to its documentation and its introduction.

The code here is MIT licensed. Each exercise names its data, its license and how to cite it.
