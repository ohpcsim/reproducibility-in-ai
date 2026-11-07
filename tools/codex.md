---
title: Codex
---

Codex is OpenAI's coding tool for the terminal. Recorded with version 0.165.0 and its default model for this account, `gpt-6.1-sol`. We read the model name from the session log in Codex's home folder, because the command's output doesn't include it.

## Install and sign in

This install command is in the README of [OpenAI's Codex repository](https://github.com/openai/codex), checked November 7, 2026. That page also lists other ways to install it. We recorded with a copy that was already installed, so we didn't run these lines for the recording.

```bash
npm install -g @openai/codex
codex login
```

Sign in with a ChatGPT plan or an API key.

## The same task

Get the folder by doing [exercise 4](../exercises/04-llm/llm.ipynb)'s setup, then copy the frozen files somewhere empty, along with the prompt:

```bash
mkdir ~/model-card
cd ~/model-card
cp ~/llm/project/{README.md,params.yaml,dvc.yaml,dvc.lock,metrics.json,splits.json,split.py,train.py,score.py,artifacts.yaml,release.yaml,sources.yaml} .
cp ~/llm/project/runs/recorded-prompt.md prompt.md
```

## The exact command

We ran this once on November 7, 2026, in an empty folder holding only the frozen exercise 3 files and the prompt, with a fresh home folder, so no settings, memory or instructions from our machine could load. Your own settings, rules and memory may change what you get. Run it in an empty folder if you want a comparable result.

```bash
codex exec --skip-git-repo-check --sandbox workspace-write --json "$(cat prompt.md)" > transcript.jsonl
```

For the recording we saved standard output to a raw log, which is what `> transcript.jsonl` stands for here. `--skip-git-repo-check` is needed because the folder isn't a Git repository.

## What it wrote

This is the file as the tool wrote it, not edited.

:::{dropdown} card.md
```{literalinclude} ../exercises/04-llm/.exercise/project/runs/codex/card.md
:language: markdown
```
:::

:::{dropdown} The transcript, trimmed to the task
```{literalinclude} ../exercises/04-llm/.exercise/project/runs/codex/transcript.md
:language: text
```
:::

## Test it

Back in your exercise 4 project, run your tests on the card. Our verdict below comes from our copy of the same rules. We don't publish that copy, because writing the tests is the exercise.

```bash
CARD=~/model-card/card.md python -m pytest -q tests
```

Here's what our tests decided about this recording:

```{literalinclude} ../exercises/04-llm/.exercise/project/runs/codex/verdict.txt
```

This card is also Model A in exercise 4's step 3. In a second turn it was given two decisions in chat, with `codex exec resume --last --skip-git-repo-check -c sandbox_mode=workspace-write --json "<the message>"`. That card, in `runs/model-a-codex-chat`, passes the decision tests, and this one can't.

## Fill in the manifest

Record the tool and its version, the model and any revision, the date, the settings, the prompt, the acceptance result, who decided, and what isn't exposed to you. Your default model may be different, so record the one you got. Here's the one for this run:

```{literalinclude} ../exercises/04-llm/.exercise/project/runs/codex/manifest.yaml
:language: yaml
```
