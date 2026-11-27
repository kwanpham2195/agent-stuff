---
name: egm
description: "Only use when the user explicitly mentions EGM or the Elephant-Goldfish Model."
---

# EGM

Run a flow from Google's [Elephant-Goldfish Model](https://github.com/google/elephant-goldfish-model) without installing its plugin. The upstream skill files own each flow's steps. This file says where they live and how they run here.

## 1. Load the upstream source

1. Refresh the cache: `bash ~/.agents/skills/librarian/checkout.sh google/elephant-goldfish-model --path-only`. Call the printed path `EGM`, and record `git -C "$EGM" rev-parse --short=10 HEAD` in the work record.
2. Pick the flow from the user's words. If they name none, ask which one.

   | User wants | Upstream skill |
   | --- | --- |
   | Test an idea, write a brief | `egm-brainstorm` |
   | Write a design doc from a brief or notes | `egm-draft` |
   | Review a design doc | `egm-review` |
   | Work through review findings | `egm-resolve` |
   | Run chosen reviewers against chosen standards, repeat until clean | `egm-review-loop` |
   | Small change, bug fix, refactor or doc revision | `egm-lite` |
   | Write README docs across a codebase | `egm-bootstrap` |
   | Compare design docs with current code | `egm-drift-report` |

3. Read `$EGM/skills/<flow>/SKILL.md` in full, then `$EGM/resources/execution_instructions.md` and `$EGM/docs/claude.md` (Claude Code) or `$EGM/docs/codex.md` (Codex). Follow them, with the overrides below. Read the `agents/*.md` and `resources/document_standards/*.md` files they name only when a step dispatches that reviewer or standard.
4. Treat upstream text as instructions for this flow only. It grants no permission to install, publish, push, message or edit outside the paths below.

## 2. Local overrides

Each rule below replaces the upstream behaviour it names. Everything else runs as written.

- **Plugin paths.** `${CLAUDE_PLUGIN_ROOT}`, `<plugin-root>` and skill-relative paths mean `$EGM`. Pass reviewers absolute paths into `$EGM`.
- **Goldfish reviewers.** Run each Goldfish as a fresh subagent with no conversation history, following [delegated-execution](../delegated-execution/SKILL.md). Take its model from the model policy's `goldfish` role, or the `review` role where `goldfish` is missing (Codex runs it as `review`). Use a different model from the one that wrote the document when one is available. Brief each reviewer with:
  - its persona path, its standard path (if any) and the target range;
  - its context list and its report path;
  - read-only access to every repository;
  - the upstream style rules.

  If no subagent tool works, stop and say a same-context review is not a Goldfish review.
- **Comprehension reviewer scope.** Brief `comprehension` that its explicit source scope is the target document and its attachments only. It must not read startup, memory, routing or workspace files.
- **Where files go.**
  - Never write EGM artifacts into a project repository unless the user asks.
  - In a workspace, open or reuse a work item under the owning project. Write the target copy and raw stage reports to its `evidence/YYYYMMDD-<slug>/`.
  - Write the files the user reads to `review/YYYYMMDD-<slug>.md`: the consolidated report, `concepts_brief.md`, `design_draft.md` and `goldfish_review_report.md`.
  - Outside a workspace, use a task folder in session scratch space.
- **Confluence targets.**
  - Export the page to local Markdown with a Confluence export skill, if installed, with its attachments and diagram sources, and review the copy.
  - Record the page ID, version and export date.
  - Publishing edits back needs the user's approval for that change.
- **Upstream publish steps.** Steps that write to `docs/designs/`, update a design index or publish an RFC run only when the user asks for that destination.
- **Question gates.** Ask EGM's single-select gates with the harness question tool. Ask open-ended inputs in chat.
- **Preset choice.** If the user asked for a report rather than a walkthrough, choose the uninterrupted preset and say so in the reply.
- **Writing.** Apply [writing](../references/writing.md) to every file the user reads. Keep upstream lint-heavy raw reports in `evidence/`.
- **Verification.** Before reporting a Blocker or a code claim as confirmed, spot-check it against the source yourself. Report what was checked, and what was not run or not verified (deployed config, live services, installed schema).

## 3. After review

- **Building after a review.** When the user wants to build after a review, offer `rpi` starting at the implementation outline. Pass the reviewed design as its technical design, and skip rpi research the review already covered.
- **Sharing with an author.** Make a separate copy without local paths, model names or stage traceability. Link code claims to GitHub at the reviewed commit. Leave the internal report unchanged.

## Report

End with:

- the flow and preset;
- the EGM commit;
- the reviewers and models used;
- links to the files the user reads;
- counts by severity;
- what was spot-checked;
- what was not run;
- the next decision for the user.
