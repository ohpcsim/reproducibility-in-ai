# 2b. Workflows in Nextflow

The same workflow as `../workflows.ipynb`, written for Nextflow instead of Snakemake. The instructions are in `../nextflow.md`, or on the site. There is no Binder for this route; it runs on your own Linux, macOS or Windows (WSL2) machine.

- `environment.yml`: conda packages for this route, Nextflow and a Java runtime plus the Python packages the scripts need.
- `main.nf`: the starting workflow, with one process written and two to add.
- `nextflow.config`: hashes input files by content, so Nextflow reruns a step when a file's content changes, not its date.

From `exercises/02-workflows`:

```bash
conda env create --quiet --file nextflow/environment.yml
conda activate repro-nextflow
nextflow -version
python scripts/setup_project.py
cp nextflow/main.nf nextflow/nextflow.config project/
cd project
```

Run `python ../check.py --nextflow` from `project` to check your work.
