# LLM documentation: can your tests catch a bad model card?

Short path, about 15 minutes: step 1 and its check. The full exercise takes about 35 minutes. The instructions are in `llm.ipynb`, or on the site.

[Open in Binder](https://mybinder.org/v2/gh/ohpcsim/reproducibility-in-ai/binder-04-llm?urlpath=lab/workspaces/exercise) for a terminal and the instructions side by side. Or use your own terminal on Linux, macOS, or Windows through WSL2:

```bash
conda env create --quiet --file .binder/environment.yml
conda activate repro-llm
python scripts/setup_project.py
cd project
```

Run `python ../check.py` from `project` to check your work.
