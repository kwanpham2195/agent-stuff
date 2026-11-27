---
name: write-issue
description: Reference standards for writing and maintaining local or remote issues. Use when another skill needs issue title, body, type, or triage guidance.
---

# Writing and maintaining issues

Before drafting or materially revising the issue's human-facing prose, read and apply [Writing reviewable artifacts](../references/writing.md).

Read and apply [unslop](../unslop/SKILL.md) whenever writing or revising an issue title or body. Before presenting a draft or saving an issue, scan, rewrite, and self-audit the prose you authored. Preserve verbatim user descriptions and quoted evidence.

These content standards apply to local and remote issues. Destination-specific APIs, types, labels, milestones, and automation apply only when that remote tracker supports them. Local mode uses the metadata and lifecycle in the [issue skill](../issue/SKILL.md) and never requires GitHub, `gh`, or network access.

## Title standards

- **Sentence case** - Capitalize only the first word and proper nouns
- **No type prefixes** - Use the destination's type metadata when supported; do not prefix titles with `Bug:`, `Feature:`, `[Bug]`, etc.
- **Imperative mood for enhancements** - "Add padding option" not "Adding padding option"
- **Descriptive for bugs** - Describe the symptom: "Arrow bindings break with rotated shapes"
- **Specific** - Readable without opening the issue body

### Good titles

- `Arrow bindings break with rotated shapes`
- `Add padding option to zoomToFit method`
- `Pinch zoom resets selection on Safari`

### Bad titles

- `Bug: arrow bug` (prefix, vague)
- `[Feature] Add new feature` (prefix, vague)
- `Not working` (vague)

### Title cleanup transformations

1. Remove prefixes: `Bug: X` → `X`
2. Fix capitalization: `Add Padding Option` → `Add padding option`
3. Use imperative: `Adding feature X` → `Add feature X`
4. Be specific: `Problem` → `[Describe the actual problem]`
5. Translate non-English titles to English

## GitHub issue types

Set via the GitHub GraphQL API after creating the issue (the `--type` flag is not reliably supported):

| Type      | Use for                             |
| --------- | ----------------------------------- |
| `Bug`     | Something isn't working as expected |
| `Feature` | New capability or improvement       |
| `Example` | Request for a new SDK example       |
| `Task`    | Internal task or chore              |

## GitHub labels

Use sparingly (1-2 per issue) for metadata, not categorization.

### Common labels

| Label              | Use for                          |
| ------------------ | -------------------------------- |
| `good first issue` | Well-scoped issues for newcomers |
| `More Info Needed` | Requires additional information  |
| `sdk`              | Affects the SDK                  |
| `a11y`             | Accessibility                    |
| `performance`      | Performance improvement          |
| `api`              | API change                       |

### Recurring-work labels

Use `recurring` for a standing issue that remains open across repeated runs. Add at most one work label beside it:

| Label          | Use for                                                |
| -------------- | ------------------------------------------------------ |
| `recurring`    | Standing work repeated on a cadence or for each release |
| `maintenance`  | Dependency, tooling, performance, or code-health work   |
| `verification` | Repeated product or release verification                |
| `release`      | Work tied to preparing or validating a release          |
| `blocked`      | Work cannot continue until a named condition changes    |

Keep standing recurring issues open. Record each completed run in a dated comment with its evidence, follow-ups, and next due date. Apply `blocked` only while a concrete condition prevents the next run, and remove it when that condition clears.

### Automation labels (do not apply manually)

`keep`, `stale`, `update-snapshots`, `publish-packages`, `major`, `minor`, `skip-release`, deploy triggers

## Issue body standards

### Bug reports

1. Clear description of what's wrong
2. Steps to reproduce
3. Expected vs actual behavior
4. Environment details (browser, OS, version) when relevant
5. Screenshots/recordings when applicable

### Feature requests

1. Problem statement - What problem does this solve?
2. Proposed solution - How should it work?
3. Alternatives considered
4. Use cases

### Example requests

1. What API/pattern to demonstrate
2. Why it's useful
3. Suggested approach
4. Which example category it belongs to

### Request-intake issues (problem readback and open questions)

Request-intake issues preserve the user's intent with an unheaded readback beneath the verbatim description, any unresolved questions, and a plain readiness statement:

- **Problem readback** - A brief, unheaded paragraph that states the agent's interpretation of the problem, expected behavior, and scope. It should be easy for the user to correct. Keep it product-facing: no code blocks, no long implementation analysis, no file paths, no function names, no line numbers, and no fix recipes unless the user explicitly asks for them.
- **Open questions** - A numbered list of the specific gaps in intent or context still worth asking the user about. Answers are written beneath each question as the user replies, and the readback is revised each round. A question prefixed with `Critical:` is genuinely blocking — the issue cannot be worked on until it is answered. Most issues have none. Non-critical questions the user chooses not to answer are marked `_Deferred by user; not blocking implementation._`.
- **Readiness line** - State whether the issue has enough intent to proceed or name the missing decision. Do not invent confidence percentages or ask questions to fill the template. Omit open questions when the supplied request is sufficient.

Keep the final readback and readiness statement in the issue. Preserve actual answered questions as the intent record, marking them resolved in place. Do not require a question round before finishing a clear issue request.

## GitHub triage workflow

### New issues

1. Verify sufficient information to act on
2. Set appropriate issue type
3. Clean up title if needed
4. Add `More Info Needed` label and comment if details missing
5. Add `good first issue` if appropriate

### Stale issues

1. Review if still relevant
2. Close if no longer applicable
3. Add `keep` label if should remain open
4. Request updates if waiting on information

## Important

- Never include AI attribution unless the issue directly relates to AI tooling
- Never use title case for descriptions - use sentence case
