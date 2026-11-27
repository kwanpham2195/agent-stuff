---
name: desk
description: "Run a T3 Code thread as the user's Desk: start work, answer what needs the user, triage, and change rules. Use when a thread is set up as the Desk."
---

# Desk

The Desk is optional. It coordinates work spanning workspaces and handles intake when the work has no owning main thread yet.

The Desk runs only in T3 Code. Confirm the session under [confirm the current session](../delegated-execution/references/t3-routing.md#confirm-the-current-session). Outside T3, or when the thread is not set up as the Desk, tell the user the Desk currently runs only in T3, handle the request as ordinary direct work, and stop reading this skill.

On start or resume, read the [Desk work record](#desk-work-record) and the workspace routing in [context routing](../references/context-routing.md).

## Intake

Pick the route by what the user asks for.

- **Quick question:** answer it. Anything that changes files in a project goes to a task thread.
- **Real work to start now:**
  1. Launch a thread only when the user asks. Pick the workspace and the launch checkout’s T3 project. Use `t3_project_list` to find it. Separately route a multi-outcome goal under [context projects](../references/context-routing.md#projects-and-bounded-work), with bounded child work. Context project identity does not select a checkout.
  2. Run the [related-work check](../references/context-routing.md#check-for-related-work). If it finds the same outcome, send the request to that record's owner thread, or relaunch from that record, instead of creating a new one. Otherwise create `workspaces/<ws>/work/<id>/index.md` within the configured context root. Keep it to one page. Use [work metadata](../references/context-routing.md#work-metadata-and-overview), including `project` for project work and `parent` for a sub-issue. Link the child from its project index or grouping view without changing project/work status by association.
  3. Check open work indexes with `owner_thread` and running or waiting threads from `t3_thread_list`. If another thread is writing in the checkout, ask the user before launching into it. Shared checkouts share files, the Git index and the branch. Launch a task thread in that project with `t3_thread_launch`. Set `workspaceStrategy` explicitly to the checkout the user approved. Choose the model using [model policy](../delegated-execution/references/model-policy.md) and pass it as `modelSelection`. Keep the returned thread ID. `t3_thread_launch` has no retry key, so after an error or lost response, check `t3_thread_list` before launching again.
  4. Give the owner a short brief with links. Include the outcome, acceptance evidence, checkout, authorized stages, human gates and artifact locations. It tells the thread to talk to the user directly, ask its questions in the thread, use the work index and decision records, and do the closeout memory step in [work lifecycle](../references/work-lifecycle.md#preserve-reusable-project-knowledge) when it finishes. Facts that need real investigation go to the task thread as its first stage, not to the Desk.
  5. If the work has its own thread, link it in `owner_thread`. Set `workflow` when a flow applies. Give the user the thread link returned by T3.
- **Real work for later:** route project-sized goals through [projects and bounded work](../references/context-routing.md#projects-and-bounded-work); file bounded requests with [issue](../issue/SKILL.md) in `workspaces/<ws>/issues/`, or the workspace's tracker when one owns the work. Set `priority` only if the user gave one.
- **No workspace fits:** ask the user the registration questions in [context routing](../references/context-routing.md): create a workspace, attach the directory to an existing one, or continue without registering; for a new workspace, also where its issues live. A new workspace gets `workspaces/<ws>/index.md` and an entry in `~/.agents/context/index.md`. Then route the request.

If the project or checkout is unclear, ask before launching.

## Size the work

Pick a flow from what the user asked for, using the [RPI flow](../references/rpi-local.md#work-state) names, and record it in the work index’s `workflow` field. Ask only when the choice changes cost or gates.

| Size | Flow | Typical shape |
| --- | --- | --- |
| Small | `oneshot` | The task thread makes the change itself, verifies it and delivers. `freeform` when the user picks the stages. |
| Medium | `rpi` | Questions and research, design, outline, phases, verify, deliver |
| Large | `prd` | Research, PRD, technical design, outline, phases, deliver |

A quick fix with no artifacts needs no flow. The task thread runs the flow and owns its artifacts; size never relaxes permissions or acceptance.

For a selected flow, the launch brief must explicitly tell the task owner to load the `rpi` entry and [RPI local rules](../references/rpi-local.md), naming the selected flow, starting stage and authorized range. Supply resolved absolute skill paths in the launch packet. Use the active harness's explicit invocation when supported, or an explicit instruction to read the entry at that path. A `workflow` field records selection; it does not load instructions. The task owner reconciles existing inputs before starting that stage. Ordinary saved-plan format reuse follows [work lifecycle](../references/work-lifecycle.md#saved-planning-artifacts) and does not select a flow.

## Name threads

Name task threads `<Action> [#issue]: <short subject>`, with the action one of Discuss, Research, Plan, Implement, Review, Verify or Fix. Use the tracker's real key and leave the issue part out when there is none. Leave out model names, status and dates unless two otherwise identical tasks need telling apart. Examples: `Implement #123: Input references`, `Research: Retry behavior`.

RPI stages map to actions: questions and research → Research; design, PRD and TDD → Discuss; outline → Plan; an implementation phase → Implement with the phase (`Implement #123: Phase 2 schema`); independent review → Review; verification → Verify.

The Desk thread is `Desk`. Schedule titles follow the same pattern, because each scheduled run's thread takes its schedule's title. A title the user sets wins.

## What needs me?

Read open work indexes and follow their `owner_thread` links when present. Include running and waiting threads from `t3_thread_list` within the authorized scope. List questions and approvals still waiting on the user, including those in the Desk thread. Report unreadable sources as coverage gaps. Add open issues with `priority: now` under their existing issue scope. Answer in at most five lines with links.

Never message or wake a task thread to ask for status.

## Triage

When the user asks to triage, run [triage-work](../triage-work/SKILL.md) against the Context Home board, one item at a time. Work items end as continue, close or park. Issues end as a priority (`now`, `next`, `later`), dropped with a reason, or started: starting follows the "start now" route, then set the issue to `started` and link the new `index.md` in its `work` field. Apply changes only to the item the user decided on. When a work item that came from an issue completes, set that issue to `done`.

## Rules broadcast

Only when the user asks to change a rule for running work, send one short message to each running or waiting task thread. Find their links in open work indexes with `owner_thread` and confirm live status with `t3_thread_list`. Use `t3_thread_send` with a stable `clientRequestId` for each thread. Ask for no acknowledgment. Before retrying an uncertain send, check the thread for the message. A rule that should outlast the running threads goes into `AGENTS.md` or the skill that owns it; the broadcast only tells running threads.

## Desk work record

Use the Desk work index for its goal and source links, including scheduled brief contracts. Keep pending questions in the Desk thread. An existing legacy Desk record keeps its current owner until converted.

## Scheduled briefs

The user may schedule briefs on the Desk, each with its own written contract. Optional briefing skills, such as `morning-brief` or `weekly-review`, are not part of this repository. Each run uses a fresh thread (`bindToCurrentThread: false`). Keep each job within its contract. Change a schedule or the contract only when the user asks. List the scheduled tasks before a change, update the existing task, and verify the ID, cadence, and next run afterward. Do not create a replacement job to change a setting.

## Limits

- No project implementation, research, or review. Task threads do that.
- No polling, watchers, or background observation.
- Create a new top-level thread only when the user asks for one.
- Task threads answer to the user in the T3 inbox. For a status request, the Desk reads open work indexes with `owner_thread` and running or waiting threads from `t3_thread_list`.
- the user can talk to any task thread directly, and does not need the Desk to relay.
