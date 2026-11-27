---
name: write-issue
description: Reference standards for writing and maintaining local or remote issues. Use when another skill needs issue title, body, type, or triage guidance.
---

# Writing and maintaining issues

Before you draft or substantially revise an issue's prose, read and apply [Writing reviewable artifacts](../references/writing.md).

Also apply [unslop](../unslop/SKILL.md) to every issue title and body you write or revise. Before you show a draft or save the issue, scan your own text, rewrite what needs it, and audit the result. Leave the user's own words and any quoted evidence exactly as given.

These standards cover local and remote issues alike. Types, labels, milestones, and automation depend on the tracker, so use them only where the tracker offers them. Local mode follows the metadata and lifecycle in the [issue skill](../issue/SKILL.md). It never needs GitHub, `gh`, or a network connection.

## Titles

A good title reads on its own, in a list, without the body.

- Use sentence case. Capitalize the first word and proper nouns only.
- Leave out type prefixes such as `Bug:`, `Feature:`, or `[Bug]`. Put the type in the tracker's type field when it has one.
- For a request to change something, write an imperative: "Add a timeout option", not "Adding a timeout option".
- For a defect, describe what the user sees: "Export fails on filenames with spaces".
- Be specific enough that the title alone tells the reader what the issue is about.

Good titles:

- `Export fails on filenames with spaces`
- `Add a timeout option to the sync command`
- `Dark theme resets after restarting on Windows`

Weak titles:

- `Bug: export bug` (has a prefix, says nothing)
- `[Feature] Add new feature` (has a prefix, says nothing)
- `Not working` (says nothing)

### Cleaning up a title

1. Strip any prefix: `Bug: X` becomes `X`.
2. Fix the case: `Add Timeout Option` becomes `Add timeout option`.
3. Switch to the imperative: `Adding feature X` becomes `Add feature X`.
4. Replace a vague title with the actual problem.
5. Translate a non-English title into English.

## GitHub issue types

Set the type through the GitHub GraphQL API after you create the issue. The `--type` flag of the CLI is unreliable.

| Type      | Use for                                  |
| --------- | ---------------------------------------- |
| `Bug`     | Behavior that differs from what is expected |
| `Feature` | A new capability or an improvement       |
| `Task`    | Internal work or a chore                 |

## GitHub labels

Labels carry metadata, not categories. Give an issue one or two.

### Common labels

| Label              | Use for                                    |
| ------------------ | ------------------------------------------ |
| `good first issue` | A well-scoped issue a newcomer can take    |
| `More Info Needed` | The report lacks details needed to act     |
| `accessibility`    | Affects users of assistive technology      |
| `performance`      | Speed or resource use                      |
| `api`              | Changes a public interface                 |

### Labels for recurring work

Mark a standing issue that stays open across repeated runs with `recurring`. Pair it with at most one of the labels below.

| Label          | Use for                                                   |
| -------------- | --------------------------------------------------------- |
| `recurring`    | Work that repeats on a schedule or once per release       |
| `maintenance`  | Dependencies, tooling, performance, or code health        |
| `verification` | Repeated checks of the product or of a release            |
| `release`      | Preparing or validating a release                         |
| `blocked`      | Cannot proceed until a named condition changes            |

Leave a standing recurring issue open. After each run, add a dated comment with the evidence, any follow-ups, and when the next run is due. Add `blocked` only while a specific condition stops the next run, and remove it once the condition clears.

### Labels that automation owns

Do not apply these by hand: `keep`, `stale`, snapshot-update or package-publish triggers, version-bump labels, labels that skip a release, and deploy triggers.

## Issue bodies

### Bug reports

1. What is wrong, stated plainly.
2. Steps to reproduce.
3. What you expected and what happened instead.
4. Environment (browser, OS, version) when it matters.
5. Screenshots or recordings if they help.

### Feature requests

1. The problem: what does this solve, and for whom?
2. The proposal: how should it work?
3. Alternatives you considered.
4. Use cases.

### Request-intake issues

A request-intake issue records what the user wants. Under the user's verbatim description it holds a short readback, any open questions, and a statement of readiness.

- **Readback.** One paragraph, with no heading, giving your reading of the problem, the behavior the user expects, and the scope. Write it so the user can correct it quickly. Describe the product, not the code. Leave out code blocks, file paths, function names, line numbers, and implementation analysis. Do not propose a fix unless the user asks for one.
- **Open questions.** A numbered list of the gaps in intent or context that are still worth asking about. Write each answer under its question when the user replies, and revise the readback after every round. Begin a question with `Critical:` only if nobody can work on the issue until it is answered. Most issues have no such question. Mark a question the user chose not to answer with `_Deferred by user; not blocking implementation._`.
- **Readiness.** Say whether the issue has enough intent to start, or name the decision that is missing. Do not put a percentage on it, and do not invent questions to fill space. If the request is already clear, leave out the open questions.

When the issue is done, keep the final readback and the readiness statement in it. Keep the answered questions too, marked resolved in place, because they record how the intent was settled. A clear request needs no question round.

## Triaging on GitHub

### New issues

1. Check that the report has enough detail to act on.
2. Set the issue type.
3. Fix the title if it needs it.
4. If details are missing, comment and add `More Info Needed`.
5. Add `good first issue` if the work suits a newcomer.

### Stale issues

1. Decide whether the issue still matters.
2. Close it if it no longer applies.
3. Add `keep` if it should stay open.
4. If you are waiting on the reporter, ask for an update.

## Always

- Do not credit AI tools unless the issue is about AI tooling.
- Write sentence case in descriptions, never title case.
