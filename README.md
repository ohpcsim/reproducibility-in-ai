# 1a. Managing software environments

About 20 minutes: declare a missing package and lock the environment, first with conda, then with uv. The instructions are in `environments.ipynb`, or on the site.

[Open in Binder](https://mybinder.org/v2/gh/ohpcsim/reproducibility-in-ai/binder-01-environments?urlpath=lab/workspaces/exercise) for a terminal and the instructions side by side. Or use your own terminal on Linux, macOS, or Windows through WSL2:

```bash
conda env create --quiet --file .binder/environment.yml
conda activate repro-environments
python scripts/setup_project.py
cd project
```

Run `python ../check.py` from `project` to check your work.
