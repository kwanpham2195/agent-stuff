---
name: write-tbp
description: Write technical blog posts explaining how a project solves a problem through its implementation.
---

# Writing a technical blog post

## Steps

### 1. Set up a folder for the topic

Make the folder in the workspace of the project you are writing about. Do not put it inside the installed skill directory.

```
assets/<topic>/
├── research.md   # what you found while researching
└── draft.md      # the post itself
```

Name the topic with a short kebab-case slug, such as `job-retries`, `index-rebuilds`, or `log-rotation`.

### 2. Research

Research the topic thoroughly before you write. Delegate it with [delegated-execution](../delegated-execution/SKILL.md), using the active harness's native exploration role and its launch protocol. Having source material handed to you does not excuse this step. If delegation is unavailable or forbidden, say that it blocks the work. Do not skip the research quietly.

Keep the brief read-only and limited to the topic and the target codebase. Ask the researcher to collect:

- implementation files, types, and schemas,
- examples and demos,
- documentation,
- tests that show how the code behaves,
- comments that explain a decision.

The researcher returns one summary, with links to sources, covering how the feature works, what each relevant file does and which functions or classes matter, interesting details, decisions that are not obvious, and what the evidence does not cover. It should leave unrelated areas alone, change no code, and not delegate further.

Save the result as `assets/<topic>/research.md` in the target workspace.

### 3. Find the angle

Read the research, then answer:

- **What problem does this solve?** Ask what would go wrong without it, not what it does.
- **What is surprising?** Look for the obvious approach that fails, or for complexity that is hidden.
- **What is the key insight?** Name the idea that makes the solution work.
- **What did we try first?** Tell a story of attempts only if the code, comments, or other sources show it. Never invent history.

If you find no interesting angle, the topic may not suit a technical blog post.

### 4. Draft

Read [blog-guide](../references/blog-guide.md) and [Writing reviewable artifacts](../references/writing.md). Write `assets/<topic>/draft.md` in the target workspace, following the guide's structure and the shared writing standards.

Aim for 800 to 1500 words.

### 5. Check your own draft

Go through the evaluation checklist at the end of the blog guide. Revise wherever the draft falls short.

### 6. Hand it over

Show the finished draft to the user. It stays at `assets/<topic>/draft.md` in the target workspace until the user accepts it. Do not move or publish it first. After acceptance, the user can place it where it belongs.

## References

- **Style guide**: `../references/blog-guide.md` covers voice, tone, and structure.
- **Shared writing standards**: [Writing reviewable artifacts](../references/writing.md).
