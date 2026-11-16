---
name: desk
description: "Run a T3 Code thread as the user's Desk: start work, answer what needs the user, triage, and change rules. Use when a thread is set up as the Desk."
---

# Desk

The Desk is one T3 Code thread that the user uses as a front door. The user starts work, asks "what needs me?", triages the backlog, and changes rules here. The Desk never does project work and never receives reports. There is no chain of command to follow.

Periodic workflow checks belong to an explicitly assigned [scrum master](../scrum-master/SKILL.md). That role may nudge task owners under its monitoring contract; it does not take over Desk intake, priorities or task execution. The Desk's no-polling and no-status-message rules remain unchanged.

The Desk runs only in T3 Code. Confirm the session under [confirm the current session](../delegated-execution/references/t3-routing.md#confirm-the-current-session). Outside T3, or when the thread is not set up as the Desk, tell the user the Desk currently runs only in T3, handle the request as ordinary direct work, and stop reading this skill.

On start or resume, read the Desk's own state (see [Desk state](#desk-state)) and the workspace routing in [context routing](../references/context-routing.md).

## Intake

Pick the route by what the user asks for.

- **Quick question:** answer it. Anything that changes files in a project goes to a task thread.
- **Real work to start now:**
  1. Pick the workspace and the launch checkout's T3 project. Use `t3_project_list` to find it. Separately route a multi-outcome goal under [context projects](../references/context-routing.md#projects-and-bounded-work), with bounded child work. Context project identity does not select a checkout.
  2. Run the [related-work check](../references/context-routing.md#check-for-related-work). If it finds the same outcome, send the request to that record's owner thread, or relaunch from that record, instead of creating a new one. Otherwise create `workspaces/<ws>/work/<id>/agent/state.md` within the configured context root. Keep it to one page. Use [work metadata](../references/context-routing.md#work-metadata-and-overview), including `project` for project work and `parent` for a sub-issue. Link the child from its project index or grouping view without changing project/work status by association.
  3. If a non-complete state file shows another task thread writing in that checkout, ask the user before launching; separate threads share files, the Git index and the branch. Launch a task thread in that project with `t3_thread_launch`. Set `workspaceStrategy` explicitly to the checkout the user approved. Never create worktrees; only the [agent-pickup](../agent-pickup/SKILL.md#worktree-exception) dispatcher does, for its lanes. Immediately before launch, resolve `task-research` or `task-implementation` under [model policy](../delegated-execution/references/model-policy.md), or the specialist role for review/advisor work regardless of thread level. Use the resolver's `--operation t3_thread_launch` native `modelSelection`, record source/key and hashes, and compare returned settings. Check authority and budgets separately. Keep the returned thread ID. `t3_thread_launch` has no retry key, so after an error or lost response, check `t3_thread_list` before launching again.
  4. The brief is a short launch packet with links, not copied policy: the outcome and how the user will accept it; workspace, repository and checkout; the flow and the stages the user authorized; the human gates; where the state and artifacts live. It tells the thread to talk to the user directly, ask its questions in the thread, keep its state to one page (history goes to `agent/history.md`), and do the closeout memory step in [work lifecycle](../references/work-lifecycle.md#preserve-reusable-project-knowledge) when it finishes. Facts that need real investigation go to the task thread as its first stage, not to the Desk.
  5. Add the thread link to the state file. When a flow applies, also add `workflow`, `workflow_stage`, `current_artifact` and `owner_thread` together, as [workflow records](../references/context-routing.md#workflow-records) requires (`workflow_stage: intake` and `current_artifact: ""` at the start). Give the user the link: `[title](t3-thread://v1/<threadId>)`.
- **Ready for agent:** when the user says "ready for agent" (or "back to agent") for planned work, follow [agent pickup packets](../agent-pickup/references/packet.md#move-a-task-into-the-state). A task without a packet goes to its planning thread first. "What is waiting for agents?" reads `ready-for-agent` work states and the agent-pickup lane ledger only.
- **Real work for later:** route project-sized goals through [projects and bounded work](../references/context-routing.md#projects-and-bounded-work); file bounded requests with [issue](../issue/SKILL.md) in `workspaces/<ws>/issues/`, or the workspace's tracker when one owns the work. Set `priority` only if the user gave one.
- **No workspace fits:** ask the user the registration questions in [context routing](../references/context-routing.md): create a workspace, attach the directory to an existing one, or continue without registering; for a new workspace, also where its issues live. A new workspace gets `workspaces/<ws>/index.md` and an entry in `~/.agents/context/index.md`. Then route the request.

If the project or checkout is unclear, ask before launching.

For every new general task, classify its difficulty under [model policy](../delegated-execution/references/model-policy.md#general-top-level-tasks), report the reason, and pass `--difficulty` to the resolver before launch. Complete explicit task/model/account choices and existing workspace/project defaults retain precedence. Specialist assignments use their own role selection. Do not reuse a previous item's classification, model approval or scope just because the conversation continues; choosing a task candidate does not change the current parent model or grant another launch.

## Size the work

Pick a flow from what the user asked for, using the [RPI flow](../references/rpi-local.md#work-state) names, and record it in the state's `workflow` field. Ask only when the choice changes cost or gates.

| Size | Flow | Typical shape |
| --- | --- | --- |
| Small | `oneshot` | The task thread makes the change itself, verifies it and delivers. `freeform` when the user picks the stages. |
| Medium | `rpi` | Questions and research, design, outline, phases, verify, deliver |
| Large | `prd` | Research, PRD, technical design, outline, phases, deliver |

A quick fix with no artifacts needs no flow. The task thread runs the flow and owns its artifacts; size never relaxes permissions or acceptance.

For a selected flow, the launch brief must explicitly tell the task owner to load the [RPI entry](../rpi/SKILL.md) and [RPI local rules](../references/rpi-local.md), naming the selected flow, starting stage and authorized range. Supply resolved absolute skill paths in the launch packet. Use the active harness's explicit invocation when supported, or an explicit instruction to read the entry at that path. A `workflow` field records selection; it does not load instructions. The task owner reconciles existing inputs before starting that stage. Ordinary saved-plan format reuse follows [work lifecycle](../references/work-lifecycle.md#saved-planning-artifacts) and does not select a flow.

## Name threads

Name task threads `<Action> [#issue]: <short subject>`, with the action one of Discuss, Research, Plan, Implement, Review, Verify or Fix. Use the tracker's real key and leave the issue part out when there is none. Leave out model names, status and dates unless two otherwise identical tasks need telling apart. Examples: `Implement #821: Insight input references`, `Research: Wrapper retry behavior`.

RPI stages map to actions: questions and research → Research; design, PRD and TDD → Discuss; outline → Plan; an implementation phase → Implement with the phase (`Implement #821: Phase 2 schema`); independent review → Review; verification → Verify.

The Desk thread is `Desk`. Schedule titles follow the same pattern, because each scheduled run's thread takes its schedule's title. A title the user sets wins.

## What needs me?

Read canonical non-complete project and work owners using [brief reporting fields](../references/context-routing.md#brief-reporting-fields), including the Desk's own published decisions. Follow that contract's project-index discovery and question ownership; exclude archives and duplicate navigation owners. Missing, unreconciled or conflicting reporting is Coverage, not a guessed ask or proof nothing is pending. Preserve old valid unanswered asks with their checked date. Add open issues with `priority: now` under their existing issue scope. Answer in at most five lines, each with a link to its owning project index or work state and, when known, its thread; group Coverage gaps if needed. Mention that threads waiting on the user are in the T3 inbox.

Read designated metadata from project indexes and work states only. Never message or wake a task thread to ask for status.

## Triage

When the user asks to triage, run [triage-work](../triage-work/SKILL.md) against the Context Home board when one exists, otherwise the open work notes, one item at a time. Work items end as continue, close or park. Issues end as a priority (`now`, `next`, `later`), dropped with a reason, or started: starting follows the "start now" route, then set the issue to `started` and link the new `state.md` in its `work` field. Apply changes only to the item the user decided on. When a work item that came from an issue completes, set that issue to `done`.

## Rules broadcast

Only when the user asks to change a rule for running work, send one short message to each active task thread named in the state files, using `t3_thread_send` with a stable `clientRequestId` for each thread. Ask for no acknowledgment. Before retrying an uncertain send, check the thread for the message. A rule that should outlast the running threads goes into `AGENTS.md` or the skill that owns it; the broadcast only tells running threads.

## Desk state

`~/.agents/context/workspaces/<workspace-id>/work/desk/agent/state.md`, one page:

- open decisions for the user, each with a link;
- the scheduled briefs and a link to their contract;
- links to anything else the Desk must find after a restart.

Follow [checkpoint retention](../references/work-lifecycle.md#checkpoint-before-context-is-lost) for state and history, and update only the Desk's own files.

## Scheduled briefs

The Desk owns the morning brief, Mac inspection and memory dream schedules, plus their contracts. Each run uses a fresh thread (`bindToCurrentThread: false`). Project attention follows the designated fields in [brief reporting](../references/context-routing.md#brief-reporting-fields); other source/write scopes stay in each job's contract. Change a schedule or the contract only when the user asks. List the scheduled tasks before a change, update the existing task, and verify the ID, cadence, and next run afterward. Do not create a replacement job to change a setting.

## Limits

- No project implementation, research, or review. Task threads do that.
- No polling, watchers, or background observation.
- No new top-level threads except task threads for intake the user approved.
- No reports routed through the Desk. Task threads answer to the user in the T3 inbox, and the Desk reads state files when asked.
- The user can talk to any task thread directly, and does not need the Desk to relay.
