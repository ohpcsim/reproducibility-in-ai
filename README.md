# 4. Model registry: which penguin model is live?

Train two values of C, register both with GTO, promote the one with the better validation score, restore a version by hand with Git and DVC, and check that every version restores. About 15 to 20 minutes. Instructions are in `registry.ipynb`, or on the site.

[Open in Binder](https://mybinder.org/v2/gh/ohpcsim/reproducibility-in-ai/binder-04-registry?urlpath=lab/workspaces/exercise) for a terminal and the instructions side by side. Or use your own terminal on Linux, macOS, or Windows through WSL2:

```bash
conda env create --quiet --file .binder/environment.yml
conda activate repro-registry
python scripts/setup_project.py
cd project
```

Run `python ../check.py` from `project` to check your work.

For uv instead of conda, see "With uv instead of conda" on [the exercise page](https://ohpcsim.github.io/reproducibility-in-ai/registry).
