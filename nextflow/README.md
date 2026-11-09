# 2b. Workflows in Nextflow

The same workflow as `../workflows.ipynb`, written for Nextflow instead of Snakemake. The instructions are in `../nextflow.md`, or on the site. There's no Binder for it. It runs on your own Linux, macOS or Windows (WSL2) machine.

- `environment.yml`: conda packages for this route, Nextflow and a Java runtime plus the Python packages the scripts need.
- `main.nf`: the starting workflow, with three working processes. You add a fourth, `PLOT`.
- `nextflow.config`: hashes input files by content, so Nextflow reruns a step when a file's content changes, not its date.

From the folder you cloned:

```bash
conda env create --quiet --file nextflow/environment.yml
conda activate repro-nextflow
nextflow -version
python scripts/setup_project.py --nextflow
cd project
```

Run `python ../check.py --nextflow` from `project` to check your work.
