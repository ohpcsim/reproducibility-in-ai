# Model registry: which penguin model is live?

Train two values of C, register both with GTO, promote the better validation score and restore every version with DVC. About 15 to 20 minutes. Instructions are in `registry.ipynb`, or on the site.

[Open in Binder](https://mybinder.org/v2/gh/ohpcsim/reproducibility-in-ai/binder-04-registry?urlpath=lab/workspaces/exercise) for a terminal and the instructions side by side. Or use your own terminal on Linux, macOS, or Windows through WSL2:

```bash
conda env create --quiet --file .binder/environment.yml
conda activate repro-registry
python scripts/setup_project.py
cd project
```

Run `python ../check.py` from `project` to check your work. `--short` runs the same check.

For uv instead of conda, see "With uv instead of conda" on [the exercise page](https://ohpcsim.github.io/reproducibility-in-ai/registry).
