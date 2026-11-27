# Packets and entering the state

Read as the planning thread or the Desk when the user says "ready for agent" or "back to agent", and as a lane for your grants.

## Repository profiles

A repository takes agent tasks only when its workspace `index.md` has an `## Agent pickup` section with a profile for it. The profile holds everything that is the same for every task in that repository:

| Field | Meaning |
| --- | --- |
| T3 project | Project name and ID. Its root must be the repository root (`t3_project_read`). |
| Forge and account | Repository identity, forge, CLI account, SSH alias |
| Commit email | Expected `git config user.email` inside the worktree |
| Base | Explicit remote base ref, never inferred from `origin/HEAD` |
| Setup | Commands for a fresh worktree, and any ignored local files to copy from the main checkout |
| Checks | Local gates and hooks |
| Live verification | What counts as live evidence and its safety rules |
| Generated paths | Paths left out of size measurement, such as lockfiles |
| PR | Exact PR command, always without reviewers |
| Lane model | Implementation and review provider, model and effort |

Repository rules (`AGENTS.md`, verification skills) stay authoritative; the profile points at them.

## Task packet

Write `work/<id>/agent/packet.md` next to the task's work state. Link the accepted plan, issue or design; do not copy it. Follow [implementation handoff](../../issue/implementation-handoff.md): one vertically sliced, independently verifiable outcome that is executable without chat. When the task comes from a local issue, set the issue `started` and link the work state.

Record the context project and parent from [work metadata](../../references/context-routing.md#projects-and-bounded-work), or `none` when absent. These identify organization, separately from the T3 project in the repository profile and from execution dependencies. Populate them for new packets; changing an existing approved packet requires its normal fresh hash approval. Project creation, attention or linkage alone never starts a task or promotes its status.

```markdown
# Packet: <task title>

Approval: The user, <ISO time>, <thread link>, "<their words>", packet sha256 <hash of everything below the Approval line>
Project: <context project ID and index link, or none>
Parent: <parent work ID and state link, or none>
Repository: <profile link>; branch `<branch>`
Outcome: <one sentence>
Acceptance: <criteria IDs and text, or links with content hashes>; evidence: <what proves each>
Settled decisions: <links with content hashes>; open Critical questions: none
Scope: in <paths>; shared files <lockfiles, changelog>; out <exclusions>; estimate <N> changed lines
New tests: <approved scenarios, or "none beyond repairs">
Live verification: <profile checks that apply, payload, cleanup plan>
Dependencies: <work IDs and what each must deliver, or none>
Start window: any time | night window
Budget: 90 agent-minutes, 2 fix rounds (or the agreed values)
Withheld beyond the standard list: <task-specific limits, or none>

## Follow-ups
<appended entries: "Follow-up N (<date>): <reason and source link>">
```

Compute the hash with `sed '1,/^Approval:/d' packet.md | shasum -a 256`. Any edit below the Approval line needs a fresh approval.

## Grants

The user's approval of a packet grants, for that task only:

- commits on the task branch, and on stacked branches for dependent tasks, in the lane worktree;
- pushing those branches to `origin` without force;
- one PR per task with the profile's PR command, without reviewers; `link_pull_request` and `write_pull_request_guides` for it;
- running the profile's setup, checks and live verification, with network access for dependency installs;
- one delegated review per task and per follow-up.

Everything else is withheld, including the standard list in [stop rules](../SKILL.md#stop-rules-for-every-role). The packet may narrow grants and never widens them.

## Entry check

Run it before setting the state. The dispatcher runs it again before placing the task. Any failure keeps the task out of the state and tells the user which check failed.

| Check | How |
| --- | --- |
| Packet complete and approved | Every field filled; the Approval hash matches the current content |
| Context hierarchy | For new or revised packets, Project and Parent match the state and resolve in its workspace; preserve existing approval hashes until an authorized packet revision |
| Plan settled | Linked acceptance, plan, issue and design sources exist at their recorded hashes; missing or mismatched hashes fail this check; no open Critical question |
| Repository opted in | Profile present in the workspace `index.md` |
| Project is the repository | `t3_project_read` root equals the repository root |
| Base exists, branch free | `git ls-remote origin <base>` returns a ref; `git ls-remote origin <branch>` returns nothing (follow-ups excepted) |
| Forge access | GitHub: `GH_TOKEN="$(gh auth token --user <account>)" gh api repos/<repo> --jq .permissions.push` prints `true`. Bitbucket: `bb pr list` succeeds as the profile's account |
| Size | Estimate at most about 700 changed lines; otherwise split into dependent tasks first |
| Dependencies | Each is merged, `ready-for-agent`, or `active` in the same repository (otherwise the task may still enter; it waits) |

## Size limit

Nobody knows a change's size in advance. Estimate it from the plan: files and functions touched, tests added, similar past changes. Split anything above about 700 lines, because estimates run low. During the run the lane measures `git diff --shortstat <base>...HEAD -- . ':(exclude)<generated paths>'` after each commit and stops at 1000 changed lines (insertions plus deletions) with a partial result.

## Move a task into the state

1. Write or update the packet. Record the user's approval only from the user's actual words in this thread ("ready for agent" for this task); never infer it.
2. Run the entry check.
3. Set `status: ready-for-agent`, `next_action: "Waiting for an agent lane"`, `blocker: ""`, `brief_attention: []` and a fresh `brief_checked_at`, under the [checkpoint rules](../../references/work-lifecycle.md#recognize-when-to-save). Commit the context change.
4. Wake the dispatcher: `run_scheduled_task_now` with the dispatch schedule ID from `runtime.md`. If T3 answers that the task is already running, send `t3_thread_send` to the dispatcher thread instead, mode `queue`, `clientRequestId` `pickup-<workspace>-<work-id>-<n>`.
5. Tell the user the task is ready, its start window, and where results will appear.

"Back to agent" on a task in `needs-review` appends a follow-up entry and sends it to the owning lane thread (the work state's `owner_thread`) with `t3_thread_send`, mode `queue`. The lane moves the task to `active` itself. Withdrawing an unstarted `ready-for-agent` task sets `status: draft` and wakes the dispatcher so it drops the task from any lane queue. For a stopped task owned by a lane, send the user's withdrawal and its source to `owner_thread`; the lane records the decision, updates the state and notifies the dispatcher. The mover does not edit that lane-owned state.
