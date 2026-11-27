---
name: write-pr
description: Standards for PR titles, descriptions, and added comments. Supporting guidance for PR workflows; use pr to create or update a PR.
---

# Writing pull requests

Before drafting or materially revising the PR's human-facing prose, read and apply [Writing reviewable artifacts](../references/writing.md).

Read and apply [unslop](../unslop/SKILL.md) whenever writing or revising a PR title or description. Before presenting a draft or publishing an update, scan, rewrite, and self-audit the prose you authored. Preserve quoted evidence and the human notes defined below exactly.

## Write for the reviewer

Assume the reviewer knows the architecture but has not read the diff. Default to a few sentences, expanding only when the change warrants it. Order framing from coarse to granular: the concrete goal, motivation, and use case first; then changed behavior and structure; then API decisions, alternatives, uncertainty, and minimal before/after usage examples when API, data shape, or usage changes.

Do not restate the diff, narrate files or functions, or add tables that merely repeat signatures. Motivation and tradeoffs must come from commits, linked issues, or the author. Ask the user when the rationale is missing; never invent it.

## PR title

Follow the repository's title convention. Otherwise use Conventional Commits:

```
<type>(<scope>): <description>
```

Use `feat`, `fix`, `docs`, `refactor`, `perf`, `test`, or `chore` as appropriate. Scope is an optional noun naming the affected area.

## PR body

Use the repository's PR template when present. The following templates are optional starting points: keep only sections that help explain this change. Body change-type labels are repository-specific and need not match Conventional Commit prefixes.

```md
[{TICKET_ID}]({TICKET_URL})

<description paragraph>

### Change type

- [x] `bugfix` | `improvement` | `feature` | `api` | `other`

### Change outline

<change outline>

### Test plan

1. Step to test...
2. Another step...

- [ ] Unit tests
- [ ] End to end tests

### Release notes

- Brief description of changes for users
```

### Description paragraph

Lead with the actual situation that prompted the work and the resulting behavior, not a circular restatement of the mechanism or a hypothetical use case. Link related issues here, but make the paragraph understandable without opening them.

### Bug fix and improvement PRs

For bug fixes and improvements, a before/after structure can help a reviewer see what changed and why. A small fix may need only a paragraph and its validation result.

```md
[{TICKET_ID}]({TICKET_URL})

This PR fixes a bug where <symptom a user or developer would hit>.

### Before

<what the code did and why that produced the symptom>

### After

<what the code does now>

### Implementation notes

<optional: what exactly changed and how — decisions, trade-offs, anything non-obvious>

### Change type

- [x] `bugfix` | `improvement`

### Change outline

<change outline>

### Test plan

- [ ] Describe checks actually run and their results; claim a before/after failure only when observed

### Release notes

- Fix <symptom> | Improve <behavior>

```

- **Intro** — one sentence. For a bug: "This PR fixes a bug where X," where X is the observable symptom, not the cause or the fix. For an improvement: "This PR improves X so that Y," where Y is what a user or developer can now do. Link the issue here if there is one. If the PR does more than one thing, add a second sentence ("It also ...") rather than a list.
- **Before** — the behavior before, and the mechanism that produced it. For a bug, name the function or path at fault; this is the one place a short description of *how* the old code went wrong belongs, because it is the cause the reviewer is checking the fix against. For an improvement, describe what the user or developer had to do (or couldn't do) and what in the code made it that way.
- **After** — the behavior after. State what the code now does, at the same level of detail as Before. Note any spec or doc that was updated alongside.
- **Implementation notes** — optional. Include only when there is something the Before/After pair doesn't carry: an approach you chose over another, a subtlety in the change, a follow-up you deliberately left out. Skip the heading entirely when there is nothing to say; most small fixes have nothing.
- Include the remaining sections only when required by the repository or useful to the reviewer. For bug fixes, distinguish a regression test from an independently observed failure on the base revision.

### Change type

- Tick exactly one type with `[x]`
- Delete unticked items

### Change outline
- When a structural outline would help, read [references/show-me.md](references/show-me.md) and [references/change-outline.md](references/change-outline.md).
- Make **Change outline** a compact structural view, not a file-by-file narrative. Include only useful schema/endpoint contracts, pseudocode, shallow file trees, component trees, and call/control/data-flow views. Prefer focused `diff` blocks for existing shapes and complete code blocks for mostly new shapes.

### Test plan

- List manual testing steps if applicable
- Remove the numbered list if changes cannot be manually tested
- Tick checkboxes for included test types

### Release notes

- Write brief notes describing user-facing changes
- Use imperative mood: "Add...", "Fix...", "Remove..."
- Omit this section entirely for internal work (CI, tooling, tests, etc.) that has no user-facing impact

## Concepts, examples, and FAQ (only when a reviewer genuinely needs them)

Include these only when reviewers need vocabulary or usage context beyond the code. Place them before the standard sections unless the repository template specifies otherwise. Each row must explain something the code does not.

Pull from this menu, in roughly this order, using only what fits:

- **Concepts** — a table of the new terms/types the PR introduces, with `Term | Type | Meaning` columns. Use this when readers need a shared vocabulary to follow the rest of the description.
- **Module augmentation** — short code blocks showing how consumers extend the new types, when the PR exposes augmentable interfaces.
- **Editor API** / **Component props** — `Method | Description` and `Prop | Type | Description` tables for new public surface.
- **Per-shape / per-feature breakdown** — tables showing what each affected shape/module returns or accepts under the new system.
- **Example** — a realistic, copy-pastable code snippet showing how a default implementation uses the new system, plus a second snippet showing how a consumer would override it.
- **FAQ** — anticipated "How do I…?" questions with short code answers. Cover the obvious customization paths a downstream user will reach for first.
- **New examples** — bullet list of any new entries added under `apps/examples/src/examples/`, with a one-line description each, so reviewers know where to look for runnable demos.

## API changes section

Include when changes affect Public Facing API:

```md
### API changes

- Added `Editor.newMethod()` for X
- Breaking! Removed `Editor.oldMethod()`
- Changed `Editor.method()` to accept optional `options` parameter
```

## Code changes table

Include a LOC table only when the user or repository template requests one. Otherwise a short scope sentence is enough.

Use non-overlapping categories from the actual repository, such as core code, tests, generated files, documentation/examples, apps, templates, and config/tooling. Count additions/deletions from the diff, omit empty rows, and explain binary or generated-file exclusions.

```md
### Code changes

| Section         | LOC change |
| --------------- | ---------- |
| Core code       | +10 / -2   |
| Tests           | +5 / -0    |
| Automated files | +0 / -1    |
| Documentation   | +2 / -0    |
| Apps            | +3 / -1    |
| Templates       | +0 / -0    |
| Config/tooling  | +1 / -0    |
```

## Related issues

Search for and link relevant issues that this PR addresses.

## The comment sweep

A pre-flight check on the diff, not the description: read the diff's added comments as carefully as its added code, and cut before opening the PR.

```bash
git diff "$pr_base"...HEAD -U0 | rg -n '^\+\s*(//|/\*|\*)'
```

Resolve `pr_base` from the PR or repository before running that command. Judge the added comments against the repository's documented comment rules, when present. For a description-only request, report code concerns without editing or committing code. One useful test:

> **A good comment names a failure mode, not a mechanism.**

The mechanism is on screen already. What isn't is what goes wrong without it. A block that only describes what the code does is cuttable in full; a block that says "otherwise X" keeps that sentence and loses the paragraph explaining it twice.

**Expect length, not category, to be the defect.** Most substantial comment blocks that need editing already name a real force — they are the right kind of comment at two or three times the necessary length. So the usual edit is a trim to the load-bearing lines, not a delete.

Leave alone, or trim at most: diagrams, enumerated case lists where the list is the specification, provenance (an issue number, "we tried X and it did Y"), and anything carrying an invariant. In `packages/*`, doc comments on the `@public` surface are the API reference — hold them to the same "says something the code doesn't" bar, but they are a deliverable, not overhead.

## Human notes (preserve exactly)

The PR author often writes a personal note at the very top of the description, prefaced with a "person" emoji such as 🅯 or 👨 (or similar). This block is human-written and readers trust it as such.

- When **updating** an existing PR description, if the body starts with a paragraph/section led by a person emoji, you MUST preserve it **byte-for-byte exactly** at the top — do not rewrite, reflow, reword, retitle, or "improve" it, even slightly.
- If the human note is longer than a single paragraph, it will be delimited at the end by a `---` horizontal rule. Preserve everything from the person emoji through (and including) that `---` exactly.
- If there is no `---`, the human note is just the leading paragraph led by the person emoji.
- Make all your edits to the content **below** the human note (and below the `---` if present).
- When **creating** a new PR, do not invent a human note — leave that for the author to add.

## Important

- Follow the user's and repository's attribution policy; do not add AI or co-author credit on your own
- Never use title case for descriptions - use sentence case
- Never put yourself as co-author of any commits
