---
title: Reproducibility in AI
subject: Hands-on exercises
---

- The exercises from the Reproducibility in AI workshop at Rice Research Computing Day.
- You do them on your own time, with these pages and a terminal.
- Each one gives you a broken project. You fix it, and a script checks your work.
- You don't need a GPU, a cluster or an account.

## The idea: literate science

- Literate programming: in 1984 Donald Knuth proposed writing a program as one document, for people and for the machine at once.
- Literate science goes one step further. The claims, the code, the environment and the data live in one project, and every published result comes from running it.
- If the code breaks, the document breaks.
- The document and the data are the pets, so you look after them.
- Everything that runs them is cattle, so you can delete it and build it again from what's in the project.
- This site works the same way. Each exercise page is a notebook that reruns when the site is published, and the failures on it are real output.

## The exercises

- Each exercise stands on its own.
- The short path is step 1 and its check, about 15 minutes. The rest is optional.
- Only reading? Each page shows the failure and how to approach the fix.

::::{grid} 1 1 2 2

:::{card} 1. GitOps
**How fast is CO2 rising?**

- **Problem:** a published number doesn't rerun.
- **You'll learn:** declare and lock an environment, find the breaking commit with `git bisect`, and rebuild from scratch.
- **Data:** NOAA's Mauna Loa CO2 record.
- 15 minutes for the short path, 30 for all of it.

{button}`Open in Binder <https://mybinder.org/v2/gh/ohpcsim/reproducibility-in-ai/binder-01-gitops?urlpath=lab/workspaces/exercise>` [Read the page](exercises/01-gitops/gitops.ipynb)
:::

:::{card} 2. DataOps
**Does a new field season change how body mass tracks flipper length in penguins?**

- **Problem:** a bad data delivery passes the pipeline.
- **You'll learn:** version data with DVC, stop a bad delivery, roll back, and record the repair.
- **Data:** Palmer penguins.
- 15 minutes for the short path, 35 for all of it.

{button}`Open in Binder <https://mybinder.org/v2/gh/ohpcsim/reproducibility-in-ai/binder-02-dataops?urlpath=lab/workspaces/exercise>` [Read the page](exercises/02-dataops/dataops.ipynb)
:::

:::{card} 3. Model registry
**Which digit classifier should we promote?**

- **Problem:** a candidate scores 1.000 and asks for promotion.
- **You'll learn:** register versions with DVC and GTO, refuse a bad candidate, and restore an old release from an empty folder.
- **Data:** scikit-learn's digits.
- 15 minutes for the short path, 40 for all of it.

{button}`Open in Binder <https://mybinder.org/v2/gh/ohpcsim/reproducibility-in-ai/binder-03-registry?urlpath=lab/workspaces/exercise>` [Read the page](exercises/03-registry/registry.ipynb)
:::

:::{card} 4. LLM documentation
**Can your tests catch a bad model card?**

- **Problem:** an LLM-written model card can be wrong, and "it looks good" isn't a check.
- **You'll learn:** write the tests first, run them over cards five tools wrote, and use a second model to find what's missing from the project.
- **Data:** recordings, so no model runs and you don't need a key.
- 15 minutes for the short path, 35 for all of it.

{button}`Open in Binder <https://mybinder.org/v2/gh/ohpcsim/reproducibility-in-ai/binder-04-llm?urlpath=lab/workspaces/exercise>` [Read the page](exercises/04-llm/llm.ipynb)
:::

::::

## How to start

It works the same way everywhere: read the page, and paste the commands into a terminal.

1. Pick an exercise. If you're not sure, start with the first.
2. Select **Open in Binder**. Your browser opens a free temporary session with a terminal on the left and the instructions on the right, with everything installed. The first start can take a few minutes. A session has 2 GB of memory and ends when it sits idle, so download anything you want to keep.
3. Or [set up your laptop](setup.md) and use your own terminal with these pages. You don't need Jupyter, and your work stays with you.
4. Do step 1, then run its check, `python ../check.py --short`.

Want to try the task yourself? [The same task in five tools](tools/five-tools.md) shows how to sign in, the exact command, what each tool wrote, and whether the tests accepted it: Claude Code, Codex, Cursor, a local model and free models.

Two more pages are optional, and you run them yourself: [if you need a GPU](gpu/gpu.md), and [if you need a container](gpu/container.md).

The code here is MIT licensed. Each exercise names its data, its license and how to cite it.
