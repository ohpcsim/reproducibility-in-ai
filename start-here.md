---
title: Start here with LLM work
---

Seven principles for research with a coding agent, and three activities to try them in your own repository.

## The example study

The examples on this page link to a public study, [Tuning a small model to call tools](https://ohpcsim.github.io/tool-call-tuning/). It tuned a small open model to turn requests into calls to a to-do tool. Its site publishes the pipeline's declarations and aggregate results. It does not publish the data, the models, the answer keys, the training and scoring code or the review reports, so you cannot rerun the study from the site. Every reported result is open validation, which means the people and agents building the system could see those cases while they worked. No tuned model met the study's selection rule.

The exercises are the four hands-on exercises on this site. They use a small penguin data project.

## Seven principles

### Declare it

Write the agent's rules in a project file. Name what it may change, what a script must compute and what it must never do.

- In software: source code under version control.
- Tools: `AGENTS.md`, Git and your coding agent.
- Exercise: [2, Workflows](exercises/02-workflows/workflows-linux.ipynb) teaches declarations for analysis steps.
- Activity: [Write a contract file](activities/contract.md).
- In the study: [`pipeline/dvc.yaml`](https://ohpcsim.github.io/tool-call-tuning/project#the-declarations) declares each step's command, inputs and outputs.

### Pin what you depend on

Record the versions of your software, data and model. For a hosted model, record its name and the date you used it. Write down what you cannot pin, such as changes the provider makes.

- In software: a dependency lock file.
- Tools: conda or uv lock files, DVC for data versions, and a model revision when you have one.
- Exercises: [1, Software environments](exercises/01-environments/environments-linux.ipynb) teaches environment locks. [3, Versioning data](exercises/03-dataops/dataops-linux.ipynb) teaches data versions.
- In the study: [`pipeline/params.yaml` and `pipeline/dvc.lock`](https://ohpcsim.github.io/tool-call-tuning/project#the-declarations) record a base-model revision and input hashes.

### Write the test first

Write requests, right answers and a pass rule before you compare models. Do not change the pass rule after you see the outputs.

- In software: a test suite with known answers.
- Tools: a text file for the cases and a script for calculations and comparisons.
- Activity: [Write five known-answer tests](activities/five-tests.md).
- In the study: [`pipeline/src/todo/select.py`](https://ohpcsim.github.io/tool-call-tuning/project#the-selection-stage) checks the declared candidate list and calls the selection rule.

### Review every change

Ask another model or a person to check a proposed change against the tests. Record the findings and your decision before you merge it.

- In software: code review on a pull request.
- Tools: Git branches, a second reviewer, and pull requests if your repository has a Git host.
- Activity: [Review one change](activities/review-one-change.md).
- In the study: [`gate.md`](https://ohpcsim.github.io/tool-call-tuning/gate#the-reviewed-implementation) describes six review rounds for the implementation of an added check. That implementation has not been merged.

### Release what you cite

Give a saved version a release name and cite that version. Check that another person can retrieve the files the result needs.

- In software: a versioned library release.
- Tools: Git tags, DVC for stored data and models, and GTO, which keeps a list of model versions as Git tags.
- Exercise: [4, Model registry](exercises/04-registry/registry-linux.ipynb) teaches registration and restoration. It uses local storage, so you need no storage account.
- In the study: [`pipeline/registry/versions.txt`](https://ohpcsim.github.io/tool-call-tuning/project#what-the-registry-versions) lists the version tags. All 12 registered versions are still at the `experiment` stage.

### Build the document from the work

Have the document build compute its tables and figures from saved inputs. Make a failing calculation stop the build.

- In software: a build with checks.
- Tools: Jupyter Book, executable notebooks and the project's scripts.
- Exercise: [2, Workflows](exercises/02-workflows/workflows-linux.ipynb) teaches a declared figure-building step. This site's [results example](results/results.ipynb) and [build instructions](build.md) show a document build.
- No activity yet.
- In the study: [`results.md`](https://ohpcsim.github.io/tool-call-tuning/results) computes its tables and a figure from public aggregate files. [`build_site.sh` and `check_site.py`](https://ohpcsim.github.io/tool-call-tuning/build) build and check the pages.

### Keep state out of the chat

Save decisions, results and unfinished work in project files that a fresh session can read.

- In software: a job that reads its inputs from files and writes its outputs to files.
- Tools: Markdown decision records and Git.
- Activity: [Review one change](activities/review-one-change.md) ends with a decision file.
- In the study: [`premise.md`](https://ohpcsim.github.io/tool-call-tuning/premise#pets-vs-cattle) names chat state as an open problem. [`sealed-test.md`](https://ohpcsim.github.io/tool-call-tuning/sealed-test) records the loss of the study's sealed test before use. A sealed test is a set of cases that nobody tuning the system sees until one final check.

## Three activities

Do them in order, in one repository of your own, with the coding agent you have. The first takes about 30 minutes. Allow 45 to 60 minutes for each of the other two. You download no code and need no special hardware.

1. [Write a contract file](activities/contract.md).
2. [Write five known-answer tests](activities/five-tests.md).
3. [Review one change](activities/review-one-change.md).

The exercises install their own tools. Their links on this page open the Linux copies. [Pick your machine](index.md#pick-your-machine) for the Mac, Windows or HPC copy of an exercise, or for Binder, which runs it in your browser.

## Next workshops

PEARC27 and SC27, in 2027: test-driven development and test-driven documentation.
