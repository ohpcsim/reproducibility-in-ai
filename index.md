---
title: Reproducibility in AI
subject: Hands-on exercises
---

These are the exercises from the Reproducibility in AI workshop at Rice Research Computing Day. You do them on your own time, in a browser or on your laptop. Each one gives you a project that's broken in a realistic way. You find the problem and fix it, and a script checks your work.

You don't need a GPU, a cluster or an account.

## The idea: literate science

In 1984 Donald Knuth proposed writing programs as one document, for people and for the machine at once. Literate science goes one step further. The claims, the code, the environment and the data live in one project, and every published result comes from running it. If the code breaks, the document breaks.

The document and the data are the pets, so you look after them. Everything that runs them is cattle, so you can delete it and build it again from what's in the project.

These pages work the same way. Each exercise page is a notebook that reruns when the site is published, and the failures on it are real output.

## The exercises

Each exercise stands on its own. The short path is one step and a check, about 15 minutes. The rest of each exercise is optional. If you're only reading, each page shows the failure and how to approach the fix.

::::{grid} 1 1 2 2

:::{card} 1. GitOps
**How fast is CO2 rising?**

Your group's published number won't rerun. Declare what's missing, find the commit that broke it, and prove the fix by deleting everything that runs it. With data from NOAA's Mauna Loa record.

15 minutes for the short path, 30 for all of it.

{button}`Open in Binder <https://mybinder.org/v2/gh/ohpcsim/reproducibility-in-ai/binder-01-gitops?urlpath=lab/tree/gitops.ipynb>` [Read the page](exercises/01-gitops/gitops.ipynb)
:::

:::{card} 2. DataOps
**Does a new field season change how body mass tracks flipper length in penguins?**

A bad delivery passes your pipeline. Make it stop, roll back with DVC, and repair the data on the record. With the Palmer penguins data.

15 minutes for the short path, 35 for all of it.

{button}`Open in Binder <https://mybinder.org/v2/gh/ohpcsim/reproducibility-in-ai/binder-02-dataops?urlpath=lab/tree/dataops.ipynb>` [Read the page](exercises/02-dataops/dataops.ipynb)
:::

:::{card} 3. Model registry
**Which digit classifier should we promote?**

Train and register versions with DVC and GTO. Refuse a candidate that scores 1.000, and get an old release back from an empty folder. With scikit-learn's digits data.

15 minutes for the short path, 40 for all of it.

{button}`Open in Binder <https://mybinder.org/v2/gh/ohpcsim/reproducibility-in-ai/binder-03-registry?urlpath=lab/tree/registry.ipynb>` [Read the page](exercises/03-registry/registry.ipynb)
:::

:::{card} 4. LLM documentation
**Can your tests catch a bad model card?**

Write the tests first, then run them over model cards written by LLMs. This one needs recorded runs that aren't ready yet, so there's no page or Binder for it today.

About 35 minutes, when it's ready.
:::

::::

## How to start

1. Pick an exercise. If you're not sure, start with the first.
2. Select **Open in Binder**. Your browser opens a free temporary session with everything installed. The first start can take a few minutes. A session has 2 GB of memory and ends when it sits idle, so download anything you want to keep.
3. Or [set up your laptop](setup.md), which takes about 10 minutes the first time. Your work stays with you.
4. Follow the notebook, and run `python check.py --short` when you finish step 1.

The code here is MIT licensed. Each exercise names its data, its license and how to cite it.
