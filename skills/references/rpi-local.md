# RPI local rules

Read whenever the `rpi` or `visual-pr` skill runs, before its first step. `rpi` and `visual-pr` are HumanLayer's skills, installed unedited through `npx skills` and pinned in `external-skills.json`. Follow them as written, except for the points below.

Give each delegated stage an outcome and acceptance evidence.

## Default route

The global guide sends implementation, refactoring and investigation beyond a trivial edit here, even when the user does not name RPI. Treat that as an explicit invocation.

Every task starts with its outcome and ends with verification against it. The steps between are chosen per task.

```text
outcome (A1..An + evidence, the user confirms) ─► the lightest steps that fit ─► verify: each criterion passed / failed / blocked / awaiting the user
```

### 1. Agree the outcome first

- Before research questions, write the acceptance contract with [define-outcome](../define-outcome/SKILL.md): who and what problem, the desired outcome, criteria A1..An each with its evidence, and a stop condition when the work is discretionary.
- Put it in the request document, or inline in chat for small work. Reuse criteria an issue or earlier document already holds.
- Wait for the user to confirm the criteria before research or design. Proposed criteria are not agreed criteria.

### 2. Choose the lightest steps that fit

Pick the fewest steps that settle the open decisions, and say which you skip and why. The user's requested step or flow, or the work item's recorded `workflow`, wins.

| Work | Steps |
| --- | --- |
| Product behavior or a new capability | research, PRD, then TDD only if technical choices are open, outline only for several phases |
| A technical change with open design choices | research, design discussion, outline if it has several phases |
| A question about the current system | research only |
| Reversible, known files, no open decision | code-first: the change or a sketch, with the diff as the review artifact; `workflow: oneshot` |
| Trivial edits, lookups, answers from context | inline, no documents |

In a PRD, the Success section holds the A1..An criteria. Switch to a heavier step when a sketch exposes a consequential decision or the change keeps growing. When the user says to skip the workflow, implement directly. A conversational thread is no exception: when a chat request turns into code, docs or pull-request changes, start at step 1.

### 3. Trace every step to the criteria

- Each design question, TDD decision and outline phase names the criteria it serves. Question a phase that serves none.
- Before implementation, write the validation plan: for each criterion, the check, who runs it and when. Code-first work writes it in the change summary.
- During implementation, follow the matching playbook: [feature](../ayo/references/feature.md) for new or changed behavior, [refactoring](../ayo/references/refactoring.md) for structure, and [diagnostics](../ayo/references/diagnostics.md) for a bug or failed fix.

### 4. Verify against the outcome

- The final report is the criteria table: each criterion passed, failed, blocked or awaiting the user, with its evidence. Passing tests alone do not pass a criterion that needs more.
- Judgment calls stay awaiting the user until the user decides. Never weaken a criterion to match the result; record any change the user approves.

## Task directory

- Instead of `.agents/artifacts/<name>`, use the work item's `review/` folder in its owning workspace: `workspaces/<workspace>/work/<id>/review/` under the context root. Resolve the workspace through [first-task routing](first-task-routing.md), then run the [related-work check](context-routing.md#check-for-related-work) to decide whether to reuse an existing work entry or create one. A directory the user names still wins.
- If no workspace owns the directory, ask whether to register it, associate it with an existing workspace, or keep the documents session-only in chat.
- Never write RPI documents into a project repository or commit them there.
- Keep `NN-` numbering, the `repos` frontmatter and supporting mockups beside the documents, as RPI describes.
- Next-step commands name this directory.

## Work state

Use `index.md` for the chosen workflow, `review/` for its artifacts and the owner thread for pending questions. Check these sources to resume. Keep existing cursor fields only on legacy records.

| RPI flow | `workflow` |
| --- | --- |
| Design discussion | `rpi` |
| PRD, then TDD | `prd` |
| TDD only, or research only | `freeform` |
| No documents, from an accepted request | `oneshot` |

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

Launch on the route delegated execution names for the harness: T3 routing in T3 Code, Claude Code routing in Claude Code, and native children in Codex. RPI's "run independent investigations in parallel" stays within the policy's role and total caps.

## visual-pr

Use `visual-pr` only when the user asks for it by name. When RPI's handoff suggests `/visual-pr`, use the [pr](../pr/SKILL.md) skill instead and mention `visual-pr` as an option. When the user does ask for it, `visual-pr` writes the PR body from its template, with these overrides:

- Keep HumanLayer out of everything published: no HumanLayer task URLs, `.humanlayer` paths, app permalinks or credits in the PR title, body, commits or comments. Its header links only a public ticket or issue URL, or is omitted.
- Never put local paths or links to private context in the PR. Save the description draft as `pr-description.md` in the work item's `review/` folder, not under `.humanlayer/tasks`.
- Save any `show-me` HTML beside that draft and link it in chat as an ordinary file. Do not use `task-artifact` fences.
- The [pr](../pr/SKILL.md) skill owns branch, commit, push and creation permission, issue links, and the no-AI-attribution rule. `visual-pr` does not push or create a PR beyond what the user asked for.
- The final answer reports the real draft path in place of "cloud permalink from hook".
