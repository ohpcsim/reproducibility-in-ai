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

## The exercises

- Each exercise stands on its own.
- Exercise 1 takes about 20 minutes. In exercises 2 to 5, the short path is step 1 and its check, about 15 minutes, and the rest is optional.
- Only reading? Each page shows the failure and how to approach the fix.

::::{grid} 1 1 2 2

:::{card} 1. Software environments
**Managing software environments**

- **Problem:** a script imports a package that the project's dependency files don't declare.
- **You'll learn:** declare and lock an environment with conda, then with uv, and why a conda lock is per platform and a uv lock isn't.
- **Data:** Palmer penguins, the 2007 field season.
- About 20 minutes.

{button}`Open in Binder <https://mybinder.org/v2/gh/ohpcsim/reproducibility-in-ai/binder-01-environments?urlpath=lab/workspaces/exercise>` [Read the page](exercises/01-environments/environments.ipynb)
:::

:::{card} 2. Workflows
**One command rebuilds the result**

- **Problem:** a README says "run these in this order", and nothing records which step reads what.
- **You'll learn:** declare each step's inputs, outputs and parameters with Snakemake, rebuild from the raw data with one command, and watch a changed parameter rerun only the step that reads it. The same exercise in Nextflow, for your own machine.
- **Data:** Palmer penguins, the 2007 field season.
- About 15 to 20 minutes.

{button}`Open in Binder <https://mybinder.org/v2/gh/ohpcsim/reproducibility-in-ai/binder-02-workflows?urlpath=lab/workspaces/exercise>` [Read the page](exercises/02-workflows/workflows.ipynb)
:::

:::{card} 3. DataOps
**Does a new field season change how body mass tracks flipper length in penguins?**

- **Problem:** a bad data delivery passes the pipeline.
- **You'll learn:** version data with DVC, stop a bad delivery, roll back, and record the repair.
- **Data:** Palmer penguins.
- 15 minutes for the short path, 35 for all of it.

{button}`Open in Binder <https://mybinder.org/v2/gh/ohpcsim/reproducibility-in-ai/binder-03-dataops?urlpath=lab/workspaces/exercise>` [Read the page](exercises/03-dataops/dataops.ipynb)
:::

:::{card} 4. Model registry
**Which digit classifier should we promote?**

- **Problem:** a candidate scores 1.000 and asks for promotion.
- **You'll learn:** register versions with DVC and GTO, refuse a bad candidate, and restore an old release from an empty folder.
- **Data:** scikit-learn's digits.
- 15 minutes for the short path, 40 for all of it.

{button}`Open in Binder <https://mybinder.org/v2/gh/ohpcsim/reproducibility-in-ai/binder-04-registry?urlpath=lab/workspaces/exercise>` [Read the page](exercises/04-registry/registry.ipynb)
:::

:::{card} 5. LLM documentation
**Can your tests catch a bad model card?**

- **Problem:** an LLM-written model card can be wrong, and "it looks good" isn't a check.
- **You'll learn:** write the tests first, run them over cards five tools wrote, and use a second model to find what's missing from the project.
- **Data:** recordings, so no model runs and you don't need a key.
- 15 minutes for the short path, 35 for all of it.

{button}`Open in Binder <https://mybinder.org/v2/gh/ohpcsim/reproducibility-in-ai/binder-05-llm?urlpath=lab/workspaces/exercise>` [Read the page](exercises/05-llm/llm.ipynb)
:::

::::

## How to start

It works the same way everywhere: read the page, and paste the commands into a terminal.

1. Pick an exercise. If you're not sure, start with the first.
2. Select **Open in Binder**. Your browser opens a free temporary session with a terminal on the left and the instructions on the right, with everything installed. The first start can take a few minutes. A session has 2 GB of memory and ends when it sits idle, so download anything you want to keep.
3. Or [set up your environment](setup.md) on your own machine and use your own terminal with these pages. You don't need Jupyter, and your work stays with you.
4. Do step 1, then run its check, `python ../check.py --short`.
5. To learn a tool, [Tools and documentation](tools.md) links to its documentation and its introduction.

Want to try the task yourself? [The same task in five tools](tools/five-tools.md) shows how to sign in, the exact command, what each tool wrote, and whether the tests accepted it: Claude Code, Codex, Cursor, a local model and free models.

Exercise 1 has an optional part you run yourself, on Linux or WSL2 with an NVIDIA GPU: [1c, PyTorch with a GPU](gpu/gpu.md), with conda, uv and containers.

The code here is MIT licensed. Each exercise names its data, its license and how to cite it.
