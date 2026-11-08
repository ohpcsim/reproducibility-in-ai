# Reproducibility in AI

Hands-on exercises from the Reproducibility in AI workshop at Rice Research Computing Day, November 10, 2026.

**Start here: https://ohpcsim.github.io/reproducibility-in-ai/**

| Exercise | Question | Open in Binder |
|---|---|---|
| 1. Software environments | How do you declare and lock what the penguin project needs, with conda and with uv? | [Launch](https://mybinder.org/v2/gh/ohpcsim/reproducibility-in-ai/binder-01-environments?urlpath=lab/workspaces/exercise) |
| 2. Workflows | How do you declare the penguin project's steps so one command rebuilds the result, with Snakemake or Nextflow? | [Launch](https://mybinder.org/v2/gh/ohpcsim/reproducibility-in-ai/binder-02-workflows?urlpath=lab/workspaces/exercise) |
| 3. DataOps | Does a new field season change how body mass tracks flipper length in penguins? | [Launch](https://mybinder.org/v2/gh/ohpcsim/reproducibility-in-ai/binder-03-dataops?urlpath=lab/workspaces/exercise) |
| 4. Model registry | Which digit classifier should we promote? | [Launch](https://mybinder.org/v2/gh/ohpcsim/reproducibility-in-ai/binder-04-registry?urlpath=lab/workspaces/exercise) |
| 5. LLM documentation | Can your tests catch a bad model card? | [Launch](https://mybinder.org/v2/gh/ohpcsim/reproducibility-in-ai/binder-05-llm?urlpath=lab/workspaces/exercise) |

You read the page and paste commands into a terminal, on Binder or on your own machine. No GPU, cluster or account needed.

The site is built from this repository with `jupyter-book build --execute --strict`, so the output on its pages comes from real runs. Code is MIT licensed. Each exercise names its data, its license and how to cite it.
