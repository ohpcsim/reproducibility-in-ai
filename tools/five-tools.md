---
title: The same task in five tools
---

- Exercise 5 uses recordings, so you don't need any of these to do it.
- These pages show the same task in each tool: write a model card for the frozen classifier, from the files alone.
- Each page has how to install and sign in, the exact command we ran, what the tool wrote, how to fill the manifest, and what the tests decided.

- All five were recorded on November 7, 2026, with the same files and the same prompt.
- Each ran once.
- Codex and OpenCode each ran one more time, for exercise 5's step 3.

| Tool | Model | Rules from step 1 | With the step 3 decisions |
|---|---|---|---|
| [Claude Code](claude-code.md) | `claude-haiku-5-5` | Rejected, for a harmless number | Rejected |
| [Codex](codex.md) | `gpt-6.1-sol` | Accepted | Rejected until it got them in chat |
| [Cursor](cursor.md) | `Auto`, not exposed | Rejected, for a harmless number | Rejected |
| [A local model](local-model.md) | `qwen2.5-coder:7b` | Accepted | Rejected |
| [Free models](free-models.md), through OpenCode | `opencode/deepseek-v4.1-flash-free` | Accepted | Rejected until `decisions.yaml` was in the folder |

- Nobody should read this as a ranking.
- Each tool ran once, on one small task, with a prompt that spelled out what to do.
- What it shows is that the tools got the facts right when the facts were in the project, and none could know a decision that wasn't.
- The tests decide about one card, and a person decides what to do about it.

- Run these only on public or synthetic work unless your institution has approved the tool.
- Your settings, your account's default model and the tool's next version can all change what you get.
- That's why the manifest exists.
