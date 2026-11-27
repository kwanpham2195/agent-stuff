---
name: code-review
description: "Review committed, pull-request, or working-tree changes along two separate axes: repository standards and the originating spec. Use when the user asks to review a branch, PR, WIP changes, or changes since a named ref."
---

Two-axis review of the selected change set:

- **Standards** — does the code conform to this repo's documented coding standards?
- **Spec** — does the code faithfully implement the originating issue / PRD / spec?

The review task owner sizes the review first (step 4). A small change gets one reviewer covering both axes. Otherwise it runs the two axes in parallel only within authorized delegation allowance, available capacity/tools, and the [two-axis reviewer exception](../delegated-execution/references/model-policy.md#code-review-exception). Lower task/runtime limits serialize them. If dispatch is unavailable or lacks allowance, the authorized review task owner may review sequentially inline, keeping axis evidence/findings separate; this grants no delegation or implementation authority.

The review task owner reconciles Standards and Spec findings against source and reports the two axis outputs to the thread or parent that requested the review, which retains acceptance. Missing task authority pauses the review. No reviewer assignment authorizes code edits, publication, or independent messages. Only the [T3 exploration-nesting contract](../delegated-execution/SKILL.md#t3-exploration-nesting) permits reserved read-only exploration descendants; it never delegates the review verdict.

Before dispatch, read [delegated execution](../delegated-execution/SKILL.md) and its current [model policy](../delegated-execution/references/model-policy.md). For T3-owned reviews read [T3 routing](../delegated-execution/references/t3-routing.md).

## Process

### 1. Select the review source

Use the source the user supplied. A pull request already supplies a base: resolve that base and do not ask the user to repeat it. A committed review uses the named commit, branch, tag, or merge-base. A WIP review includes the working tree even when no committed base was supplied.

For a named fixed point, preserve the requested comparison semantics. The default committed-range command is `git diff <fixed-point>...HEAD` (three-dot, comparing from the merge-base), with commits from `git log <fixed-point>..HEAD --oneline`. If the user asks for an exact commit comparison or supplies a two-dot range, use that exact range instead of silently substituting a merge-base comparison.

For WIP changes, capture the committed range when a base exists, then inspect the working-tree layers separately: `git diff` for unstaged changes, `git diff --cached` for staged changes, and `git ls-files --others --exclude-standard` for untracked files. Include those paths in the review scope and do not treat them as committed history.

Before going further, confirm every supplied ref resolves (`git rev-parse <ref>`) and that the selected change set is non-empty. A bad ref or empty change set should fail here, before delegation or the review axes.

### 2. Identify the spec source

Look for the originating spec, in this order:

1. Issue references in the commit messages (`#123`, `Closes #45`, GitLab `!67`, etc.).
2. A path the user passed as an argument.
3. A PRD/spec file under `docs/`, `specs/`, or `.scratch/` matching the branch name or feature.
4. If nothing is found, ask the user where the spec is. If they say there isn't one, do not launch a Spec child; the task reports "no spec available" under the Spec axis.

### 3. Identify the standards sources

Anything in the repo that documents how code should be written, such as `CODING_STANDARDS.md` or `CONTRIBUTING.md`.
Otherwise use `/coding-standards` as the general rules.

On top of whatever the repo documents, the Standards axis always carries the **smell baseline** below — a fixed set of Fowler code smells (_Refactoring_, ch.3) that applies even when a repo documents nothing. Two rules bind it:

- **The repo overrides.** A documented repo standard always wins; where it endorses something the baseline would flag, suppress the smell.
- **Always a judgement call.** Each smell is a labelled heuristic ("possible Feature Envy"), never a hard violation — and, like any standard here, skip anything tooling already enforces.

Each smell reads _what it is_ → _how to fix_; match it against the diff:

- **Mysterious Name** — a function, variable, or type whose name doesn't reveal what it does or holds. → rename it; if no honest name comes, the design's murky.
- **Duplicated Code** — the same logic shape appears in more than one hunk or file in the change. → extract the shared shape, call it from both.
- **Feature Envy** — a method that reaches into another object's data more than its own. → move the method onto the data it envies.
- **Data Clumps** — the same few fields or params keep travelling together (a type wanting to be born). → bundle them into one type, pass that.
- **Primitive Obsession** — a primitive or string standing in for a domain concept that deserves its own type. → give the concept its own small type.
- **Repeated Switches** — the same `switch`/`if`-cascade on the same type recurs across the change. → replace with polymorphism, or one map both sites share.
- **Shotgun Surgery** — one logical change forces scattered edits across many files in the diff. → gather what changes together into one module.
- **Divergent Change** — one file or module is edited for several unrelated reasons. → split so each module changes for one reason.
- **Speculative Generality** — abstraction, parameters, or hooks added for needs the spec doesn't have. → delete it; inline back until a real need shows.
- **Message Chains** — long `a.b().c().d()` navigation the caller shouldn't depend on. → hide the walk behind one method on the first object.
- **Middle Man** — a class or function that mostly just delegates onward. → cut it, call the real target direct.
- **Refused Bequest** — a subclass or implementer that ignores or overrides most of what it inherits. → drop the inheritance, use composition.

### 4. Run the review axes

**Size the review.** A change is small when the diff is roughly 150 changed lines or fewer across about 5 files or fewer, the spec and standards sources are short enough to read in one pass, and none of the risk triggers under _Optional adversarial synthesis_ apply. For a small change use one read-only reviewer (or the task owner inline) that covers both axes. Give it both prompts below, and have it return `## Standards` and `## Spec` sections separately; the axes stay separate in the report. Use two reviewers when the change is larger, the context read is large, or the user asks for independent axes.

Otherwise use exactly one read-only reviewer per available axis, up to two concurrently under the shared code-review exception. Each receives its axis, exact changed-head source/diff, criteria, source scope, remaining cumulative budget and stops. Reviewers cannot edit, send independent messages, accept the change or spawn other reviewers. Exploration-only children require the linked T3 contract and root-reserved capacity; otherwise no further delegation. Reserve total and role capacity before dispatch, including descendants; if a lower limit allows only one reviewer, serialize axes. Without permitted dispatch, the authorized task owner performs the available axes sequentially inline. The prompts and evidence stay the same in either mode.

**Standards sub-agent prompt** — include:

- The full diff command and commit list.
- The list of standards-source files you found in step 3, **plus the smell baseline from step 3** pasted in full — the sub-agent has no other access to it.
- The brief: "Report — per file/hunk where relevant — (a) every place the diff violates a documented standard: cite the standard (file + the rule); and (b) any baseline smell you spot: name it and quote the hunk. Distinguish hard violations from judgement calls — documented-standard breaches can be hard, but baseline smells are always judgement calls, and a documented repo standard overrides the baseline. Skip anything tooling enforces. Findings only, no preamble."

**Spec sub-agent prompt** — include:

- The diff command and commit list.
- The path or fetched contents of the spec.
- The brief: "Report: (a) requirements the spec asked for that are missing or partial; (b) behaviour in the diff that wasn't asked for (scope creep); (c) requirements that look implemented but where the implementation looks wrong. Quote the spec line for each finding. Findings only, no preamble."

If the spec is missing, skip the Spec sub-agent and note this in the final report.

For consequential safety or compatibility assumptions, or an explicit impact review, read [impact analysis](references/impact-analysis.md). Include its evidence in the applicable Standards or Spec axis and preserve unverified risks as such.

**Optional adversarial synthesis** — when the user requests it or the change has material correctness, security, privacy, compatibility, or concurrency risk, the task owner may reconcile existing evidence or arrange subsequent independent read-only rounds through an authorized supported harness, including T3. Complete the axis runs first and serialize subsequent rounds under the normal one-reviewer cap, remaining cumulative allowance and lower limits. Give each reviewer the same intent, exact changed-head diff, relevant spec/impact evidence, prior findings/responses, unresolved objections and bounded report contract. For independent T3 rounds, start a fresh delegated task with full context and a distinct stable request ID under shared T3 routing. Do not nest review rounds or invoke an external runner; only reserved exploration support under the linked T3 contract is permitted. Reviewers do not edit, apply changes, or message other owners.

Keep adversarial findings separate from Standards and Spec until the parent reconciles them against the current changed-head source and tests. Treat findings as hypotheses, resolve contradictions with source or authorized checks, and invalidate results when the head changes. Where the review's authorized probes allow, require each reviewer finding to carry the command it ran, its output, and the output the intent requires. The parent reruns the command at the current changed head and keeps the finding only when the output shows the failure and the failure breaks the intent. Within the adversarial findings, merge those that share a root cause. For each reviewer, report how many of its findings the parent dropped and why. A finding without a run stays a labeled hypothesis. Reviewer agreement is evidence strength, not vote-based truth. If authorized independent review capability or allowance is unavailable, report that missing evidence; inline synthesis may reconcile existing findings but must not claim independent review.

When the user asks an agent to review and also change the work, follow [review and fix](../delegated-execution/references/review-and-fix.md). Its edits are proposals until the parent reads the diff and reruns the checks.

Route added-comment checks to the comment sweep in [write-pr](../write-pr/SKILL.md); do not duplicate that sweep here.

### 5. Aggregate

Before drafting or materially revising the human-facing review report, read and apply [Writing reviewable artifacts](../references/writing.md).

Present the two reports under `## Standards` and `## Spec` headings, verbatim or lightly cleaned. Do **not** merge or rerank findings — the two axes are deliberately separate (see _Why two axes_).

End with a one-line summary: total findings per axis, and the worst issue _within each axis_ (if any). Don't pick a single winner across axes — that's the reranking the separation exists to prevent.

## Why two axes

A change can pass one axis and fail the other:

- Code that follows every standard but implements the wrong thing → **Standards pass, Spec fail.**
- Code that does exactly what the issue asked but breaks the project's conventions → **Spec pass, Standards fail.**

Reporting them separately stops one axis from masking the other.
