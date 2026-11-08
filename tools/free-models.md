---
title: Free models
---

- Free models let you try this with no paid plan.
- **They may use what you send them for training, so use them only for public or synthetic work.** Never send them anything confidential, unpublished or about a person.

- We ran one free model through OpenCode.
- We didn't run OpenRouter, and it's described below from its documentation.

## OpenCode, as we ran it

- Recorded with OpenCode 2.1.4 and the free model `opencode/deepseek-v4.1-flash-free`.
- It needed no account and no key.

What [OpenCode's Zen documentation](https://opencode.ai/docs/zen/) said when we checked it on November 7, 2026:

- Free models are free for a limited time, and the list changes.
- The model we ran is listed as zero-retention, and as not using your data for training.
- Others are not. For example, it says Big Pickle may use collected data to improve the model, Iceman Free retains data and uses it to improve the model, and Inkling 2 Small Free retains data and may use it for model training. The NVIDIA free endpoints are for trial use, with no personal or confidential data.
- Some aren't available in every country.

- So check the current page for the model you pick, and don't assume that one free model's terms apply to another.

## Install and sign in

- This is the install command from [OpenCode's documentation](https://opencode.ai/docs/).
- We recorded with a copy that was already installed, so we didn't run this line for the recording.

```bash
curl -fsSL https://opencode.ai/install | bash
```

- Sign-in isn't needed for the free models.
- List them with `opencode models`.

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
opencode run --standalone --auto --model opencode/deepseek-v4.1-flash-free --format json "$(cat prompt.md)" > transcript.jsonl
```

- For the recording we saved standard output to a raw log, which is what `> transcript.jsonl` stands for here.
- We used `--standalone` so that it ran its own server, separate from anything else on our machine.
- You shouldn't need that flag.
- `--auto` approves its actions without asking, so use it only in a folder you can throw away.

## What it wrote

- This is the file as the tool wrote it, not edited.

:::{dropdown} card.md
```{literalinclude} ../exercises/05-llm/.exercise/project/runs/opencode-free/card.md
:language: markdown
```
:::

:::{dropdown} The transcript, trimmed to the task
```{literalinclude} ../exercises/05-llm/.exercise/project/runs/opencode-free/transcript.md
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

```{literalinclude} ../exercises/05-llm/.exercise/project/runs/opencode-free/verdict.txt
```

- This card is Model B's first recording in exercise 5's step 3.
- It can't state the decisions, because they weren't in the folder.
- `runs/model-b-opencode-second` is the same command with `decisions.yaml` added, and that card passes.

## Fill in the manifest

- Record the tool and its version, the model and any revision, the date, the settings, the prompt, the acceptance result, who decided, and what isn't exposed to you.
- Free models change, so record the exact model name and the date.

Here's the one for this run:

```{literalinclude} ../exercises/05-llm/.exercise/project/runs/opencode-free/manifest.yaml
:language: yaml
```

## OpenRouter: documented here, not run

- **We did not run OpenRouter.** No command on this page was tested with it, and there's no recording.
- It sells access to many models through one API, and some of those models are free.

This is what its pages said when we checked on November 7, 2026:

- You need an account and an API key. That's different from what we ran with OpenCode.
- Free model IDs end in `:free`. The [limits page](https://openrouter.ai/docs/api/reference/limits) gives 20 requests a minute, and 50 requests a day if you've bought less than 10 credits in total, or 1,000 a day if you've bought at least 10. It also says a negative balance can cause errors on free models.
- [Provider logging](https://openrouter.ai/docs/guides/privacy/provider-logging) says each provider has its own data policy, and that your account settings have separate choices for whether paid and free models can be routed to providers that may train on your data. If you opt out, it won't route to those providers.
- Its [terms](https://openrouter.ai/terms), updated August 31, 2026, and its [privacy policy](https://openrouter.ai/privacy) say that some models may store or train on your input, and tell you to review each model's terms yourself.

- Check these pages again before you rely on them, because they change.
