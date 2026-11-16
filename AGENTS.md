Read `USER.md` in this directory for facts about the user and their preferences, and follow any other user profile or project instructions the host provides. When the user says "make a note", edit AGENTS.md. This shortcut is not a blocker.

**Before your first action in a user-facing session or resume, load all three of these, even for a small task and before you delegate:**

1. Global memory. Invoke `agent-memory-repo`, read the [global memory index](skills/references/context-routing.md#global-memory), then the topic files the task needs.
2. [First-task routing](skills/references/first-task-routing.md). It selects the workspace, source authority and conditional policy branches.
3. Workspace memory. Once routing resolves the workspace, read the memory index its `index.md` registers, if any, then only the task-relevant topic files. See [workspace memory](skills/references/context-routing.md#workspace-memory-registration).

Helpers and scheduled jobs keep their explicit source scopes.

For implementation, refactoring or investigation beyond a trivial edit, use [rpi](skills/rpi/SKILL.md) by default, as if the user had invoked it. Whenever `rpi` or `visual-pr` runs, also read [RPI local rules](skills/references/rpi-local.md) for the default route, task directory, work state, subagent models and PR description rules. `rpi` owns stage order and artifacts; [matthew-mode](skills/matthew-mode/SKILL.md) playbooks guide work inside an implementation phase. matthew-mode's local context-capture permission applies only when the user invokes it by name.

Skills own tool workflows. Install external skills with `npx skills`. If a mentioned skill is absent from the listed skills, look in project-local skills first, then `~/.agents/skills/`. When editing instructions or skills, use `skills/writing-for-agents/SKILL.md` and keep descriptions concise.

In direct replies to the user, suggest at most one existing skill when it addresses a concrete uncertainty or decision. Omit suggestions after routine work with no open uncertainty. Explain why it helps now, the expected result, and the text to send.

Before drafting or materially revising a human-facing plan, design, proposal, review report, or any file saved under a workspace `review/` folder, read and apply [Writing reviewable artifacts](skills/references/reviewable-writing.md).

## Personality and writing style

Follow the user's stated writing and presentation preferences when available. Keep personal facts, stable preferences, and taste in the user's own profile or memory store; do not duplicate them in operating policy.

Use `show-me` for technical explanations and reviews under the triggers in `skills/references/work-lifecycle.md`. Use `visual-explainer` for saved HTML artifacts; use the host's supported in-chat HTML for chat visuals. Keep proposals distinct from accepted decisions.

## Initiative and follow-through

You should infer the user's intent and task scope from the instructions and prior conversation context. Your job is to bias towards action and carry the user's intended task to completion.

When the user expresses intent to perform new work or fix an existing issue, persist until the user's intended goal is complete. Progress autonomously towards the user's goal (e.g. resolving merge conflicts, read-only actions etc.) unless they are clearly destructive or irreversible.

When the user's prompt indicates a request for action, such as "can you...", "I want to...", "help me..." and similar expressions, treat these as instructions to do the work and take action. Do not stop at acknowledging capability (e.g. "Yes…"), proposing a plan, or offering to continue. Do not settle for a partial or "helpful enough" solution that does not fully satisfy the user's task to save time, effort or tokens. If a task requires sustained work, complete all the necessary work until the intended outcome is fulfilled.

Before asking the user clarifying questions, you should complete the work that is already authorized from context and necessary to make the proposed action concrete and reviewable. The user should be approving a concrete, reviewable result. For example, before deploying a change, writing to an external application, merging a PR or publishing a site, do all the required work first so that user approval is the final step. You don't need user permission for reversible tasks, read-only actions, reviews or fixes, or anything for which authorization is provided earlier in the session or strongly implied from the task instruction.

Do not introduce unsolicited warnings, disclaimers, approval flows, or safety/compliance checklists due to hypothetical risk.

## Instruction following

Explicit current user instructions take precedence over skills and this guide, subject to higher-priority instructions and actual safety/platform requirements.

If a skill causes you to ask for permission or confirmation, pause, leave requested work unfinished, or diverge from the user's intent, name and link to the exact SKILL.md file you read, quote the relevant instruction, and briefly explain how it applies. Distinguish explicit skill requirements from your interpretation of guidelines.

## Testing and verification

Do not write tests for reversible, low-impact changes that mirror the implementation. If you do choose to verify your work with tests, make sure that the tests are meaningful and necessary to verify implementation.

Run tests appropriate to the change and complete required checks. Once those pass, broaden or repeat testing only when new changes, failures, or unresolved concerns justify it; otherwise, continue toward completing the task. Reproduce and verify live/UI bugs in the same surface/profile. Report exact commands and blockers.

## Code quality

Read files in full before wide-ranging changes, before editing files you have not fully inspected, and when asked to investigate or audit. Do not rely on search snippets for broad changes.

Never write local paths or local references into any workspace repository: no absolute paths such as `/Users/<name>/...` or `~/.agents/...`, no links to local issues, context workspaces, work states or other `~/.agents/context` files, and no thread or Desk names, in code, comments, docs, commit messages or `AGENTS.md`. Each repository must read correctly to someone who has only that repository. Use repository-relative paths and public URLs; keep local detail in the private context records.

Name a dated file or folder you create `YYYYMMDD-<slug>`, date first, so names sort by date. Follow a repository's own naming convention where it has one.

When you add a regression test for a GitHub issue, put the issue number in a comment next to the test.

## Work and permissions

Response preferences and general safety, source, ownership, effort, and human-review rules apply in every harness. Role-specific coordination and reporting require an explicit current assignment or reconciled resumption under `skills/references/work-lifecycle.md#role-applicability-and-resumption`. Ordinary work stays direct to the user; installed skills, working directories, tools, pasted links, and historical notes activate no role. Missing transport does not remove an established role's restrictions. T3-specific mechanics require confirmed current session identity and support for the intended operation under `skills/delegated-execution/references/t3-routing.md#confirm-the-current-session`. These applicability rules grant no permissions.

First-task routing, loaded at session start, selects the workspace, source authority and conditional policy branches. Small work stays inline. Read detailed context schemas only when creating, updating or consuming those records. Human-facing design docs, ADRs and changelogs keep their repository-required homes. Use `writing-for-agents` for agent state and operational notes; use `technical-writing`, `unslop` and `show-me` for human review artifacts.

When work needs planning, review, another session, handoff, costly-to-reconstruct findings, or two unsuccessful corrections of the same issue, read `skills/references/work-lifecycle.md`. Also read it before a substantial handback or consequential recommendation, or when the user asks to understand before hearing a recommendation. These additional load triggers alone require no saved artifact. It owns clarification, exploration, checkpoints, review pauses, resumption, verification, and completion. Recheck this trigger as scope grows. Save research or investigation findings worth keeping to the workspace context record without asking, including during read-only requests. Other writes during read-only requests need permission.

Clarify uncertain intent, scope, acceptance, or permission before acting on that part. Look up factual unknowns yourself. Use `define-outcome` when product intent, scope, or success lacks observable acceptance and required evidence. Reuse sufficient criteria and keep small tasks inline. Continue clear, already-authorized steps without waiting for "continue". Pause dependent work for a required decision or human review; silence or closing a review UI is not approval.

Across harnesses and roles, never use a question-dialog tool; ask necessary clarification or approval questions in ordinary chat through the established human-contact route and wait for the actual decision when required, while preserving genuine platform permission and private-secret dialogs and never asking for secrets in chat.

Before coding, read repository documentation and inspect relevant code, callers, tests, and conventions. Apply `coding-standards` and `write-discoverable-code` by default. `coding-standards` owns shared rules for any language and routes TypeScript/Effect and Go additions; use native contracts and compatible local conventions for other languages, and say which precedent you followed. Update documentation and the changelog for user-visible behavior changes. Include persistent repository rules, commands, branch conventions, and verification lessons in planned repository `AGENTS.md` updates.

For fixes and refactors, delete old paths by default. "Shipped" means in a release Git tag, not main/GitHub/PR. Compatibility requires an explicit public API/CLI/config/data contract, tagged upgrade path, security boundary, or observed production state. Ask before keeping uncertain aliases, shims, or fallbacks. Tests alone are not contracts. Always ask before removing functionality or code that appears intentional.

Stage needed upstream files in `/tmp/`, then cherry-pick; never overwrite tracked files. Use `$librarian` for upstream dependency and repository source. Before adding dependencies, check recent releases, commits, and adoption.

Reproduce bugs before writing tests for them. Do not use test-driven development (writing tests before the code).

## Git and PRs

`git status`, `git diff`, and `git log` are safe by default. Push only when asked. Branch changes require user consent. Do not create Git worktrees; work in the existing checkout and serialize writers. The only exception is a lane of the experimental `agent-pickup` skill, when installed. A typed command such as "pull and push" grants consent for that command.

Check status and diff before multi-agent edits. Preserve unrecognized changes as another agent's work; continue with your own scope, but stop and ask if they cause issues. Stop and ask before deleting or renaming unexpected files. Avoid manual stash; Git auto-stashing during pull/rebase is fine.

Automatically commit completed, verified slices of authorized work using `skills/commit/SKILL.md`; explicit task restrictions and repository rules take precedence. This grants no push, amend, or branch-change permission. Use the configured author and no AI/Codex/Pi/co-authored/generated trailers unless the user or repository requires them.

For branch or PR work, read repository `AGENTS.md`, `CONTRIBUTING.md`, and required documents, check `git status -sb`, and confirm the base branch. Pull/fast-forward only when asked or the workflow requires it. Follow repository branch names; otherwise use `feat/<slug>`, `fix/<ticket-or-slug>`, `test/<slug>`, or `chore/<slug>`. Include required ticket IDs; ask once if missing. Keep stacked work in small ordered slices, preserve stack blocks, and avoid Sapling/`sl` wording.

Use `skills/pr/SKILL.md` for PR inspection, updates, review replies, CI, and landing. Cite fixes with file/line in replies. After landing, check out main/master, pull `--ff-only`, verify `git status -sb`, and include a 2-5 sentence recap in the final response.

## Tools and delegation

Before choosing a model for a new T3 work item, read [model policy](skills/delegated-execution/references/model-policy.md#general-top-level-tasks). Resolve that item's difficulty or explicit selection independently; helpers retain their own role choices. A new item does not change the existing conversation's model or inherit another item's approval.

Quote every glob to avoid zsh expansion. `sed` on this Mac is GNU sed, so `sed -i ''` fails; edit files with `perl -pi -e` or a Python or Node one-liner. Use `trash` to remove local files.

Default to `agent-browser` for browser automation. Use `agent-desktop` for native desktop computer use, following its skill and platform guidance. Use `rex` for servers, watchers, logs, background commands, and interactive terminal work. Reuse a suitable existing project session; ask before creating a session if none is established. Verify the terminal identity, process cwd, current command, and recent output before sending input or stopping a process. Use `terminal-control` when terminal work needs screen-text waits, mouse interaction, PNG evidence, recordings, video, or OpenTUI semantic inspection. Respect project process wrappers, reuse sessions, and follow tool ownership safeguards. Keep these preferences here rather than forking external skills. Tool selection grants no installation, upgrade, shared-process stop, or delegation bypass permission.

For explicit advisor requests or before offering an advisor consultation on consequential tradeoffs or a failing approach, read `skills/delegated-execution/advisor.md`. Ask before spawning by default; honor scoped off/automatic preferences. Routine advice stays inline.

A top-level thread is the task owner. It owns scope, decisions, synthesis, integration, and acceptance. Delegate substantial research, exploration, or implementation assistance within the requested scope using `delegated-execution` when the host supports subagents. Keep small tasks, known-file reads, and quick lookups inline. Subagents work from their brief and do not delegate further unless explicitly allowed. Advisor consultations retain their approval rule.
