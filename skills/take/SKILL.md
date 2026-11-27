---
name: take
description: Find a GitHub issue, assign it, implement it, verify it, and open a pull request. Use when the user invokes take, asks to take an issue, implement an issue, work on an issue number or URL, or pick up an issue from a description.
---

# Take

Take an issue from first read to an open pull request.

Read [work-lifecycle](../references/work-lifecycle.md) for bounded context, authority, checkpoints, review, and resumption. Use [context-routing](../references/context-routing.md) to find the right workspace before you search for or create local records. If an owning issue or plan already exists, reuse it and the decisions already accepted in it. Keep small work inline.

## Workflow

### 0. Check for work already under way

Start with `git status -sb` and look for an existing entry artifact. If this issue already has work in progress, reconcile before you act:

- the checkout and branch,
- the current PR or tracker state,
- earlier evidence,
- who owns any uncommitted changes,
- reviews that are still pending.

Then take the next authorized step. Do not assign, branch, or open a PR a second time just because the workflow begins at step 1. Checked boxes and old test results need to be rechecked against the current revision.

If a phased plan exists, load the read-first set for the current phase and the decisions and prototype findings it links to. For a small task, the issue, the relevant code, and an inline checklist are enough. The issue owns the assigned scope and status. A plan, if there is one, owns the order of work. Link to each rather than starting a second progress record.

### 1. Locate the issue

The request may give a number, a URL, or only a description.

- One clear match: continue.
- Several matches: show the numbers and titles and ask the user to pick one.
- No match: offer to file a new one with the `issue` skill, and wait for the answer.

### 2. Read and understand it

Read the whole issue and its comments. Note:

- The kind of issue: defect, new feature, enhancement, cleanup, documentation, or chore.
- The behavior the reporter wants, and the acceptance criteria.
- Any technical notes and the files involved.
- Discussion or clarifications that change the picture.

Issues drafted through intake may carry a readback, open questions, and a readiness statement. Older ones may have `## Confidence` and `## Open questions` headings. Handle the questions this way:

- An unanswered `Critical:` question blocks the work.
- An `_Awaiting answer._` entry or a `More Info Needed` label blocks the work only when it stands for user intent that reading the code cannot supply.
- Settle blockers with the user.
- A question marked `_Deferred by user; not blocking implementation._` can stay open.

If the issue is thin, read the codebase before you decide whether it is safe to build.

### 3. Assign it

Set the current GitHub user as the assignee. If another person is already assigned, check with the user before you continue.

### 4. Plan

Run `git status --short` before you create a branch. Keep unrelated uncommitted work intact, and ask before carrying changes you cannot place into the new branch.

Write a short checklist drawn from the issue, its acceptance criteria, what you learned from the code, and the patterns the repository already uses.

If the issue is more than a trivial edit, use `rpi` under the [RPI local rules](../references/rpi-local.md), with the issue as the request. Pick up any existing RPI documents at their first unfinished step. RPI's research, design, and outline stages take the place of this checklist, and in step 5 you create the branch and then follow RPI's implement stage instead of the checklist. Steps 6 to 8 still apply. Settle technical unknowns through RPI research or an authorized [prototype](../prototype/SKILL.md). If a prototype is inconclusive or cannot run, hold back the work that depends on it. A trivial issue keeps its inline checklist.

### 5. Build

Branch from the repository's configured base branch. Do not assume the name is `main` or `master`. Do not pull or rebase unless asked.

Follow the checklist:

- Read a file before you change it.
- Match existing patterns.
- Stay focused on the issue, and skip speculative extras.
- Change docs, examples, tests, or API reports too if the issue needs them.

Track progress with [bounded working context](../references/work-lifecycle.md#keep-working-context-bounded). Keep progress for small tasks inline. When durable work has an owning artifact, update it. If the task outgrows inline context, apply the lifecycle's rule for choosing a mode before you create a record. Use [delegated-execution](../delegated-execution/SKILL.md) only when delegation is authorized.

### 6. Verify

Start with the narrowest checks that cover your change. Widen them if you touched behavior that other code shares.

Take the final checks from the repository's instructions and package scripts, for example:

```bash
<package-manager> run typecheck
<package-manager> run lint
```

For a change within one package, run that workspace's tests before repo-wide checks. Never run placeholder commands as written.

### 7. Open the PR

Use the `pr` skill. In the PR:

- Close the issue from the description with `Closes #<issue-number>`.
- Carry over the context from the issue thread that a reviewer needs.
- Describe how to test it.

### 8. Report back

Finish with:

- The issue you implemented.
- The main changes and the files they touch.
- The verification you ran.
- The PR link.
- Steps for testing by hand, where useful.
- Acceptance criteria you could not meet, and why.

For durable work, record completion or handoff in the owning checkpoint, following [work-lifecycle](../references/work-lifecycle.md#checkpoint-before-context-is-lost). For small work, the report is the checkpoint. If the work is partial, include open reviews, blockers, and the next action. Publishing local context or updating remote records still needs its own authority.

## Rules

- If an important requirement is still unclear after you have read the code, ask the user. A leftover `_Awaiting answer._` placeholder blocks only the work that depends on it.
- Settle routine implementation choices from the request, the agreed criteria, and the repository's conventions. Ask before deciding unspecified product behavior that matters.
- Keep the change within the scope of the issue.
- Leave AI attribution out of commits, issues, and PRs.
