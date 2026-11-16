# RPI local rules

Read whenever the [rpi](../rpi/SKILL.md) or `visual-pr` skill runs, before its first step. `rpi` and `visual-pr` are HumanLayer's skills, installed unedited through `npx skills` and pinned in `external-skills.json`. Follow them as written, except for the points below.

## Default route

The global guide sends implementation, refactoring and investigation beyond a trivial edit here, even when the user does not name RPI. Treat that as an explicit invocation.

- Use the user's requested step or flow, or the work item's recorded `workflow`. Otherwise follow RPI's own chooser: start with research questions and ask which flow to use.
- Trivial edits, quick lookups and questions answered from existing context stay inline, without RPI documents.
- A conversational thread is no exception. When a chat request turns into code, docs or pull-request changes, start this route: run RPI's chooser, or go code-first as below and say so.
- Go code-first when writing the code costs less than writing a plan for it: the change is reversible, the files are known and no product or architecture decision is open. Skip RPI documents. Write the change, or a rough sketch when the direction is uncertain, and show the diff as the review artifact. Record `workflow: oneshot` if the work item tracks it. Switch to RPI's chooser if the sketch exposes a consequential decision or the change keeps growing.
- When the user says to skip the workflow, implement directly, as RPI's chooser note allows.

## Task directory

- Instead of `.agents/artifacts/<name>`, use the work item's `review/` folder in its owning workspace: `workspaces/<workspace>/work/<id>/review/` under the context root. Resolve the workspace through [first-task routing](first-task-routing.md), then run the [related-work check](context-routing.md#check-for-related-work) to decide whether to reuse an existing work entry or create one. A directory the user names still wins.
- If no workspace owns the directory, ask whether to register it, associate it with an existing workspace, or keep the documents session-only in chat.
- Never write RPI documents into a project repository or commit them there.
- Keep `NN-` numbering, the `repos` frontmatter and supporting mockups beside the documents, as RPI describes.
- Next-step commands name this directory.

## Work state

Keep the work item's `agent/state.md` current after each saved document or finished phase: status, next action, and pending decisions. When the state records workflow fields, update `workflow_stage` and `current_artifact` under [workflow records](context-routing.md#workflow-records), using this flow mapping:

| RPI flow | `workflow` value | RPI stages |
| --- | --- | --- |
| Design discussion | `rpi` | `questions`, `research`, `design`, `outline`, `implementation` |
| PRD, then TDD | `prd` | `questions`, `research`, `prd`, `tdd`, `outline`, `implementation` |
| TDD only, or research only | `freeform` | the stages actually used |
| No documents, from an accepted request | `oneshot` | `implementation` |

Workflow records add `intake` before these stages and `verification` and `delivery` after them. The outline is optional in every flow.

## Subagents and models

Choose execution under [delegated execution](../delegated-execution/SKILL.md); RPI's exploration and implementation subagent steps do not require spawning children. The task owner may follow their prompt instructions inline or use supported tool batching or code mode when more efficient, while retaining RPI's stage order, artifacts, and verification requirements. Explicit independent-review requirements still apply.

When delegation is useful, RPI's subagents are prompt files, not installed agents, in every harness. Use RPI's fallback for unavailable named subagents:

1. Read `references/subagents/<name>.md` in the `rpi` skill.
2. Launch a generic child through [delegated execution](../delegated-execution/SKILL.md), with the file's body as `<instructions>` and the task as `<message>`.
3. Take the child's model and effort from [model policy](../delegated-execution/references/model-policy.md) by role. Ignore the file's `model` line.
4. Treat the file's `tools` list as the child's scope.

| RPI subagent | Policy role | Scope |
| --- | --- | --- |
| `codebase-locator`, `codebase-analyzer`, `codebase-pattern-finder`, `web-search-researcher` | exploration | read-only |
| `outline-implementer-agent` | implementation | writes source and tests for the assigned phase |

Launch on the route delegated execution names for the harness: T3 routing in T3 Code, Claude Code routing in Claude Code, and native children in Codex and Pi. RPI's "run independent investigations in parallel" stays within the policy's role and total caps.

## visual-pr

Use `visual-pr` only when the user asks for it by name. When RPI's handoff suggests `/visual-pr`, use the [pr](../pr/SKILL.md) skill instead and mention `visual-pr` as an option. When the user does ask for it, `visual-pr` writes the PR body from its template, with these overrides:

- Keep HumanLayer out of everything published: no HumanLayer task URLs, `.humanlayer` paths, app permalinks or credits in the PR title, body, commits or comments. Its header links only a public ticket or issue URL, or is omitted.
- Never put local paths or links to private context in the PR. Save the description draft as `pr-description.md` in the work item's `review/` folder, not under `.humanlayer/tasks`.
- Save any `show-me` HTML beside that draft and link it in chat as an ordinary file. Do not use `task-artifact` fences.
- The [pr](../pr/SKILL.md) skill owns branch, commit, push and creation permission, issue links, and the no-AI-attribution rule. `visual-pr` does not push or create a PR beyond what the user asked for.
- The final answer reports the real draft path in place of "cloud permalink from hook".
