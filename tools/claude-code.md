---
title: Claude Code
---

- Claude Code is Anthropic's coding tool for the terminal.
- Recorded with version 2.1.317 and the model `claude-haiku-5-5`, chosen with `--model haiku`.

## Install and sign in

- On macOS, Linux or WSL, this is the install command from [Anthropic's quickstart](https://code.claude.com/docs/en/quickstart), checked November 7, 2026.
- We recorded with a copy that was already installed, so we didn't run this line for the recording.

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

- Run `claude`, and sign in when it asks.
- You need a Claude subscription or an Anthropic Console account.

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
claude -p "$(cat prompt.md)" --model haiku --allowedTools "Read,Glob,Grep,Write" --output-format stream-json --verbose > transcript.jsonl
```

- For the recording we saved standard output to a raw log, which is what `> transcript.jsonl` stands for here.
- `--allowedTools` lets it read and write without asking.
- It also ran read-only shell commands such as `find`, which the tool allows by default.

## What it wrote

- This is the file as the tool wrote it, not edited.

:::{dropdown} card.md
```{literalinclude} ../exercises/04-llm/.exercise/project/runs/claude-code/card.md
:language: markdown
```
:::

:::{dropdown} The transcript, trimmed to the task
```{literalinclude} ../exercises/04-llm/.exercise/project/runs/claude-code/transcript.md
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

```{literalinclude} ../exercises/04-llm/.exercise/project/runs/claude-code/verdict.txt
```

- It's a good card, and the rule rejected it for a harmless reason: it describes accuracy as a fraction "from 0 to 1", and 1 isn't in the evidence.
- Cursor's card was rejected for the same reason.
- A person has to decide whether that rule is right.
- That's what a test failure is for, so write down what you decide.

## Fill in the manifest

- Record the tool and its version, the model and any revision, the date, the settings, the prompt, the acceptance result, who decided, and what isn't exposed to you.
- Claude Code reports the model name, and doesn't report the sampling settings.

Here's the one for this run:

```{literalinclude} ../exercises/04-llm/.exercise/project/runs/claude-code/manifest.yaml
:language: yaml
```
