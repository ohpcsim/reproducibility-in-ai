---
title: 2b. Workflows in Nextflow
---

- This page is optional. It redoes [2a. Snakemake](workflows.ipynb) in Nextflow, with the same data, the same scripts and the same result.
+++ {"tags": ["track-mac", "track-linux", "track-wsl2"]}

- You run it on your own machine. There's no Binder for it, and the section "Why there's no Binder" below says why.

+++ {"tags": ["track-hpc"]}

- You run it on the cluster, with Nextflow's local executor. There's no Binder for it, and the section "Why there's no Binder" below says why.

+++

- If you did the Snakemake exercise, the problem is the one you know, and steps 2 and 3 show where the two tools differ.

## Learning objectives

- Start from a working Nextflow workflow, and read what each process reads and writes.
- Add a process written like the others, call it in the `workflow` block, and run with `-resume` so the other processes come from the cache.
- See how Nextflow decides what's stale. `-resume` reruns a task when the hash of its inputs or script changed, and takes the rest from `work/`. With this project's `cache = 'deep'`, file dates play no part.
- Compare the two tools on the same job.

## The problem

- The workshop's exercises use one project, [a study of Palmer penguins](../../project.md), and add a capability in each exercise.
- `project` has a working `main.nf` with three processes, `CLEAN`, `VALIDATE` and `REPORT`. They build `metrics.json` from the 2007 field season: how much heavier a male penguin is than a female of the same species, in grams.
- Its README shows a figure, `figures/body_mass.svg`. `plot.py` draws it, and nothing runs `plot.py`.
- [nf-core](https://nf-co.re/) pipelines are a common starting point in Nextflow. Groups often run one and add the step their study needs.

## What you'll do

1. Step 1: run the workflow you were given, and compare its numbers with this page.
2. Step 2: add a `PLOT` process that draws the figure, and commit `main.nf`.
3. Step 3: change a parameter, and see what `-resume` reruns.
4. Run the check with `--nextflow`.

- The exercise takes about 15 to 20 minutes.

## Why there's no Binder

- Nextflow runs on the Java virtual machine. On our machines one run of this workflow takes about 2 to 4 seconds, most of it starting Java, and peaks at 0.39 to 0.48 GB of memory. A Binder session has at least 1 GB and at most 2 GB, so one run would take a large share of it, next to JupyterLab.
- We checked whether the first run downloads anything. From the conda package it doesn't. The package carries the whole runtime, `~/.nextflow` held two empty folders after a run, and a run with the network switched off succeeded. Nextflow's own installer is different. [Its install page](https://docs.seqera.io/nextflow/install) says it needs Java on the machine, or, with `NXF_JAVA_BUNDLE=true`, downloads a Java bundle the first time each version runs.
- It has executors for SLURM and the other schedulers, Kubernetes and the cloud batch services, and the point of the tool is to move a workflow from a laptop to those.
+++ {"tags": ["track-mac", "track-linux", "track-wsl2"]}

- So use it on your own Linux or macOS machine, or on Windows through WSL2, on x86_64 or ARM. The environment file below solved on all four platforms, and we ran the exercise on three machines, listed at the end.

+++ {"tags": ["track-hpc"]}

- On a cluster, follow your site's rule for where short jobs run. One run takes a few seconds and under 0.5 GB. The environment file below solved on all four platforms. We ran the exercise on three machines, listed at the end, none of them a cluster.

+++

## Get a terminal

- You read this page and paste commands into a terminal. Nothing runs on the page.

+++ {"tags": ["track-wsl2"]}

- On Windows, keep the folder in your WSL2 home, not under `/mnt/c`.

+++

- You need [conda](../../setup.md). You don't need Jupyter or Java; the environment brings its own Java.
- Paste this once. The folder is `workflows-nextflow`, so it doesn't clash with a clone from another exercise:

```bash
git clone --branch binder-02-workflows --single-branch https://github.com/ohpcsim/reproducibility-in-ai.git workflows-nextflow
cd workflows-nextflow
conda env create --quiet --file nextflow/environment.yml
conda activate repro-nextflow
export NXF_ANSI_LOG=false
nextflow -version
python scripts/setup_project.py --nextflow
cd project
```

- If `conda env create` says the prefix already exists, an environment with that name is left from an earlier run. The rest of the block then uses that old environment and leaves a half-built `workflows-nextflow` folder. Remove both, then paste the block again: `conda deactivate; conda env remove -n repro-nextflow -y; cd ../..; rm -rf workflows-nextflow`
- The block leaves you in `workflows-nextflow/project`, so `cd ../..` goes to the folder above `workflows-nextflow`. If `cd project` failed too, use `cd ..` instead.
- `conda activate` matters here. The Java runtime lives inside the environment, and `nextflow` finds it only after activation.
- `NXF_ANSI_LOG=false` makes Nextflow print one plain line per task, `Submitted process` or `Cached process`, as recorded on this page. Without it, Nextflow redraws a live table in your terminal, with the same information.
- `nextflow -version` is the first run. It printed `version 26.10.5 build 14654` for us, and it also confirms that Nextflow found Java.
- Every command below runs in that `project` folder.
- In a new terminal, turn conda on as in [Set up](../../setup.md), then run `conda activate repro-nextflow`, `export NXF_ANSI_LOG=false` and `cd workflows-nextflow/project` from the folder above `workflows-nextflow`.
- To start over, run `cd ..` to leave `project`, then `python scripts/setup_project.py --nextflow --reset`. This deletes your work.

**Editing files**

- Use any text editor.
- If you're not sure, `nano FILE` works in the terminal. Ctrl+O, then Enter, saves. Ctrl+X quits.

The environment:

```{literalinclude} nextflow/environment.yml
:language: yaml
```

- `nextflow` comes from bioconda and `openjdk` from conda-forge. Nextflow needs Java 17 or later, and the package pins that.
- [Nextflow's install page](https://docs.seqera.io/nextflow/install) prefers its own installer and warns that conda can lag behind. We use conda because the rest of this site does, and the version it gave was the current one.
- It took under 10 seconds to build on our machines, with the packages already downloaded, and takes about 1 GB of disk.

## The project

- `project` has the 2007 penguins, four scripts, `params.yaml`, a README, `main.nf` and `nextflow.config`, in one commit. It's the Snakemake exercise's project, with `main.nf` in place of the Snakefile. Nothing built is in Git.
- `nextflow.config` has one line, and `main.nf` has three processes:

```{literalinclude} nextflow/nextflow.config
:language: groovy
```

```{literalinclude} nextflow/main.nf
:language: groovy
```

**Facts**

- A process is one step. `input:` lists the files it reads, `output:` the files it writes, and `script:` the command.
- Nextflow runs each task in its own folder under `work/`, named by the task's hash, and stages the inputs into it as links. The script has to be an input, or the task's folder won't have it. So does `params.yaml`, for `report.py`, which reads it.
- `path 'data/penguins.csv'` stages the file under that name, folder included, so the scripts run unchanged.
- `publishDir '.', mode: 'copy', overwrite: true` copies the outputs back into the project, with their folders. Without it, `results/clean.csv` would exist only inside `work/`. Without `overwrite: true`, a resumed run leaves a published file alone when the task came from the cache, and step 3 would end with a stale `metrics.json`.
- The `workflow` block connects the processes. `CLEAN(...)` returns a channel with `results/clean.csv`, and the next process takes it as input.
- `process.cache = 'deep'` in the config hashes input files by content. Nextflow's default hashes their name, size and modification time.
- `.gitignore` lists what's built: `results/`, `metrics.json`, `figures/`, and what Nextflow writes, `work/`, `.nextflow/` and `.nextflow.log`.

## Step 1: run the workflow you were given

**Problem:** before you change a workflow, run it, and check that you get the numbers its authors got.

```bash
nextflow run main.nf
cat metrics.json
git status --short
```

- Recorded November 8, 2026, on aarch64, Linux, Nextflow 26.10.5, OpenJDK 25.0.2. Your task hashes and run names will differ, and after your edit in step 2, so will the `revision:` ID.

```text
$ nextflow run main.nf
N E X T F L O W  ~  version 26.10.5
Launching `main.nf` [gigantic_sanger] - revision: 35154abeca
[ee/648ebf] Submitted process > CLEAN
[c3/9a1999] Submitted process > VALIDATE
[31/3ee53b] Submitted process > REPORT
$ cat metrics.json
{
  "dimorphism_g_adelie": 648.9,
  "dimorphism_g_chinstrap": 250.0,
  "dimorphism_g_gentoo": 934.2,
  "n_rows": 103
}
$ git status --short
```

**Facts**

- `ee/648ebf` is the start of the task's hash, and `work/ee/648ebf.../` is its folder. `ls -a` in there shows the staged inputs, `.command.sh` with the command, `.command.log` with what it printed and `.exitcode`.
- `metrics.json` holds the numbers on this page: Adelie males are 648.9 g heavier, Chinstrap males 250.0 g and Gentoo males 934.2 g, from 103 penguins. The same numbers from the raw data, on your machine, show that the workflow reproduces the result.
- `git status --short` prints nothing. What Nextflow builds is in `.gitignore`.
- With `NXF_ANSI_LOG=false`, Nextflow prints the plain log: a banner, the run's name, and one line per task. It prints no summary line at the end.

**Steps**

1. Run the commands above, and check that `metrics.json` has the numbers on this page.
2. Read `main.nf`. For each process, find what it reads and what it writes, and in the `workflow` block, which process takes which output.

## Step 2: add a step

**Problem:** the README shows a figure that nothing builds.

```bash
grep body_mass README.md
ls figures
```

```text
$ grep body_mass README.md
![Body mass by species and sex](figures/body_mass.svg)
- The workflow reads `data/penguins.csv` and writes `metrics.json`, the difference per species, and `figures/body_mass.svg`, the figure above. Neither is in Git. The workflow builds them.
$ ls figures
ls: cannot access 'figures': No such file or directory
```

**Facts**

- `plot.py` reads `results/validated.csv` and writes `figures/body_mass.svg`, body mass by species and sex.
- A new process is written like the others, with the same `publishDir` line, and takes its script as an input.
- A process runs only if the `workflow` block calls it. `VALIDATE` returns `validated`, so `PLOT` takes it, like `REPORT` does.
- With `-resume`, Nextflow computes each task's hash from its inputs and its script, and looks it up in `.nextflow/cache/`. A match whose outputs are still in `work/` is reused, and prints `Cached process`. Anything else runs, and prints `Submitted process`. ([Cache and resume](https://docs.seqera.io/nextflow/cache-and-resume))
- Without `-resume`, every run executes every task, and `work/` keeps the old task folders too.
- There's no dry run that says what would rerun. You run with `-resume` and read the lines.

**Steps**

1. In `main.nf`, add a process `PLOT`, written like `REPORT`. It reads `results/validated.csv` and `plot.py`, writes `figures/body_mass.svg`, and runs `python plot.py`:

```text
process PLOT {
    publishDir '.', mode: 'copy', overwrite: true

    input:
    path 'results/validated.csv'
    path 'plot.py'

    output:
    path 'figures/body_mass.svg'

    script:
    "python plot.py"
}
```

2. In the `workflow` block, call it after `REPORT`:

```text
    PLOT(validated, file('plot.py'))
```

3. Run it with `-resume`, and look at the figure. The three tasks from step 1 come from the cache, and only `PLOT` runs. If Nextflow reports an error instead, it names the line in `main.nf`.

```bash
nextflow run main.nf -resume
ls figures
```

```text
$ nextflow run main.nf -resume
N E X T F L O W  ~  version 26.10.5
Launching `main.nf` [sick_gautier] - revision: 1278b01991
[ee/648ebf] Cached process > CLEAN
[c3/9a1999] Cached process > VALIDATE
[31/3ee53b] Cached process > REPORT
[71/ec0dc8] Submitted process > PLOT
$ ls figures
body_mass.svg
```

- `PLOT` and `REPORT` both wait only for `VALIDATE`, so here and in step 3 the order of their lines can differ on your machine.

+++ {"tags": ["track-mac", "track-linux", "track-wsl2"]}

- Open `figures/body_mass.svg` in a web browser, or `README.md` in a Markdown viewer.

+++ {"tags": ["track-hpc"]}

- Copy `figures/body_mass.svg` to your laptop with `scp` and open it there.

+++

4. Commit `main.nf`. The figure is built, not committed, so `git status --short` prints nothing after the commit.

```bash
git add main.nf
git commit -m "Draw the figure with a PLOT process"
git status --short
```

## Step 3: change a parameter

**Problem:** `params.yaml` says `statistic: mean`. If you change it to `median`, which tasks have to rerun? Nextflow decides from hashes, and `-resume` tells you what it decided.

**Facts**

- `params.yaml` is an input of `REPORT` only. `PLOT` reads `results/validated.csv`, which doesn't change.
- With `process.cache = 'deep'`, an input file's hash is its content. A new date on an unchanged file changes nothing. ([The cache directive](https://docs.seqera.io/nextflow/reference/process/directives/cache))

**Steps**

1. Open `params.yaml`, change `statistic: mean` to `statistic: median`, save, and run with `-resume`. `REPORT` reruns. `CLEAN`, `VALIDATE` and `PLOT` come from the cache. Snakemake reran only `report` here too.

```bash
nextflow run main.nf -resume
cat metrics.json
```

```text
$ nextflow run main.nf -resume
N E X T F L O W  ~  version 26.10.5
Launching `main.nf` [festering_brenner] - revision: 1278b01991
[ee/648ebf] Cached process > CLEAN
[c3/9a1999] Cached process > VALIDATE
[71/ec0dc8] Cached process > PLOT
[d5/2279da] Submitted process > REPORT
$ cat metrics.json
{
  "dimorphism_g_adelie": 625.0,
  "dimorphism_g_chinstrap": 200.0,
  "dimorphism_g_gentoo": 925.0,
  "n_rows": 103
}
```

2. Change it back to `statistic: mean`, save, and run with `-resume`. Nothing runs. The old task folders are still in `work/`, their hashes match again, and `metrics.json` comes back from them. `git status --short` prints nothing. Snakemake reran `report` here, because the recorded parameter changed again.

```bash
nextflow run main.nf -resume
git status --short
```

```text
$ nextflow run main.nf -resume
N E X T F L O W  ~  version 26.10.5
Launching `main.nf` [furious_bose] - revision: 1278b01991
[ee/648ebf] Cached process > CLEAN
[c3/9a1999] Cached process > VALIDATE
[71/ec0dc8] Cached process > PLOT
[31/3ee53b] Cached process > REPORT
$ git status --short
```

## Check your work

- The same checker as the Snakemake exercise, with `--nextflow`. It clones your last commit into an empty folder, runs `nextflow run main.nf` there, compares the numbers with this page and checks which penguins the figure plots. Then it changes `report.statistic`, runs with `-resume`, and reads Nextflow's log to see that only `REPORT` ran.
- Each FAIL line says what to fix. It takes about 10 seconds.

```bash
python ../check.py --nextflow
```

On the starter project it fails like this:

```text
$ python ../check.py --nextflow
FAIL  main.nf has no PLOT process called in the workflow block. Add it in step 2, then commit main.nf.
PASS  In a clean clone, nextflow run main.nf builds metrics.json from the raw data, and the numbers match the page
FAIL  The build wrote no figures/body_mass.svg. README.md shows it, so declare the step that draws it (step 2).
PASS  A changed report.statistic reruns REPORT, and -resume takes the rest from the cache: CLEAN, VALIDATE

2 of 4 parts pass.
```

## Snakemake and Nextflow

| | Snakemake | Nextflow |
|---|---|---|
| The workflow file | `Snakefile`, Python with a rule syntax. Rules name input and output files, and Snakemake connects them by file name. | `main.nf`, written in a language built on Groovy that runs on the Java virtual machine. Processes name inputs and outputs, and you connect them in the `workflow` block. |
| Where a step runs | In the project folder. Outputs land where the rule says. | In its own folder under `work/`, with inputs staged as links. `publishDir` copies outputs back. |
| What's stale | A rule reruns when an input is newer than its output, or when its code, parameters, inputs or software environment are recorded as changed. `--rerun-triggers mtime` keeps only the dates. ([Snakemake command line](https://snakemake.readthedocs.io/en/stable/executing/cli.html)) | A task reruns when its hash isn't in the cache. The hash covers the inputs and the script. By default a file hashes by name, size and date. With `cache = 'deep'` it hashes by content. Nothing is reused unless you pass `-resume`. ([Cache and resume](https://docs.seqera.io/nextflow/cache-and-resume)) |
| A parameter | `configfile:` loads it, and a rule's `params:` names the part it reads. A change reruns that rule only. | `params.yaml` is a file input of every process that reads it. A change to any part of the file reruns each of them. |
| Dry run | `snakemake -n` lists what would run. | `nextflow run main.nf -preview` checks the script and the wiring without running tasks. Nothing says what `-resume` would reuse. |
| One task at a time | `--cores 1` | Not needed here. The config can set `executor.cpus`. |
| Where it's common | Research groups and bioinformatics, with Python-heavy code. Rules with wildcards run over many samples. | Bioinformatics and clinical pipelines, clusters and clouds. The [nf-core](https://nf-co.re/) community maintains pipelines in it, and a company, Seqera, maintains the tool. |
| Scaling up | Executors and profiles for cluster schedulers and clouds. | Executors for SLURM and other schedulers, Kubernetes and the cloud batch services, switched by a config profile. |
| Start-up | A Python process. | A Java virtual machine. One run of this workflow takes 2 to 4 seconds here, most of it starting Java, and peaks at 0.39 to 0.48 GB. |
| Learn more | [Snakemake documentation](https://snakemake.readthedocs.io/en/stable/) | [Nextflow documentation](https://docs.seqera.io/nextflow/), [Hello Nextflow](https://training.nextflow.io/latest/hello_nextflow/) |

- The idea doesn't change. Each step names what it reads and what it writes, the tool knows what's stale, and one command rebuilds everything from the raw data.
- The two tools differ in how they decide what's stale. Snakemake reads file dates first and keeps records next to them. Nextflow hashes.
- In both, a new step is one more declaration, written like the others, and the tool runs only what's new or stale.

## What we ran where

- Recorded November 8, 2026, with Nextflow 26.10.5, OpenJDK 25.0.2 and Python 3.12.16 from the environment file above.
- A script ran the whole current page on each machine: the starter and its failing check, the three steps and the final check. Peak memory is the largest resident set of any process in the run, which is the Java virtual machine.

| Machine | Starter fails | Solution passes | Whole page | Peak memory |
|---|---|---|---|---|
| aarch64, Linux, DGX Spark | Yes, 2 of 4 | Yes, 4 of 4 | 45 s | 0.47 GB |
| x86_64, WSL2 on Windows, Ubuntu 24.04 | Yes, 2 of 4 | Yes, 4 of 4 | 29 s | 0.48 GB |
| arm64, macOS 27.0.1 | Yes, 2 of 4 | Yes, 4 of 4 | 31 s | 0.39 GB |

+++ {"tags": ["track-hpc"]}

- We haven't run this on an HPC cluster.

+++

## When you're done

From the folder above `workflows-nextflow`:

```bash
conda deactivate
conda env remove --yes --name repro-nextflow
rm -rf workflows-nextflow
```
