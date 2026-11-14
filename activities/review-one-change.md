---
title: Review one change
---

Allow 45 to 60 minutes once a reviewer is available. This activity practises [Review every change](../start-here.md#review-every-change) and [Keep state out of the chat](../start-here.md#keep-state-out-of-the-chat).

## What you need

- A repository of your own and the coding agent you have.
- Your [five known-answer tests](five-tests.md), their recorded results and a small change to propose.
- A reviewer: a person, a second model, or a new session of the same model. Record which one reviewed it.

If you have no pull request host, use a local branch. Give the reviewer the output of `git diff main...<branch>`, using your default branch's name if it is not `main`, and record the branch and commit instead of a URL. If no person or model can review the change, stop here.

## The problem

An agent can miss a defect in its own change. Ask someone else to inspect the change and its evidence before you decide whether to merge it.

## Step 1: propose one change on a branch

Spend about twenty minutes on this step.

1. Check the repository's working files. Preserve any work from other tasks.
2. Ask your agent to create a new branch with an unused name.
3. Ask it for one small change, such as fixing a calculation. Have it follow `AGENTS.md`.
4. Inspect the diff. Check that the branch contains the task's changes and no credentials or private data.
5. Commit the change and record its commit identifier.
6. Send the same five requests to fresh sessions on that commit, and save the outputs beside the earlier result. If the change makes an expected answer out of date, write a new version of the tests as [the tests activity](five-tests.md) describes, keep the old result, and run the new version.
7. Commit the results. If you have a Git host, push the branch and open a pull request. Name the change, the tests and the result in its description.

## Step 2: ask for review

Spend about fifteen minutes on this step. Give the reviewer the pull request or the diff, the five tests and both sets of results. Include the input files needed to check them, within your project's data rules.

Ask the reviewer:

```text
Read the proposed change, the five known-answer tests and the before and after results. Check the expected answers against their sources. Check whether the change meets each test and breaks any project rule. Name each defect with its file and the evidence. State whether you recommend accepting the change or requesting changes. Do not edit or merge it.
```

Read the findings. If you make a correction, rerun the tests and have the reviewer check the corrected diff.

## Step 3: record your decision

Spend about five minutes on this step. Write `review-decision.md` in the project.

Record the pull request URL, or the branch name, and the reviewed commit identifier. Name the reviewer, the review date, the test results and any unresolved findings. If a model reviewed it, record its name and version, or say that the provider did not expose the version.

State your decision in a sentence. You can accept the change, request changes or reject it. Give the reason and the next action. Commit this note to the branch.

## Check your work

Use the last five minutes to read the diff and the decision file without the chat. You are done when the reviewer has checked the change against all five tests and your decision file identifies the version they reviewed. A decision to request changes or reject the change completes this activity.

Merge an accepted change through your project's usual process when its required checks and reviews pass.

## What this does not prove

A second reviewer can miss the same defect. The decision file records what you decided and why.

Return to [the seven principles](../start-here.md).
