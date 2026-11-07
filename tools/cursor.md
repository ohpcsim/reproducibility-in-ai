---
title: Cursor
---

- Cursor's command-line agent.
- Recorded with version 2026.09.18-9a7762b and its default model setting, `Auto`.
- The tool reports only `Auto`, so we can't tell you which model wrote this card.
- That goes in the manifest under `not_exposed`.

## Install and sign in

- This is the install command from [Cursor's CLI docs](https://cursor.com/docs/cli/installation), checked November 7, 2026.
- We recorded with a copy that was already installed, so we didn't run these lines for the recording.

```bash
curl https://cursor.com/install -fsS | bash
cursor-agent login
```

- You need a Cursor account.

## The same task

Get the folder by doing [exercise 4](../exercises/04-llm/llm.ipynb)'s setup, then copy the frozen files somewhere empty, along with the prompt:

```bash
mkdir ~/model-card
cd ~/model-card
cp ~/llm/project/{README.md,params.yaml,dvc.yaml,dvc.lock,metrics.json,splits.json,split.py,train.py,score.py,artifacts.yaml,release.yaml,sources.yaml} .
cp ~/llm/project/runs/recorded-prompt.md prompt.md
```

## The exact command

- We ran this once on November 7, 2026, in an empty folder holding only the frozen exercise 3 files and the prompt, with a fresh home folder, so no settings, memory or instructions from our machine could load.
- Your own settings, rules and memory may change what you get.
- Run it in an empty folder if you want a comparable result.

```bash
cursor-agent -p --force --trust --output-format stream-json "$(cat prompt.md)" > transcript.jsonl
```

- For the recording we saved standard output to a raw log, which is what `> transcript.jsonl` stands for here.
- `--force` lets it run commands and write files without asking, so use it only in a folder you can throw away.
- `--trust` skips the question about trusting the folder.

## What it wrote

- This is the file as the tool wrote it, not edited.

:::{dropdown} card.md
```{literalinclude} ../exercises/04-llm/.exercise/project/runs/cursor/card.md
:language: markdown
```
:::

:::{dropdown} The transcript, trimmed to the task
```{literalinclude} ../exercises/04-llm/.exercise/project/runs/cursor/transcript.md
:language: text
```
:::

## Test it

- Back in your exercise 4 project, run your tests on the card.
- Our verdict below comes from our copy of the same rules.
- We don't publish that copy, because writing the tests is the exercise.

```bash
CARD=~/model-card/card.md python -m pytest -q tests
```

Here's what our tests decided about this recording:

```{literalinclude} ../exercises/04-llm/.exercise/project/runs/cursor/verdict.txt
```

- The rule rejected this card for a harmless reason: it writes the accuracy's range as `[0, 1]`, and 1 isn't in the evidence.
- A person has to decide whether that rule is right.
- Claude Code's card was rejected for the same reason.

## Fill in the manifest

- Record the tool and its version, the model and any revision, the date, the settings, the prompt, the acceptance result, who decided, and what isn't exposed to you.
- With `Auto`, the model isn't exposed, so say that.
- Passing `--model` gives you a name you can record.

Here's the one for this run:

```{literalinclude} ../exercises/04-llm/.exercise/project/runs/cursor/manifest.yaml
:language: yaml
```
