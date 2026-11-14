---
title: Write five known-answer tests
---

Allow 45 to 60 minutes. This activity practises [Write the test first](../start-here.md#write-the-test-first).

## What you need

- A repository of your own, a text editor and your existing coding agent.
- A small task with answers you can check from your files or compute with a script.
- Five requests from your own work and the inputs each request needs.

## The problem

If you choose the pass rule after you see the agent's answers, you can change the rule to fit the result.

## Step 1: write the five cases

Spend about twenty minutes on this step. Create `known-answer-tests.md` in your project. Write five requests in it, each with its inputs and right answer.

1. Choose four requests the agent should answer or complete. Use requests whose right answers come from your data or from your scripts' output. A test of the code's current behaviour stops being right when you fix the code.
2. Choose one request it should refuse under your project rules. Use a made-up example that requires no real forbidden action.
3. Check each right answer against its source. Compute numerical answers with a script, and save the command and output in `known-answer-tests.md` above the cases.
4. Write the comparison rule for each answer. Name any rounding, numerical tolerance or allowed variation.

Use this structure for each case, and replace the instructions with your own text.

```text
## Case 1

Write the request here.
List the input files or paste the small input here.
Write the right answer here.
Name the source or calculation that supports that answer.
State how you will compare an observed answer with this answer.
```

For the refusal case, say what the agent must decline and what it must leave unchanged.

## Step 2: write the pass rule

Spend about five minutes on this step. Add this rule to the file:

```text
The run passes if all five answers meet their written comparison rules and the agent takes no forbidden action. A refusal passes only if the agent declines the request and leaves the protected files unchanged.
```

Commit the file before the run. The commit shows that the tests came first, and later corrections show up as new commits.

## Step 3: run the five requests

Spend about twenty minutes on this step.

1. Choose a model available in your existing agent.
2. Send each request to its own fresh session with the same setup: the project rules and the inputs. Your agent can read the project, so tell it which files it may read, and check its log for any read of `known-answer-tests.md`. For a stricter run, move the tests file out of the project during the run.
3. Use read-only or proposal mode. For a request to change a file, ask for the proposed edit, not an applied edit. Test no forbidden action against real data or a live service.
4. Send the requests without hints about the expected answers, and save every output.
5. In `known-answer-results.md`, record the model name, version and date. Record the agent name, settings and input files. If the provider does not expose a version, write that it does not expose one. Do not guess.
6. Compare each output with its rule. Record each pass or failure and the total out of five.

## Check your work

Use the last five minutes to check that the tests file's commit predates the run. Check that the results file names every case and quotes or links its observed output. You are done when both files exist and you have recorded the outcome, even if the run fails.

If you correct a wrong expected answer, record why. Give the corrected tests a new version, commit it and rerun. Keep the earlier result.

## What this does not prove

Five cases that you and the agent can both read show how the agent did on these five requests and nothing more.

Next, [review one change](review-one-change.md) against these five tests.
