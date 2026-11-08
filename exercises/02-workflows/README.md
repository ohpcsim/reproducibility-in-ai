# Workflows: add a step to a working workflow

About 15 to 20 minutes: run the penguin project's working Snakefile, add a step that draws the README's figure, and watch a changed parameter rerun one step. The instructions are in `workflows.ipynb`, or on the site. `nextflow.md` is the same exercise in Nextflow, for your own machine.

[Open in Binder](https://mybinder.org/v2/gh/ohpcsim/reproducibility-in-ai/binder-02-workflows?urlpath=lab/workspaces/exercise) for a terminal and the instructions side by side. Or use your own terminal on Linux, macOS, or Windows through WSL2:

```bash
conda env create --quiet --file .binder/environment.yml
conda activate repro-workflows
python scripts/setup_project.py
cd project
```

Run `python ../check.py` from `project` to check your work.
