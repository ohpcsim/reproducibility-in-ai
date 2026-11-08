---
title: Exercise 2 in Nextflow
---

- This page is optional. It redoes [Exercise 2, Workflows](workflows.ipynb) in Nextflow instead of Snakemake, with the same data, the same scripts and the same result.
- You run it on your own machine. There's no Binder for it, and the next section says why.
- If you did the Snakemake exercise, the problem is the one you know, and step 2 shows where the two tools differ.

## Learning objectives

- Write the README's three steps as Nextflow processes, each naming what it reads, what it writes and the command.
- Build the result from the raw data with one command, and commit it.
- See how Nextflow decides what's stale. `-resume` reruns a task when the hash of its inputs or script changed, and takes the rest from `work/`. File dates play no part.
- Compare the two tools on the same job.

## The problem

- The workshop's exercises use one project, a study of Palmer penguins, and add a capability in each exercise.
- `project` computes one table from the 2007 field season: how much heavier a male penguin is than a female of the same species, in grams, in three scripts, `clean.py`, `validate.py` and `report.py`.
- The README says to run the three in order, and after a change to `params.yaml` to "rerun the steps that need it".
- Nothing records which step reads what. A person has to know, every time.

## What you'll do

1. Step 1: complete `main.nf`, build from the raw data, and commit it.
2. Step 2: change a parameter, and watch what `-resume` reruns.
3. Run the check with `--nextflow`.

- The exercise takes about 15 to 20 minutes.

## Why there's no Binder

- Nextflow runs on the Java virtual machine. On our machines one run of this three-step workflow takes about 3 to 4 seconds, most of it starting Java, and peaks at 0.41 to 0.46 GB of memory. A Binder session has at least 1 GB and at most 2 GB, so one run would take a large share of it, next to JupyterLab.
- We checked whether the first run downloads anything. From the conda package it doesn't. The package carries the whole runtime, `~/.nextflow` held two empty folders after a run, and a run with the network switched off succeeded. Nextflow's own installer is different. [Its install page](https://docs.seqera.io/nextflow/install) says it downloads a Java bundle the first time each version runs, and that plugins download at run time.
- Nextflow is built for real machines, clusters and clouds. It has executors for SLURM and the other schedulers, Kubernetes and the cloud batch services, and the point of the tool is to move a workflow from a laptop to those.
- So use it on your own Linux or macOS machine, or on Windows through WSL2, on x86_64 or ARM. The environment file below solved on all four platforms, and we ran the exercise on three machines, listed at the end.

## Get a terminal

- You read this page and paste commands into a terminal. Nothing runs on the page.
- Linux or macOS, on x86_64 or ARM, or Windows through WSL2. On Windows, keep the folder in your WSL2 home, not under `/mnt/c`.
- You need [conda](../../setup.md). You don't need Jupyter or Java; the environment brings its own Java.
- Paste this once:

```bash
git clone --depth 1 https://github.com/ohpcsim/reproducibility-in-ai.git
cd reproducibility-in-ai/exercises/02-workflows
conda env create --quiet --file nextflow/environment.yml
conda activate repro-nextflow
export NXF_ANSI_LOG=false
nextflow -version
python scripts/setup_project.py
cp nextflow/main.nf nextflow/nextflow.config project/
cd project
```

- `conda activate` matters here. The Java runtime lives inside the environment, and `nextflow` finds it only after activation.
- `NXF_ANSI_LOG=false` makes Nextflow print one line per task, as recorded on this page. Without it, Nextflow redraws a live table in your terminal, with the same information.
- `nextflow -version` is the first run. It printed `version 26.10.5 build 14654` for us, and it also confirms that Nextflow found Java.
- Every command below runs in that `project` folder.
- To start over, go to the folder above it and run `python scripts/setup_project.py --reset`, then copy `main.nf` and `nextflow.config` in again. This deletes your work.

The environment:

```{literalinclude} nextflow/environment.yml
:language: yaml
```

- `nextflow` comes from bioconda and `openjdk` from conda-forge. Nextflow needs Java 17 or later, and the package pins that.
- [Nextflow's install page](https://docs.seqera.io/nextflow/install) prefers its own installer and warns that conda can lag behind. We use conda because the rest of this site does, and the version it gave was the current one.
- It took under 10 seconds to build on our machines, with the packages already downloaded, and takes about 1 GB of disk.

## The project

- `project` has the 2007 penguins, three scripts, `params.yaml` and a committed `metrics.json`, in one commit. It's the same project as the Snakemake exercise.
- You copied two files into it. `nextflow.config` has one line, and `main.nf` has one process written and two to add.

```{literalinclude} nextflow/nextflow.config
:language: groovy
```

```{literalinclude} nextflow/main.nf
:language: groovy
```

**Facts**

- A process is one step. `input:` lists the files it reads, `output:` the files it writes, and `script:` the command.
- Nextflow runs each task in its own folder under `work/`, named by the task's hash, and stages the inputs into it as links. The script has to be an input, or the task's folder won't have it. So does `params.yaml`, for the two scripts that read it.
- `path 'data/penguins.csv'` stages the file under that name, folder included, so the scripts run unchanged.
- `publishDir '.', mode: 'copy', overwrite: true` copies the outputs back into the project, with their folders. Without it, `results/clean.csv` would exist only inside `work/`. Without `overwrite: true`, a resumed run leaves a published file alone when the task came from the cache, and step 2 would end with a stale `metrics.json`.
- The `workflow` block connects the processes. `CLEAN(...)` returns a channel with `results/clean.csv`, and the next process takes it as input.
- `process.cache = 'deep'` in the config hashes input files by content. Nextflow's default hashes their name, size and modification time, which is the Snakemake way. Step 2 shows the difference.

## Step 1: declare the steps

**Problem.** The starter runs, and it runs only the first step. The other two steps aren't declared anywhere Nextflow can see.

```bash
nextflow run main.nf
git status --short
```

- Recorded November 8, 2026, on aarch64, Linux, Nextflow 26.10.5, OpenJDK 25.0.2. The project is in `~/workflows` here.

```text
$ nextflow run main.nf
[PIPELINE] main.nf | profile=standard
[WORKDIR] ~/workflows/project/work
[PROCESS 6a/73d19b] CLEAN

[SUCCESS] completed=1 failed=0 cached=0
$ git status --short
?? .nextflow.log
?? .nextflow/
?? main.nf
?? nextflow.config
?? work/
```

**Facts**

- `6a/73d19b` is the start of the task's hash, and `work/6a/73d19b.../` is its folder. `ls -a` in there shows the staged inputs, `.command.sh` with the command, `.command.log` with what it printed and `.exitcode`.
- `work/`, `.nextflow/` and `.nextflow.log` are cattle. Nextflow rebuilds them, so they go in `.gitignore`.
- `.nextflow/cache/` is where `-resume` looks up task hashes. Delete it and the next run starts from nothing, even with `work/` still there.

**Steps**

1. Tell Git what Nextflow writes.

```bash
printf 'work/\n.nextflow/\n.nextflow.log*\n' >> .gitignore
```

2. In `main.nf`, add a process `VALIDATE` and a process `REPORT` in the same form as `CLEAN`. `validate.py` reads `results/clean.csv` and writes `results/validated.csv`. `report.py` reads `results/validated.csv` and `params.yaml`, and writes `metrics.json`. Each has the same `publishDir` line, and each takes its script as an input.
3. In the `workflow` block, call them in order. `VALIDATE` takes `clean` and `file('validate.py')`. `REPORT` takes what `VALIDATE` returns, `file('params.yaml')` and `file('report.py')`.

```text
    validated = VALIDATE(clean, file('validate.py'))
    REPORT(validated, file('params.yaml'), file('report.py'))
```

4. Run it, and look at the result. All three tasks run, and the diff is empty, because the committed numbers were current. If Nextflow reports an error instead, it names the line in `main.nf`.

```bash
nextflow run main.nf
git diff metrics.json
```

```text
$ nextflow run main.nf
[PIPELINE] main.nf | profile=standard
[WORKDIR] ~/workflows/project/work
[PROCESS f7/684374] CLEAN
[PROCESS 2d/19da93] VALIDATE
[PROCESS 23/843d99] REPORT

[SUCCESS] completed=3 failed=0 cached=0
$ git diff metrics.json
```

5. Commit the workflow, its config and the ignore list.

```bash
git add .gitignore main.nf nextflow.config
git commit -m "Declare the three steps as Nextflow processes"
```

## Step 2: what -resume reruns

**Problem.** `params.yaml` says `statistic: mean`. Change it to `median`, and which tasks have to rerun? Nextflow decides from hashes, and `-resume` tells you what it decided.

**Facts**

- Without `-resume`, every run executes every task, and `work/` keeps the old task folders too.
- With `-resume`, Nextflow computes each task's hash from its inputs and its script, and looks it up in `.nextflow/cache/`. A match whose outputs are still in `work/` is reused and counted as `cached`. Anything else runs, and prints a `[PROCESS ...]` line. ([Cache and resume](https://docs.seqera.io/nextflow/cache-and-resume))
- With `process.cache = 'deep'`, an input file's hash is its content. A new date on an unchanged file changes nothing. ([The cache directive](https://docs.seqera.io/nextflow/reference/process/directives/cache))
- There's no dry run that says what would rerun. You run with `-resume` and read the lines.

**Steps**

1. Run again with nothing changed. All three tasks come from the cache.

```bash
nextflow run main.nf -resume
```

```text
$ nextflow run main.nf -resume
[PIPELINE] main.nf | profile=standard
[WORKDIR] ~/workflows/project/work

[SUCCESS] completed=0 failed=0 cached=3
```

2. Open `params.yaml`, change `statistic: mean` to `statistic: median`, save, and run with `-resume`. `params.yaml` is an input of `CLEAN` and of `REPORT`, so both rerun. `VALIDATE` doesn't: the new `results/clean.csv` has the same content as the old one, and content is what the hash sees. Snakemake, declaring the parameter sections per rule, reran only `report` here.

```bash
nextflow run main.nf -resume
cat metrics.json
```

```text
$ nextflow run main.nf -resume
[PIPELINE] main.nf | profile=standard
[WORKDIR] ~/workflows/project/work
[PROCESS 2a/b2ad97] CLEAN
[PROCESS 2b/aefcb4] REPORT

[SUCCESS] completed=2 failed=0 cached=1
$ cat metrics.json
{
  "dimorphism_g_adelie": 625.0,
  "dimorphism_g_chinstrap": 200.0,
  "dimorphism_g_gentoo": 925.0,
  "n_rows": 103
}
```

3. Change it back to `statistic: mean`, save, and run with `-resume`. Nothing runs. The old task folders are still in `work/`, their hashes match again, and `metrics.json` comes back from them. `git status --short` prints nothing. Snakemake reran `report` here, because the recorded parameter changed again.

```bash
nextflow run main.nf -resume
git status --short
```

```text
$ nextflow run main.nf -resume
[PIPELINE] main.nf | profile=standard
[WORKDIR] ~/workflows/project/work

[SUCCESS] completed=0 failed=0 cached=3
$ git status --short
```

## Check your work

- The same checker as the Snakemake exercise, with `--nextflow`. It clones your last commit into an empty folder, deletes every output, runs `nextflow run main.nf` there and compares the result with the one you committed. Then it changes `report.statistic`, runs with `-resume`, and reads Nextflow's log to see that `REPORT` ran and `VALIDATE` came from the cache.
- Each line says what to do next. It takes about 10 seconds. `--short` runs the same parts.

```bash
python ../check.py --nextflow
```

On the starter project it fails like this:

```text
$ python ../check.py --nextflow
Note: you have uncommitted changes. This checks your last commit only.

FAIL  No main.nf is committed. Write the processes in step 1, then git add main.nf and commit.

0 of 1 parts pass.
```

## Snakemake and Nextflow

| | Snakemake | Nextflow |
|---|---|---|
| The workflow file | `Snakefile`, Python with a rule syntax. Rules name input and output files, and Snakemake connects them by file name. | `main.nf`, a language built on Groovy, on the Java virtual machine. Processes name inputs and outputs, and you connect them in the `workflow` block. |
| Where a step runs | In the project folder. Outputs land where the rule says. | In its own folder under `work/`, with inputs staged as links. `publishDir` copies outputs back. |
| What's stale | A rule reruns when an input is newer than its output, or when its code, parameters, inputs or software environment are recorded as changed. `--rerun-triggers mtime` keeps only the dates. ([Snakemake command line](https://snakemake.readthedocs.io/en/stable/executing/cli.html)) | A task reruns when its hash isn't in the cache. The hash covers the inputs and the script. By default a file hashes by name, size and date. With `cache = 'deep'` it hashes by content. Nothing is reused unless you pass `-resume`. ([Cache and resume](https://docs.seqera.io/nextflow/cache-and-resume)) |
| A parameter | `configfile:` loads it, and a rule's `params:` names the part it reads. A change reruns that rule only. | `params.yaml` is a file input of every process that reads it. A change reruns them all, and content hashing spares the steps whose inputs came out the same. |
| Dry run | `snakemake -n` lists what would run. | `nextflow run main.nf -preview` checks the script and the wiring without running tasks. Nothing says what `-resume` would reuse. |
| One task at a time | `--cores 1` | Not needed here. The config can set `executor.cpus`. |
| Where it's common | Research groups and bioinformatics, with Python-heavy code. Rules with wildcards run over many samples. | Bioinformatics and clinical pipelines, clusters and clouds. The [nf-core](https://nf-co.re/) community maintains pipelines in it, and a company, Seqera, maintains the tool. |
| Scaling up | Executors and profiles for cluster schedulers and clouds. | Executors for SLURM and other schedulers, Kubernetes and the cloud batch services, switched by a config profile. |
| Start-up | A Python process. | A Java virtual machine, about 3 seconds and 0.4 to 0.5 GB here before any work. |
| Learn more | [Snakemake documentation](https://snakemake.readthedocs.io/en/stable/) | [Nextflow documentation](https://docs.seqera.io/nextflow/), [Hello Nextflow](https://training.nextflow.io/latest/hello_nextflow/) |

- The idea doesn't change. Each step names what it reads and what it writes, the tool knows what's stale, and one command rebuilds everything from the raw data.
- The two tools differ on how they know. Snakemake reads file dates first and keeps records next to them. Nextflow hashes.
- Both are declarations. The README was a procedure, and the person running it had to know.

## What we ran where

- Recorded November 8, 2026, with Nextflow 26.10.5, OpenJDK 25.0.2 and Python 3.12.16 from the environment file above.
- Each row is the whole page, run by a script: the starter and its failing check, step 1, step 2 and the final check. Peak memory is the largest resident set of any process in the run, which is the Java virtual machine.

| Machine | Starter fails | Solution passes | Whole page | Peak memory |
|---|---|---|---|---|
| aarch64, Linux, DGX Spark | Yes, 0 of 1 | Yes, 4 of 4 | 30 s | 0.44 GB |
| x86_64, WSL2 on Windows, Ubuntu 24.04 | Yes, 0 of 1 | Yes, 4 of 4 | 36 s | 0.46 GB |
| arm64, macOS 27.0.1 | Yes, 0 of 1 | Yes, 4 of 4 | 33 s | 0.41 GB |

- When you're done, `conda env remove --yes --name repro-nextflow` gets the disk back.
