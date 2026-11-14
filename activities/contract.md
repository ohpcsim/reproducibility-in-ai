---
title: Write a contract file
---

Allow about 30 minutes. This activity practises [Declare it](../start-here.md#declare-it).

## What you need

- One repository of your own, a text editor and your existing coding agent.
- A small task, such as correcting one report's calculation.
- An agent that can read the project folder.

## What you make

Three task rules in `AGENTS.md` at the project root, which a fresh session reads.

## Step 1: name the task and its limits

Spend about five minutes on this step.

1. Write the task in one sentence at the top of `AGENTS.md`.
2. Name the files the agent may edit for this task. Include the files the next two activities create: `known-answer-tests.md`, `known-answer-results.md` and `review-decision.md`.
3. Choose one quantity the agent must compute with a script.
4. Name an action the agent must never take, such as editing original data or sending files outside the project.

## Step 2: write the contract

Spend about ten minutes on this step. If `AGENTS.md` exists, read it and add task rules that agree with it. Keep its other rules.

Write three rules like these, with your own paths and calculation. This example assumes a Python project with a report script.

```text
# Rules for this task

1. You may edit report.py, notes/calculation.md, known-answer-tests.md, known-answer-results.md and review-decision.md for this task.
2. You must compute every reported mean with a script and save the command and its output in notes/calculation.md.
3. You must never edit files under data/original/ or send project files to another service.
```

Use paths that exist in your project. Create the notes file if the task needs it. Keep credentials out of the contract.

## Step 3: check in a fresh session

Spend about ten minutes on this step. Start a new agent session in the project, without the earlier chat history.

Ask it:

```text
Read the root AGENTS.md. Do not edit files or run the task. State the three task rules, including the allowed paths, the required script calculation and the forbidden actions. Name the file you read.
```

Compare its answer with the file. If it misses a rule, revise the wording and repeat the check in another fresh session. If your agent does not load `AGENTS.md` on startup, keep the explicit read request.

Some agents also load instruction files from parent folders or your home folder. Note any rule it states that is not in `AGENTS.md`.

## Check your work

Use the last five minutes to save the session's answer and the date in `notes/contract-check.md`. You are done when a fresh session names `AGENTS.md` and states all three rules without changing their meaning.

## What this does not prove

It does not show that the agent will obey the rules during work. A contract file does not set tool permissions, so keep your agent's existing permission controls and review its edits.

Next, [write five known-answer tests](five-tests.md) for the task.
