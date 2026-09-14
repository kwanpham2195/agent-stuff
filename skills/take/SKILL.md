---
name: take
description: Find a GitHub issue, assign it, implement it, verify it, and open a pull request. Use when the user invokes take, asks to take an issue, implement an issue, work on an issue number or URL, or pick up an issue from a description.
---

# Take

Find an issue, implement it, and open a pull request.

Read [work-lifecycle](../references/work-lifecycle.md) for bounded context, authority, checkpoints, review, and resumption. Use [context-routing](../references/context-routing.md) to resolve the workspace before searching or creating local records. Reuse an existing owning issue/plan and its accepted decisions; keep small work inline.

## Workflow

### 0. Resume existing work first

Check `git status -sb` and any existing entry artifact. If this issue already has work in progress, reconcile its checkout/branch, current PR or tracker state, prior evidence, dirty-work ownership, and pending reviews before taking the next authorized action. Do not repeat assignment, branch creation, or PR creation merely because this workflow starts at step 1. Stored checkboxes and old passing tests need reconciliation against the current revision.

For an existing phased plan, load the current phase's read-first set and relevant linked decisions/prototype findings. For a small task, use the issue, relevant code, and an inline checklist. The issue owns assigned scope and status; a plan, when present, owns sequencing. Link these authorities rather than creating competing progress records.

### 1. Find the issue

The user may reference an issue by number, URL, or description.

If there is one clear match, proceed. If several issues match, ask the user to choose from issue numbers and titles. If none match, ask whether to create a new issue using the `issue` skill.

### 2. Understand the issue

Read the full issue and comments. Identify:

- Issue type: bug, feature, enhancement, cleanup, docs, or task.
- Requested behavior and acceptance criteria.
- Technical notes and affected files.
- Relevant discussion or clarifications.

Agent-drafted issues may include `## Confidence` and `## Open questions` sections. Treat an unanswered `Critical:` question as a blocker. An `_Awaiting answer._` entry or `More Info Needed` label blocks implementation only when it represents missing user intent that codebase exploration cannot resolve. Resolve those blockers with the user; non-critical questions marked `_Deferred by user; not blocking implementation._` may remain open.

If the issue lacks detail, explore the codebase before deciding whether implementation is safe.

### 3. Assign the issue

Assign the issue to the current GitHub user. If someone else is already assigned, ask the user whether to proceed.

### 4. Plan the implementation

Check `git status --short` before creating a branch. Preserve unrelated dirty work and ask before carrying ambiguous changes into the implementation branch.

Create a concise implementation checklist based on:

- The issue description.
- Acceptance criteria.
- Codebase exploration.
- Existing repo patterns.

For substantial dependencies, consequential technical unknowns, or work across sessions, offer [write-exec-plan](../write-exec-plan/SKILL.md) unless an accepted plan already exists. Its workflow resolves technical unknowns through bounded prototypes before drafting dependent implementation phases. Reuse prior evidence; block dependent work when a prototype is inconclusive or cannot run. Observe the plan's review gate before execution. A small issue keeps its checklist inline.

### 5. Implement

Create a new branch from the repository's configured base branch. Do not assume `main` or `master`, and do not pull or rebase implicitly.

Work through the checklist:

- Read files before editing them.
- Follow existing patterns.
- Keep changes focused on the issue.
- Avoid speculative improvements.
- Update docs, examples, tests, or API reports when the issue requires it.

Work through the authorized checklist or plan using [bounded working context](../references/work-lifecycle.md#keep-working-context-bounded). Keep small-task progress inline; update the owning artifact when durable work has one. If work grows beyond inline context, use the lifecycle's mode-selection rule before creating a record. Use [delegated-execution](../delegated-execution/SKILL.md) only when delegation is authorized.

### 6. Verify

Run the smallest relevant checks first. Use broader checks when the change touches shared behavior.

Choose final checks from the repository's instructions and package scripts. For example:

```bash
<package-manager> run typecheck
<package-manager> run lint
```

For focused package changes, prefer the relevant workspace tests before repo-wide checks. Do not run placeholder commands literally.

### 7. Create the PR

Use the `pr` skill.

- Link the issue with `Closes #<issue-number>`.
- Include relevant context from the issue discussion.
- Include a clear test plan.

### 8. Summarize

End with:

- Issue implemented.
- Key changes and files modified.
- Verification performed.
- PR link.
- Manual testing steps, if relevant.
- Any acceptance criteria that could not be met and why.

For durable work, update the owning checkpoint for completion or handoff using [work-lifecycle](../references/work-lifecycle.md#checkpoint-before-context-is-lost). For small work, the summary above is the checkpoint; include unresolved review, blockers, and the next action if partial. Publishing local context or updating remote records still requires the applicable authority.

## Rules

- Ask the user when requirements are unclear. Do not implement past unanswered critical questions or unresolved `_Awaiting answer._` placeholders.
- Do not guess at unspecified product behavior.
- Keep the implementation scoped to the issue.
- Never include AI attribution in commits, issues, or PRs.
