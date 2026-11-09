# Reproducibility in AI

Hands-on exercises from the Reproducibility in AI workshop at Rice Research Computing Day, November 10, 2026.

**Start here: https://ohpcsim.github.io/reproducibility-in-ai/**

| Exercise | Question | Open in Binder |
|---|---|---|
| 1. Software environments | How do you declare and lock what the penguin project needs, with conda and with uv? | [Launch](https://mybinder.org/v2/gh/ohpcsim/reproducibility-in-ai/binder-01-environments?urlpath=lab/workspaces/exercise) |
| 2. Workflows | How do you add a step with Snakemake or Nextflow so one command builds the penguin project's numbers and figure? | [Launch](https://mybinder.org/v2/gh/ohpcsim/reproducibility-in-ai/binder-02-workflows?urlpath=lab/workspaces/exercise) |
| 3. Versioning data | Does adding the 2008 and 2009 data change our estimate of how much heavier male penguins are? | [Launch](https://mybinder.org/v2/gh/ohpcsim/reproducibility-in-ai/binder-03-dataops?urlpath=lab/workspaces/exercise) |
| 4. Model registry | Which penguin model is live? | [Launch](https://mybinder.org/v2/gh/ohpcsim/reproducibility-in-ai/binder-04-registry?urlpath=lab/workspaces/exercise) |

You read the page and paste commands into a terminal, on Binder or on your own machine. No GPU, cluster or account needed.

The site is built from this repository by `build_site.sh`, which runs each notebook in its own environment ([How this site is built](https://ohpcsim.github.io/reproducibility-in-ai/build)), so the output on its pages comes from real runs. Code is MIT licensed. Each exercise names its data, its license and how to cite it.
