---
title: The premise
---

## Problem statement

- Reproducibility is a core tenet of science.
- 99+% of papers that involve computation are by definition not reproducible. Is that really science?
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
- If the code breaks, the document breaks.
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

- Components don't keep data between requests.
- State lives outside them, in databases or object storage.
- Any instance can handle any request.
- This makes scaling and recovery easy.

**The history of \*Ops**

- \*Ops, or "splat ops", applies ideas from DevOps to everything else.
- DevOps treats operations as a software development project.
- DataOps: data has versions, and pipelines are declared steps. [Exercise 2](exercises/02-dataops/dataops.ipynb).
- GitOps: the declared state lives in Git, and automation makes the system match it. [Exercise 1](exercises/01-gitops/gitops.ipynb).
- Towards MLOps and LLMOps, when coupled with automation (CI/CD): models and prompts are versioned, tested and released like software. [Exercises 3](exercises/03-registry/registry.ipynb) [and 4](exercises/04-llm/llm.ipynb).

Timeline:

1. 2009, DevOps: the first DevOpsDays, in Ghent, organized by Patrick Debois.
2. 2014, DataOps: the term is credited to Lenny Liebmann, and Andy Palmer popularized it in 2015.
3. 2017, GitOps: Weaveworks, "Operations by Pull Request".
4. Today, MLOps and LLMOps: the same ideas for models and prompts. There's no single origin year. An early paper on the problem is Sculley et al., ["Hidden Technical Debt in Machine Learning Systems"](https://research.google/pubs/hidden-technical-debt-in-machine-learning-systems/), NeurIPS 2015.

## Pets vs cattle

**Traditional HPC, the "pets" approach**

- Each server or node has its own identity and configuration.
- People build each one by hand, maintain it carefully and give it a name.
- When something breaks, you diagnose it, repair it and nurse it back to health.
- You SSH into specific nodes and hand-tune environments.

**Cloud-native, the "cattle" approach**

- Servers have numbers, not names.
- Automation configures them identically.
- When something breaks, you terminate it and replace it.
- Any node can run any workload.

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
- Practical steps:
  1. Define environments declaratively, in `environment.yml` or a `Dockerfile`.
  2. Store the definitions in Git.
  3. Build and rebuild environments on demand.
  4. Test on more than one system.
- The goal is to move from "this node is special" to "this definition is reproducible".
- The document and the data are the pets. Everything that runs them is cattle.

## Thesis

- Interactive HPC workloads are inherently stateful.
- Capturing the state of an HPC system is almost impossible.
- Cloud-native methods help you express your full computational environment.
- Declarative approaches are more portable and less fragile than procedural ones.
- Treating every system as stateless makes it portable in its software, OS and libraries, and in its data.
- Managing software interactively, with conda or pip, probably isn't enough. Use declarative, reproducible definitions.
- Leaving data on a POSIX file system probably isn't enough for AI workloads. Use GitOps and DataOps.
- Leaving your method in a chat session probably isn't enough. Keep it in the project, harness and model agnostic.

## From the ideas to the exercises

- An environment file and its lock: [exercise 1, GitOps](exercises/01-gitops/gitops.ipynb).
- Pointers to the data in Git, and the data in object storage: [exercise 2, DataOps](exercises/02-dataops/dataops.ipynb).
- A model registry: [exercise 3, model registry](exercises/03-registry/registry.ipynb).
- The method stays in the project, not in the chat: [exercise 4, LLM documentation](exercises/04-llm/llm.ipynb).

## Further reading

- [The History of Pets vs Cattle and How to Use the Analogy Properly](https://cloudscaling.com/blog/cloud-computing/the-history-of-pets-vs-cattle/), Randy Bias, 2016. Where the analogy came from. He credits Bill Baker's talk on scaling SQL Server.
- [CERN Data Centre Evolution](https://www.slideshare.net/gmccance/cern-data-centre-evolution), Gavin McCance, SDCD12 in Bern, November 2012. Slides on moving CERN's data centre to a pets and cattle service model.
- [Literate Programming](https://doi.org/10.1093/comjnl/27.2.97), D. E. Knuth, The Computer Journal 27(2):97-111, 1984. The paper that introduced literate programming.
