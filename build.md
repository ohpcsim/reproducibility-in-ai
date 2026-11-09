---
title: How this site is built
---

:::{figure} slides/how-built.png
:alt: One repository holds the pages, notebooks, data, environment files and build scripts. Publishing: a push to main runs GitHub Actions, which builds each exercise's environment from its environment.yml; tracks.py writes each page's copy for Binder, Mac, Linux, WSL2 and HPC; Jupyter Book reruns every notebook and the results page, and a failing cell stops the build; GitHub Pages serves the site. Running: one branch per exercise, made by make_binder_branches.sh; mybinder.org's repo2docker builds an image from the same environment.yml and reuses it; learners get JupyterLab in the browser. Your own machine: clone the branch and build the same environments from its files, with conda or uv. Everything after the repository is rebuilt from it.
How this site and its Binder sessions are built from one repository.
:::

## What this site is

- Exercises 1a, 2a, 3 and 4 are notebooks. They rerun when the site is published, so their output is real, but it's teaching output, not results. 1b, 1c and 2b show recorded output.
- [The results page](results/results.ipynb) is the literate-science example: the penguin study's numbers, rebuilt from the project's code on every publish, and a figure the page draws from the project's validated table.
- The site follows its own advice: everything it needs is declared in the repository, it rebuilds from scratch, and the build fails if a notebook raises an error or a cross-reference breaks.
- It isn't a research publication. [The penguin analysis](project.md) is a teaching example on published data.

## The tools

- This site is a project too. Its pages, its configuration and the automation that builds it are in [one repository](https://github.com/ohpcsim/reproducibility-in-ai).
- [Jupyter Book 2](https://jupyterbook.org/stable/) builds it, on [mystmd](https://mystmd.org/guide).
- The exercise notebooks and the results page rerun in the build, so their output comes from a real run.

## The configuration

`myst.yml` names the pages, their order and the theme. `tracks.py` writes each track's copy of a page from one source, before the build.

```{literalinclude} myst.yml
:language: yaml
```

## Build it on your own machine

- Each notebook has to run in its own environment. Exercise 1's failure needs pandas to be missing, and the results page needs matplotlib.
- So first build five environments: one for each exercise, from its `.binder/environment.yml` plus `ipykernel` and `jupyter_server`, and one for the results page, from `results/environment.yml` plus `jupyter_server`:

```bash
for exercise in 01-environments 02-workflows 03-dataops 04-registry; do
  conda env create --quiet --prefix "envs/$exercise" --file "exercises/$exercise/.binder/environment.yml"
  conda install --quiet --yes --prefix "envs/$exercise" ipykernel jupyter_server
done
conda env create --quiet --prefix envs/results --file results/environment.yml
conda install --quiet --yes --prefix envs/results jupyter_server
```

- `results/environment.yml` isn't locked yet. It names its packages without versions, so a later build can solve newer ones.

- Install Jupyter Book with `pip install "jupyter-book==2.1.7"`.
- Then one command builds the site into `_build/html`. Run it in a fresh clone, because running the notebooks writes `project/` folders, and `tracks.py` writes each track's pages over their sources. A second build needs another fresh clone.

```bash
./build_site.sh envs/01-environments envs/02-workflows envs/03-dataops envs/04-registry envs/results
```

- The script builds each notebook alone, as a one-page site, with its own environment first on `PATH`.
- Jupyter Book caches each notebook's outputs, keyed by its code, in `_build/execute`. The script copies those to the whole site's `_build/execute`.
- The last command builds the whole site with `--execute --strict`. It reuses the cached outputs, so no notebook runs in the wrong environment.
- `--strict` turns every warning into a failure, so a broken cross-reference or a Python error in a notebook cell stops the build. The exercise pages record what each shell command prints, pass or fail, because the starter checks are meant to fail.

```{literalinclude} build_site.sh
:language: bash
```

## The automation on each push

- A GitHub Actions workflow runs the same build on every push to `main`, then publishes `_build/html` to GitHub Pages.
- It builds each exercise's environment from its `.binder/environment.yml`, so the site runs on what a learner gets, and the results page's from `results/environment.yml`.

```{literalinclude} .github/workflows/site.yml
:language: yaml
```

## Binder

- Each exercise has its own branch, such as `binder-01-environments`. The branch's root is that exercise's folder.
- `make_binder_branches.sh` makes the four branches from the site's commit. A person pushes them.
- mybinder.org builds an image from the branch's `.binder/` folder the first time someone opens the link after the branch changes, and reuses it after that.
- So a learner's environment comes from the same `environment.yml` that the site's build used.
- [The Binder page](setup.md) has the launch links.

### How it works

- [How Binder works](setup.md#how-binder-works), on the Binder page, explains repo2docker, BinderHub, each branch's `.binder/` files, the launch links and the session limits.

## Other tools that do this

- [Quarto](https://quarto.org/docs/projects/code-execution.html) renders websites from notebooks and Markdown with executable code, and can store results so a full render doesn't rerun them.
- [Sphinx](https://www.sphinx-doc.org/en/master/) with [MyST-NB](https://myst-nb.readthedocs.io/en/latest/computation/execute.html) runs notebooks during the build and caches their outputs. Errors fail the build only with `-W` or `nb_execution_raise_on_error`.
