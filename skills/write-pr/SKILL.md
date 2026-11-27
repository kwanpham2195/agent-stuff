---
name: write-pr
description: Standards for PR titles, descriptions, and added comments. Supporting guidance for PR workflows; use pr to create or update a PR.
---

# Writing pull requests

Before you draft or substantially revise a PR's prose, read and apply [Writing reviewable artifacts](../references/writing.md).

Apply [unslop](../unslop/SKILL.md) every time you write or revise a PR title or description. Before you show a draft or publish an update, scan your own text, rewrite what needs it, and audit the result. Keep quoted evidence and the human notes described below exactly as they are.

## Write for the reviewer

Picture a reviewer who understands the architecture but has not opened the diff. Their attention is limited, so give them the context the code cannot, then stop. A few sentences usually do it. Grow the description only when the change calls for more.

Order the content from broad to specific, so a reader can stop at any point and still have a correct picture:

1. The concrete goal, the motivation, and the use case.
2. What changed in behavior and structure.
3. API decisions, alternatives you rejected, and anything you are unsure about. Add a small before/after usage example when an API, a data shape, or a usage pattern changes.

Do not repeat the diff. Skip file-by-file tours, step-by-step accounts of what a function does, and tables that only restate signatures.

Take the motivation and the trade-offs from commits, linked issues, or the author. If the reason for the change is missing, ask the user. Never make one up.

## PR title

Use the repository's title convention when it has one. Otherwise write a Conventional Commits title:

```
<type>(<scope>): <description>
```

Pick the type from `feat`, `fix`, `docs`, `refactor`, `perf`, `test`, and `chore`. The scope is an optional noun for the area affected, for example `fix(parser)`.

## PR body

If the repository has a PR template, use it. The templates below are starting points only. Keep the sections that help explain this particular change and drop the others. The change-type labels in the body belong to the repository, so they need not match the commit type.

```md
[{TICKET_ID}]({TICKET_URL})

<description paragraph>

### Change type

- [x] <one of: bugfix, improvement, feature, api, other>

### Change outline

<change outline>

### Test plan

1. First step to try...
2. Next step...

- [ ] Unit tests
- [ ] End-to-end tests

### Release notes

- One line for users describing the change
```

### The description paragraph

Start from the real situation that led to the work, and say what is now possible or fixed. Do not restate the mechanism in other words, and do not make up a hypothetical use case. Put links to related issues in this paragraph, but write it so a reader gets the point without following them.

### Bug fixes and improvements

For these, a before/after layout helps the reviewer see what changed and why. A very small fix may need only a paragraph and the result of its check.

```md
[{TICKET_ID}]({TICKET_URL})

This PR fixes a bug where <the symptom a person would see>.

### Before

<what the code did, and why that caused the symptom>

### After

<what the code does now>

### Implementation notes

<optional: choices, trade-offs, anything non-obvious>

### Change type

- [x] <bugfix or improvement>

### Change outline

<change outline>

### Test plan

- [ ] Checks you actually ran, with results. Say a test failed before the change only if you saw it fail.

### Release notes

- Fix <symptom>, or Improve <behavior>
```

How to fill it in:

- **Intro.** One sentence. For a bug, "This PR fixes a bug where X", where X is the symptom a person can observe, not the cause and not the fix. For an improvement, "This PR improves X so that Y", where Y is what people can now do. Put the issue link here. If the PR does a second thing, add one more sentence beginning "It also" and skip the list.
- **Before.** Say what happened and why. For a bug, name the function or code path at fault. This is the single place where the old code's mechanism belongs, because the reviewer checks the fix against that cause. For an improvement, describe what people had to do, or could not do, and what in the code forced that.
- **After.** Describe the new behavior at the same level of detail. Mention any spec or doc you updated with it.
- **Implementation notes.** Optional. Add them only when the before/after pair leaves something out: a choice between approaches, a subtle point, or a follow-up you left for later. Leave out the whole heading when there is nothing to add. Most small fixes need none.
- Add the other sections only when the repository requires them or they help the reviewer. For a bug fix, separate a regression test you wrote from a failure you saw on the base revision.

### Change type

- Tick exactly one box with `[x]`.
- Delete the boxes you did not tick.

### Change outline

- When a structural outline would help, read [references/show-me.md](references/show-me.md) and [references/change-outline.md](references/change-outline.md).
- Keep the outline compact and structural. Do not write a file-by-file story. Include only what helps: schema or endpoint contracts, pseudocode, a shallow file tree, a component tree, or a call, control, or data flow. Use `diff` blocks for shapes that already exist and full code blocks for shapes that are mostly new.

### Test plan

- List manual steps when the change can be tried by hand.
- Delete the numbered list when it cannot.
- Tick the boxes for the kinds of tests the PR includes.

### Release notes

- Write short notes on what users will notice.
- Use the imperative: "Add...", "Fix...", "Remove...".
- Leave the section out for internal work such as CI, tooling, or tests that users never see.

## Concepts, examples, and FAQ

Add these only when a reviewer needs shared vocabulary or usage context that the code does not give. Size alone is not a reason. Unless the repository template says otherwise, put them before the standard sections. Every row must say something the code does not.

Choose from this list, roughly in this order, and use only what fits:

- **Concepts.** A table with `Term | Type | Meaning` columns for the new terms the PR introduces.
- **Type extension.** Short code blocks showing how consumers extend new types, if the PR exposes interfaces meant to be extended.
- **Public surface.** `Method | Description` and `Prop | Type | Description` tables for new public methods and props.
- **Per-module breakdown.** A table of what each affected module returns or accepts under the new design.
- **Example.** A realistic snippet that shows a default implementation using the new design, and a second that shows a consumer overriding it.
- **FAQ.** The "How do I...?" questions a downstream user will ask first, each with a short code answer.
- **New examples.** A list of any runnable examples the PR adds, each with one line on what it shows, so reviewers know where to look.

## API changes

Add this section when the change touches the public API.

```md
### API changes

- Added `client.newMethod()` for X
- Breaking! Removed `client.oldMethod()`
- Changed `client.method()` to take an optional `options` argument
```

## Code changes table

Include a lines-of-code table only when the user or the repository template asks for one. Otherwise one sentence on the scope is enough.

Use categories that do not overlap and that match the repository, for instance core code, tests, generated files, documentation, apps, templates, and config. Count additions and deletions from the diff. Leave out empty rows. Say so when binary or generated files are excluded.

```md
### Code changes

| Area            | Lines changed |
| --------------- | ------------- |
| Source          | +42 / -7      |
| Tests           | +18 / -0      |
| Generated files | +0 / -3       |
| Docs            | +6 / -1       |
| Config and CI   | +2 / -2       |
```

## Related issues

Look for issues that this PR addresses and link them.

## The comment sweep

This check runs on the diff, not on the description. Read the comments the diff adds as closely as the code it adds, and cut before you open the PR.

```bash
git diff "$pr_base"...HEAD -U0 | rg -n '^\+\s*(//|/\*|\*)'
```

Set `pr_base` from the PR or the repository first. Judge each added comment against the repository's written comment rules, if it has any. When the request is only about the description, report code concerns and do not edit or commit code.

One test to apply:

> **A comment earns its place by saying what breaks without it, not how the code works.**

Anyone can see the mechanism in the code. What they cannot see is what breaks without it. A comment that only says what the code does can go entirely. A comment that says "otherwise X" keeps that sentence and loses the paragraph that explains the same thing twice.

**Length is usually the flaw, not the kind of comment.** Most long comments that need work already name a real hazard. They are the right comment at two or three times the length. So the usual edit is to trim to the lines that matter, not to delete.

Leave these alone, or trim them lightly: diagrams, case lists where the list is the specification, provenance such as an issue number or "we tried X and got Y", and anything that states an invariant. Doc comments on a public API are the reference documentation. Hold them to the same bar of saying something the code does not, but treat them as a deliverable rather than overhead.

## Human notes (keep exactly)

An author may put a personal note at the top of the PR description. Readers trust that block because a person wrote it.

A human note is the author's own text at the very top of the body, set apart from the rest. The most reliable sign is a block that ends with a `---` rule. A paragraph the author labelled as a note also counts. If you cannot tell whether the opening text is a note, treat it as one, and ask the user if it matters.

- When you update an existing description that starts with a human note, keep that note byte for byte. Do not reword, reflow, retitle, or tidy it.
- If the note ends with a `---` rule, the note includes everything up to and including that rule. Without a rule, the note is just the opening paragraph.
- Make all your changes below the note, and below its rule if it has one.
- When you create a new PR, do not write a human note. Leave that to the author.

## Always

- Follow the user's and the repository's attribution policy. Do not add AI or co-author credit on your own.
- Write descriptions in sentence case, never title case.
- Never list yourself as a co-author of a commit.
