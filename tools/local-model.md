---
title: A local model
---

- A model running on your own machine sends nothing to anyone, and you can record exactly which file it was.
- Recorded with Ollama 0.9.6 from conda-forge, using its CPU build, and the model `qwen2.5-coder:7b`, a 4.7 GB download under the Apache 2.0 license.
- We ran it on a 64-bit ARM Linux machine, on the CPU, and the run took under two minutes, including the download.

## Install and sign in

- You don't need an account.

This is how we installed it, in a throwaway conda environment:

```bash
conda create --yes --name ollama-test --channel conda-forge "ollama=0.9.6=cpu*"
conda activate ollama-test
ollama serve &
ollama pull qwen2.5-coder:7b
```

- For the recording we also used a private folder for the environment, a private home folder and a private port.
- When you're done, stop the server, and remove the environment and `~/.ollama`.

## The same task

Get the folder by doing [exercise 5](../exercises/05-llm/llm.ipynb)'s setup, then copy the frozen files somewhere empty, along with the prompt:

```bash
mkdir ~/model-card
cd ~/model-card
cp ~/llm/project/{README.md,params.yaml,dvc.yaml,dvc.lock,metrics.json,splits.json,split.py,train.py,score.py,artifacts.yaml,release.yaml,sources.yaml} .
cp ~/llm/project/runs/recorded-prompt.md prompt.md
```

## The exact command

- We ran this once on November 7, 2026, in an empty folder holding only the frozen exercise 4 files and the prompt, with a fresh home folder, so no settings, memory or instructions from our machine could load.
- Your own settings, rules and memory may change what you get.
- Run it in an empty folder if you want a comparable result.

```bash
{ cat prompt.md; for f in release.yaml metrics.json params.yaml sources.yaml artifacts.yaml README.md; do printf '\n--- %s ---\n' "$f"; cat "$f"; done; } | ollama run qwen2.5-coder:7b > card.md
```

- This tool can't open files itself, so the command hands it the prompt and six files as text.

## What it wrote

- This is the file as the tool wrote it, not edited.

:::{dropdown} card.md
```{literalinclude} ../exercises/05-llm/.exercise/project/runs/local-model/card.md
:language: markdown
```
:::

:::{dropdown} The transcript, trimmed to the task
```{literalinclude} ../exercises/05-llm/.exercise/project/runs/local-model/transcript.md
:language: text
```
:::

## Test it

- Back in your exercise 5 project, run your tests on the card.
- Our verdict below comes from our copy of the same rules.
- We don't publish that copy, because writing the tests is the exercise.

```bash
CARD=~/model-card/card.md python -m pytest -q tests
```

Here's what our tests decided about this recording:

```{literalinclude} ../exercises/05-llm/.exercise/project/runs/local-model/verdict.txt
```

- The rules accept this card.
- Read it anyway.
- It says the model is intended for "educational and research settings", and no file in the folder says that.
- Our tests didn't catch that, so a person has to.
- That's a reason to write another test.

## Fill in the manifest

- Record the tool and its version, the model and any revision, the date, the settings, the prompt, the acceptance result, who decided, and what isn't exposed to you.
- You can record the model's exact digest here, which the hosted tools don't give you.

Here's the one for this run:

```{literalinclude} ../exercises/05-llm/.exercise/project/runs/local-model/manifest.yaml
:language: yaml
```
