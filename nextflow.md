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

- `project` computes one number from the 2024 earthquake catalog, the Gutenberg-Richter b-value. With b near 1, there are about ten magnitude 5 earthquakes for each magnitude 6.
- The README says to run `subset.py`, `count.py` and `fit.py` in order, and after a change to `params.yaml` to "rerun the steps that need it".
- The last commit limited the catalog to shallow earthquakes and reran only `fit.py`. The committed number comes from the whole catalog, and nothing says so.
- The fit also starts at magnitude 4.0, where the catalog isn't complete, so the number is wrong a second way.

## What you'll do

1. Step 1: complete `main.nf`, build from the raw data, and commit the fresh result. This is the short path, about 15 minutes, and it has its own check.
2. Step 2, optional, about 20 minutes: change a parameter, a date and a script, and watch what `-resume` reruns. Then add the step the README skipped, choose the start magnitude, and rebuild everything from nothing.

## Why there's no Binder

- Nextflow runs on the Java virtual machine. On our machines one run of this four-step workflow takes about 3 to 4 seconds, most of it starting Java, and peaks at 0.35 to 0.49 GB of memory. A Binder session has at least 1 GB and at most 2 GB, so one run would take a large share of it, next to JupyterLab.
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

- `conda activate` matters here. On macOS the Java runtime lives inside the environment and `nextflow` finds it only after activation.
- `NXF_ANSI_LOG=false` makes Nextflow print one line per task, as recorded on this page. Without it, Nextflow redraws a live table in your terminal, with the same information.
- `nextflow -version` is the first run. It printed this, and it also confirms that Nextflow found Java.
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

- `project` has the 2024 catalog, three scripts, `params.yaml` and a committed `metrics.json`, in two commits. It's the same project as the Snakemake exercise.
- You copied two files into it. `nextflow.config` has one line, and `main.nf` has one process written and two to add.

```{literalinclude} nextflow/nextflow.config
:language: groovy
```

```{literalinclude} nextflow/main.nf
:language: groovy
```

**Facts**

- A process is one step. `input:` lists the files it reads, `output:` the files it writes, and `script:` the command.
- Nextflow runs each task in its own folder under `work/`, named by the task's hash, and stages the inputs into it as links. The script has to be an input, or the task's folder won't have it.
- `path 'data/earthquakes.csv'` stages the file under that name, folder included, so the scripts run unchanged.
- `publishDir '.', mode: 'copy'` copies the outputs back into the project, with their folders. Without it, `results/subset.csv` would exist only inside `work/`.
- The `workflow` block connects the processes. `SUBSET(...)` returns a channel with `results/subset.csv`, and the next process takes it as input.
- `process.cache = 'deep'` in the config hashes input files by content. Nextflow's default hashes their name, size and modification time, which is the Snakemake way. Step 2 shows the difference.

## Step 1: declare the steps

**Problem.** The starter runs, and it runs only the first step. The committed number doesn't move.

```bash
nextflow run main.nf
git status --short
```

- Recorded November 8, 2026, on aarch64, Linux, Nextflow 26.10.5, OpenJDK 25.0.2. The project is in `~/workflows` here.

```text
$ nextflow run main.nf
N E X T F L O W  ~  version 26.10.5
Launching `main.nf` [backstabbing_brenner] - revision: cff54d0cac
[f5/415e8f] Submitted process > SUBSET
$ git status --short
?? .nextflow.log
?? .nextflow/
?? main.nf
?? nextflow.config
?? work/
```

**Facts**

- `[f5/415e8f]` is the start of the task's hash, and `work/f5/415e8f.../` is its folder. `ls -a` in there shows the staged inputs, `.command.sh` with the command, `.command.log` with what it printed and `.exitcode`.
- `work/`, `.nextflow/` and `.nextflow.log` are cattle. Nextflow rebuilds them, so they go in `.gitignore`.
- `.nextflow/cache/` is where `-resume` looks up task hashes. Delete it and the next run starts from nothing, even with `work/` still there.

**Steps**

1. Tell Git what Nextflow writes.

```bash
printf 'work/\n.nextflow/\n.nextflow.log*\n' >> .gitignore
```

2. In `main.nf`, add a process `COUNT` and a process `FIT` in the same form as `SUBSET`. `count.py` reads `results/subset.csv` and writes `results/counts.csv`. `fit.py` reads `results/counts.csv` and writes `metrics.json`. Each has `publishDir '.', mode: 'copy'`, and each takes its script as an input.
3. In the `workflow` block, call them in order. `COUNT` takes `subset` and `file('count.py')`. `FIT` takes what `COUNT` returns and `file('fit.py')`.

```text
    counts = COUNT(subset, file('count.py'))
    FIT(counts, file('fit.py'))
```

4. Run it, and look at the result. The diff is the one the README procedure gives when it's run in full, the same as in the Snakemake exercise. If Nextflow reports an error instead, it names the line in `main.nf`.

```bash
nextflow run main.nf
git diff metrics.json
```

```text
$ nextflow run main.nf
N E X T F L O W  ~  version 26.10.5
Launching `main.nf` [spontaneous_bernard] - revision: 8f977013ac
[d0/bc7982] Submitted process > SUBSET
[25/4c00f0] Submitted process > COUNT
[05/657447] Submitted process > FIT
$ git diff metrics.json
diff --git a/metrics.json b/metrics.json
index 9fe5fac..443aae2 100644
--- a/metrics.json
+++ b/metrics.json
@@ -1,7 +1,7 @@
 {
-  "b_value": 0.802,
-  "b_uncertainty": 0.007,
-  "quakes_per_unit_magnitude": 6.3,
-  "n_earthquakes": 14175,
+  "b_value": 0.744,
+  "b_uncertainty": 0.008,
+  "quakes_per_unit_magnitude": 5.5,
+  "n_earthquakes": 9496,
   "lowest_magnitude": 4.0
 }
```

5. Commit the workflow, its config, the ignore list and the fresh result.

```bash
git add .gitignore main.nf nextflow.config metrics.json
git commit -m "Declare the three steps as Nextflow processes, and rebuild the result from the raw data"
```

### Check the short path

- The same checker as the Snakemake exercise, with `--nextflow`. It clones your last commit into an empty folder, runs `nextflow run main.nf` there, and compares the result with the one you committed.
- Each line says what to do next.

```bash
python ../check.py --nextflow --short
```

On the starter project it fails like this:

```text
$ python ../check.py --nextflow --short
Note: you have uncommitted changes. This checks your last commit only.

FAIL  No main.nf is committed. Write the processes in step 1, then git add main.nf and commit.

0 of 1 parts pass.
```

## Step 2 (optional): what -resume reruns

**Facts**

- Without `-resume`, every run executes every task, and `work/` keeps the old task folders too.
- With `-resume`, Nextflow computes each task's hash from its inputs, its script and its parameters, and looks it up in `.nextflow/cache/`. A match whose outputs are still in `work/` is reused and printed as `Cached process`. Anything else is `Submitted`. ([Cache and resume](https://docs.seqera.io/nextflow/cache-and-resume))
- With `process.cache = 'deep'`, an input file's hash is its content. A new date on an unchanged file changes nothing. ([The cache directive](https://docs.seqera.io/nextflow/reference/process/directives/cache))
- There's no dry run that says what would rerun. You run with `-resume` and read the lines.

**Steps**

1. Run again with nothing changed. All three tasks come from the cache.

```bash
nextflow run main.nf -resume
```

```text
$ nextflow run main.nf -resume
N E X T F L O W  ~  version 26.10.5
Launching `main.nf` [trusting_monod] - revision: 8f977013ac
[d0/bc7982] Cached process > SUBSET
[25/4c00f0] Cached process > COUNT
[05/657447] Cached process > FIT
```

2. Change `max_depth_km` in `params.yaml` to 300, save, and run with `-resume`. The parameter is an input of `SUBSET`, so `SUBSET` reruns, and so does everything that reads what it wrote.

```bash
nextflow run main.nf -resume
cat metrics.json
```

```text
$ nextflow run main.nf -resume
N E X T F L O W  ~  version 26.10.5
Launching `main.nf` [silly_agnesi] - revision: 8f977013ac
[d4/f69e94] Submitted process > SUBSET
[c5/c7e118] Submitted process > COUNT
[d5/b639ab] Submitted process > FIT
$ cat metrics.json
{
  "b_value": 0.784,
  "b_uncertainty": 0.007,
  "quakes_per_unit_magnitude": 6.1,
  "n_earthquakes": 12964,
  "lowest_magnitude": 4.0
}
```

3. Put the parameter back, and run with `-resume`. Nothing runs. The old task folders are still in `work/`, their hashes match again, and `metrics.json` comes back from them. Snakemake would rerun all three here, because `params.yaml` is newer than the outputs.

```bash
git checkout -- params.yaml
nextflow run main.nf -resume
```

```text
$ git checkout -- params.yaml
$ nextflow run main.nf -resume
N E X T F L O W  ~  version 26.10.5
Launching `main.nf` [voluminous_lorenz] - revision: 8f977013ac
[d0/bc7982] Cached process > SUBSET
[25/4c00f0] Cached process > COUNT
[05/657447] Cached process > FIT
```

4. Give every input a new date without changing it. Still nothing runs.

```bash
touch data/earthquakes.csv params.yaml *.py
nextflow run main.nf -resume
```

```text
$ touch data/earthquakes.csv params.yaml *.py
$ nextflow run main.nf -resume
N E X T F L O W  ~  version 26.10.5
Launching `main.nf` [naughty_yalow] - revision: 8f977013ac
[d0/bc7982] Cached process > SUBSET
[25/4c00f0] Cached process > COUNT
[05/657447] Cached process > FIT
```

5. Add a comment to `count.py` and run with `-resume`. `COUNT` reruns, because its script changed. `SUBSET` doesn't, because nothing it reads changed. `FIT` doesn't either: the new `results/counts.csv` has the same content as the old one, and content is what the hash sees. Then put the script back.

```bash
echo '# An edit to the code.' >> count.py
nextflow run main.nf -resume
git checkout -- count.py
```

```text
$ echo '# An edit to the code.' >> count.py
$ nextflow run main.nf -resume
N E X T F L O W  ~  version 26.10.5
Launching `main.nf` [nasty_heisenberg] - revision: 8f977013ac
[d0/bc7982] Cached process > SUBSET
[dd/5226db] Submitted process > COUNT
[05/657447] Cached process > FIT
```

6. Add a process `COMPLETENESS` for the step the README skipped. It reads `data/earthquakes.csv`, `params.yaml` and `completeness.py`, and writes `completeness.md`. Call it in the `workflow` block with the same three `file(...)` arguments as `SUBSET`. Run with `-resume`, and read the table it writes. b rises while the catalog is incomplete, then levels off within its uncertainty. Pick the lowest start magnitude on the level part, as in the Snakemake exercise.

```bash
nextflow run main.nf -resume
cat completeness.md
```

```text
$ nextflow run main.nf -resume
N E X T F L O W  ~  version 26.10.5
Launching `main.nf` [lonely_magritte] - revision: d0d175c326
[d0/bc7982] Cached process > SUBSET
[25/4c00f0] Cached process > COUNT
[9e/7a1aaa] Submitted process > COMPLETENESS
[05/657447] Cached process > FIT
$ cat completeness.md
| start magnitude | earthquakes | b-value | uncertainty |
|---|---|---|---|
| 4.0 | 9496 | 0.74 | 0.01 |
| 4.1 | 9079 | 0.85 | 0.01 |
| 4.2 | 8428 | 0.98 | 0.01 |
| 4.3 | 7421 | 1.09 | 0.01 |
| 4.4 | 6213 | 1.19 | 0.02 |
| 4.5 | 4845 | 1.23 | 0.02 |
| 4.6 | 3583 | 1.21 | 0.02 |
| 4.7 | 2638 | 1.17 | 0.02 |
| 4.8 | 2100 | 1.23 | 0.03 |
| 4.9 | 1678 | 1.31 | 0.03 |
| 5.0 | 1221 | 1.30 | 0.04 |
| 5.1 | 859 | 1.22 | 0.04 |
| 5.2 | 625 | 1.17 | 0.05 |
| 5.3 | 462 | 1.13 | 0.05 |
| 5.4 | 350 | 1.12 | 0.06 |
| 5.5 | 265 | 1.09 | 0.07 |
```

7. Set `min_magnitude` in `params.yaml` to your choice, save, and run with `-resume`. Everything that reads `params.yaml` reruns. Commit, and in the message name the magnitude and what in the table supports it.

```bash
nextflow run main.nf -resume
cat metrics.json
git add main.nf params.yaml metrics.json completeness.md
git commit -m "REPLACE THIS with the start magnitude you chose, and what in the table supports it"
```

8. Delete every output, the cache and `work/`, and rebuild. `git status --short` should print nothing: the committed files came back byte for byte from the raw data.

```bash
rm -rf results work .nextflow .nextflow.log* metrics.json completeness.md
nextflow run main.nf
git status --short
```

```text
$ rm -rf results work .nextflow .nextflow.log* metrics.json completeness.md
$ nextflow run main.nf
N E X T F L O W  ~  version 26.10.5
Launching `main.nf` [drunk_magritte] - revision: d0d175c326
[8f/7c1ee6] Submitted process > SUBSET
[f1/a26a33] Submitted process > COMPLETENESS
[75/bef3e7] Submitted process > COUNT
[eb/619cf8] Submitted process > FIT
$ git status --short
```

## Check everything

- The full check. It clones your last commit, builds from the raw data, edits a script and changes a parameter under `-resume` and reads Nextflow's log to see what ran, checks your start magnitude and its commit message, then deletes every output and rebuilds.
- It knows the accepted start magnitudes only as salted digests, so reading `check.py` won't give you one.
- It works in a throwaway clone, so your project is safe. It takes about 20 seconds.

```bash
python ../check.py --nextflow
```

After step 1 only, it says this:

```text
$ python ../check.py --nextflow
PASS  The committed main.nf parses
PASS  nextflow builds metrics.json from the raw data in a clean clone
PASS  The committed metrics.json matches a clean build
PASS  An edited script reruns its task, and -resume takes the task before it from the cache
PASS  A changed parameter reruns every task that depends on it
FAIL  The committed min_magnitude is not a start magnitude this exercise accepts. Read the table from python completeness.py, and pick the lowest start magnitude at which b has stopped rising (step 2).
FAIL  completeness.md is not committed. Add a COMPLETENESS process that writes it, call it in the workflow block, build it and commit it (step 2).

5 of 7 parts pass.
```

- Two of the Snakemake exercise's checks pass here without extra work. In Nextflow the script has to be an input, or the task can't run it, so an edit to the code is always seen.

## Snakemake and Nextflow

| | Snakemake | Nextflow |
|---|---|---|
| The workflow file | `Snakefile`, Python with a rule syntax. Rules name input and output files, and Snakemake connects them by file name. | `main.nf`, a language built on Groovy, on the Java virtual machine. Processes name inputs and outputs, and you connect them in the `workflow` block. |
| Where a step runs | In the project folder. Outputs land where the rule says. | In its own folder under `work/`, with inputs staged as links. `publishDir` copies outputs back. |
| What's stale | A rule reruns when an input is newer than its output, or when its code, parameters, inputs or software environment are recorded as changed. `--rerun-triggers mtime` keeps only the dates. ([Snakemake command line](https://snakemake.readthedocs.io/en/stable/executing/cli.html)) | A task reruns when its hash isn't in the cache. The hash covers the inputs, the script and the parameters. By default a file hashes by name, size and date. With `cache = 'deep'` it hashes by content. Nothing is reused unless you pass `-resume`. ([Cache and resume](https://docs.seqera.io/nextflow/cache-and-resume)) |
| Dry run | `snakemake -n` lists what would run. | `nextflow run main.nf -preview` checks the script and the wiring without running tasks. Nothing says what `-resume` would reuse. |
| One task at a time | `--cores 1` | Not needed here. The config can set `executor.cpus`. |
| Where it's common | Research groups and bioinformatics, with Python-heavy code. Rules with wildcards run over many samples. | Bioinformatics and clinical pipelines, clusters and clouds. The [nf-core](https://nf-co.re/) community maintains pipelines in it, and a company, Seqera, maintains the tool. |
| Scaling up | Executors and profiles for cluster schedulers and clouds. | Executors for SLURM and other schedulers, Kubernetes and the cloud batch services, switched by a config profile. |
| Start-up | A Python process. | A Java virtual machine, about 3 seconds and 0.4 to 0.5 GB here before any work. |
| Learn more | [Snakemake documentation](https://snakemake.readthedocs.io/en/stable/) | [Nextflow documentation](https://docs.seqera.io/nextflow/), [Hello Nextflow](https://training.nextflow.io/latest/hello_nextflow/) |

- The idea doesn't change. Each step names what it reads and what it writes, the tool knows what's stale, and one command rebuilds everything from the raw data.
- The two tools differ on how they know. Snakemake reads file dates first and keeps records next to them. Nextflow hashes.
- Both are declarations. The README was a procedure, and the person running it was wrong.

## What we ran where

- Recorded November 8, 2026, with Nextflow 26.10.5, OpenJDK 25.0.2 and Python 3.12.16 from the environment file above.
- Each row is the whole page, run by a script: the starter and its failing checks, step 1 and its check, step 2 and the final check. Peak memory is the largest resident set of any process in the run, which is the Java virtual machine.

| Machine | Starter fails | Solution passes | Whole page | Peak memory | First run downloaded |
|---|---|---|---|---|---|
| aarch64, Linux, DGX Spark | Yes, 0 of 1 and 0 of 3 | Yes, 3 of 3 and 8 of 8 | 60 s | 0.48 GB | Nothing |
| x86_64, WSL2 on Windows, Ubuntu 24.04 | Yes, 0 of 1 and 0 of 3 | Yes, 3 of 3 and 8 of 8 | 64 s | 0.49 GB | Nothing. A run with the network off succeeded. |
| arm64, macOS 27.0.1 | Yes, 0 of 1 and 0 of 3 | Yes, 3 of 3 and 8 of 8 | 60 s | 0.38 GB | Nothing |

- When you're done, `conda env remove --yes --name repro-nextflow` gets the disk back.
