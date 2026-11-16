---
name: write-tbp
description: Write technical blog posts explaining how a project solves a problem through its implementation.
---

# Write technical blog post

## Process

### 1. Create the workspace

Create an assets folder for this topic in the target project workspace, not in the installed skill directory:

```
assets/<topic>/
├── research.md   # Gathered context and notes
└── draft.md      # The blog post draft
```

Use a short, kebab-case name for the topic (e.g., `cache-invalidation`, `query-planning`, `dash-patterns`).

### 2. Research the topic

Delegate thorough research before drafting, using [delegated-execution](../delegated-execution/SKILL.md) and the active harness's native exploration role and launch protocol. Supplied source does not waive this research step. If delegation is unavailable or prohibited, report the blocker rather than silently skipping it.

Bound the read-only brief to the topic and target codebase. Gather implementation files, types/schemas, examples/demos, documentation, behavior-revealing tests, and comments explaining decisions. Return a comprehensive source-linked summary of how the feature works, each relevant file's responsibility and key functions/classes, interesting details, non-obvious decisions, and evidence gaps for the drafting agent. Stop at unrelated areas; do not modify code or delegate further.

Save the research output to the target workspace's `assets/<topic>/research.md`.

### 3. Identify the interesting angle

Before writing, answer these questions from the research:

- **What problem does this solve?** Not "what does it do" but "what would go wrong without it?"
- **What's surprising or unintuitive?** The obvious approach that doesn't work, or the hidden complexity.
- **What's the key insight?** The "aha" that makes the solution work.
- **What did we try first?** Include a journey or iteration only when evidenced by code, comments, or other sources. Do not fabricate history.

If you can't find an interesting angle, the topic may not be suitable for a technical blog post.

### 4. Write the draft

Read [blog-guide](../references/blog-guide.md) and [technical-writing](../technical-writing/SKILL.md). Create `assets/<topic>/draft.md` in the target workspace using the blog-guide's structure and shared writing standards.

Target 800-1500 words.

### 5. Self-evaluate

Review the draft against the blog-guide evaluation checklist and revise any gaps.

### 6. Output

Present the final draft to the user for review. The draft remains in the target workspace's `assets/<topic>/draft.md` until the user accepts it. Do not promote or move it before acceptance; the user can then move it to the appropriate location.

## References

- **Style guide**: See `../references/blog-guide.md` for voice, tone, and structure.
- **Shared writing standards**: See [technical-writing](../technical-writing/SKILL.md).
