---
title: The premise
---

## Problem statement

- Reproducibility is a core tenet of science.
- Most published computational results can't be rerun from what's published. Is that really science?
- Of 204 Science papers sampled, artifacts were obtained for 44% and results reproduced for 26% ([Stodden, Seiler and Ma, PNAS 2018](https://doi.org/10.1073/pnas.1708290115)).
- Reproducibility involves software, data and workflows.
- LLMs add more reproducibility challenges.

## AI workflows

An AI result depends on:

- Software you develop. It should be version controlled with Git.
- Software you consume.
- Workflows you develop.
- Data you acquire, consume or both.
- LLMs you use.
- Conclusions you draw from all of the above.

## Literate programming to literate science

**Literate programming**

- Donald Knuth developed literate programming in 1984, while he was writing TeX.
- A program is one document, for people and for the machine.
- Weave makes the document readable. Tangle makes it run.
- Knuth wrote: "Instead of imagining that our main task is to instruct a computer what to do, let us concentrate rather on explaining to human beings what we want a computer to do."

**Literate science**

- Literate science applies the same idea to the whole result, and not only to the program.
- The claims, the code, the environment and the data live in one project.
- Published results come from running the project, not from pasted output.
- If the code breaks, the build breaks.
- Earlier work: Claerbout and Karrenbach (1992) on reproducible electronic documents, and Buckheit and Donoho (1995) on WaveLab.
- The step this workshop adds is doing it with cloud-native tools, which are stateless and declarative.

## Cloud-native and the history of \*Ops

- Cloud-native applications are designed to run in dynamic, distributed environments.
- They rely on automation, they scale, and they recover from failures.
- Cloud-native is an architectural approach. It means more than running in the cloud.

**Declarative**

- You specify what you want, not how to get it.
- The system works out the steps to reach that state.
- Examples are Docker Compose, Kubernetes manifests and conda's `environment.yml`.

**Stateless**

- A job keeps nothing on the node between runs.
- Inputs and results live in Git and object storage.
- Any node can rerun any job.

**The history of \*Ops**

- \*Ops, or "splat ops", applies ideas from DevOps to everything else.
- DevOps treats operations as a software development project.
- DataOps: data has versions, and pipelines are declared steps. [Exercise 3](exercises/03-dataops/dataops.ipynb).
- Workflows: each analysis step declares what it reads and writes, so a tool reruns only what changed. [Exercise 2](exercises/02-workflows/workflows.ipynb).
- GitOps: the declared state lives in Git, and automation makes the system match it. [Exercise 1](exercises/01-environments/environments.ipynb) puts the declared environment in Git.
- MLOps and LLMOps: models and prompts are versioned, tested and released like software. [Exercise 4](exercises/04-registry/registry.ipynb) does it for a model.

Timeline:

1. 2009, DevOps: the first DevOpsDays, in Ghent, organized by Patrick Debois.
2. 2014, DataOps: the term is credited to Lenny Liebmann, and Andy Palmer popularized it in 2015.
3. 2017, GitOps: Weaveworks, "Operations by Pull Request".
4. Today, MLOps and LLMOps: the same ideas for models and prompts. There's no single origin year. An early paper on the problem is Sculley et al., ["Hidden Technical Debt in Machine Learning Systems"](https://research.google/pubs/hidden-technical-debt-in-machine-learning-systems/), NeurIPS 2015.

## Pets vs cattle

**The "pets" approach: a hand-built environment**

- Custom builds that "just work" on one system.
- SSH into specific nodes and hand-tune environments.
- Fear of losing a carefully curated environment.
- When something breaks, you diagnose it, repair it and nurse it back to health.

**Cloud-native, the "cattle" approach**

- Servers have numbers, not names.
- Automation configures them identically.
- When something breaks, you terminate it and replace it.
- Any compatible node can run the workload.

**Why this matters for academic HPC**

Today:

- Long-running simulations run on specific nodes.
- Custom software builds "just work" on one system.
- People fear losing carefully curated environments.
- "It works on my machine."

The goal:

- Environments are defined in code and rebuild the same way.
- They're portable across a laptop, an HPC system and the cloud.
- Failures show up early, and recovery is quick.
- Collaborators share the same definitions.

**You don't have to choose one or the other**

- Computational infrastructure is cattle. You can throw it away and replace it.
- Your data and results are pets. Preserve them carefully.
- Software environments are declarative definitions under version control.
- Your research products (papers, code, data) are the pets. Everything that runs them is cattle.

## Thesis

"Bringing cloud-native, declarative, and stateless concepts to batch HPC workloads solves most problems."

- Interactive HPC workloads are stateful.
- You can't capture the state of an HPC system.
- Cloud-native tools declare the full computational environment.
- Declarative beats procedural: more portable, less fragile.
- Stateless systems make software, OS, libraries and data portable.
- Interactive conda or pip installs aren't reproducible. Declare and lock them.
- Data left on a POSIX file system doesn't capture its history or provenance. Version it, with GitOps and DataOps.
- Work done in an LLM chat isn't reproducible. Keep the prompts and decisions in the project.

## From the ideas to the exercises

- An environment file and its lock: [exercise 1, Software environments](exercises/01-environments/environments.ipynb).
- Declared steps: [exercise 2, Workflows](exercises/02-workflows/workflows.ipynb).
- Pointers to the data in Git, and the data in object storage: [exercise 3, Versioning data](exercises/03-dataops/dataops.ipynb).
- A model registry: [exercise 4, model registry](exercises/04-registry/registry.ipynb).

## Further reading

- [The History of Pets vs Cattle and How to Use the Analogy Properly](https://cloudscaling.com/blog/cloud-computing/the-history-of-pets-vs-cattle/), Randy Bias, 2016. Where the analogy came from. He credits Bill Baker's talk on scaling SQL Server.
- [CERN Data Centre Evolution](https://www.slideshare.net/gmccance/cern-data-centre-evolution), Gavin McCance, SDCD12 in Bern, November 2012. Slides on moving CERN's data centre to a pets and cattle service model.
- [Literate Programming](https://doi.org/10.1093/comjnl/27.2.97), D. E. Knuth, The Computer Journal 27(2):97-111, 1984. The paper that introduced literate programming.
