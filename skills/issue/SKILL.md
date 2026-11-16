---
name: issue
description: "Capture a user request or hand off scoped implementation work to a local workspace issue or an authorized configured remote tracker."
---

# Issue

## Choose mode and destination

- **Request intake:** preserve a new bug, idea, or request and clarify user intent using the body below.
- **Implementation handoff:** queue, split, or transfer agreed work. Follow [implementation-handoff](implementation-handoff.md); its technical body replaces the intake body.
- **Destination:** use local workspace storage, GitHub, or another configured tracker. User phrases such as `/issue local`, `/issue github`, `split plan into local issues`, and `promote local issues` select skill behavior; they are not commands to parse or execute.

First check the outcome boundary under [projects and bounded work](../references/context-routing.md#projects-and-bounded-work). A long-lived goal with several independently verifiable outcomes belongs in `projects/<project-id>/`, with bounded issues/work linked beneath it. Reuse an existing project and tracker authority. Do not turn the umbrella goal into one oversized local issue or merge its child outcomes. Creating a project still requires authorized destination and scope; a project record grants no implementation or dispatch permission.

Before any create, the destination and workspace/repository scope must be explicit in the request or authorized by a workspace default. Otherwise ask before writing. Resolve remote project/repository ambiguity too. Once destination and scope are authorized, intake may create before follow-up questions. Drafting does not authorize publication, assignment, status changes, or implementation.

Read the workspace index's `Issue tracking` section for its approved destination, repository routing, and creation policy. Follow [workspace issue tracker setup](../references/context-routing.md#workspace-issue-tracker-setup) when the default is missing or deferred. Honor required draft review before creation; an explicit draft request never authorizes publication.

Use [write-issue](../write-issue/SKILL.md) for title and content standards. Its GitHub API, types, and labels apply only to GitHub mode; use the configured integration for another remote tracker. Local mode never runs tracker commands and requires no network, repository, plan, or work directory.

## Local issue record

Store a local issue at `~/.agents/context/workspaces/<workspace-id>/issues/<slug>.md`, where the slug is a short lowercase hyphenated form of the title (`skeleton-get-status-api.md`). Generate a stable collision-resistant `id` for the frontmatter (a UUID-derived value is sufficient). Check that the destination does not exist and never overwrite; on a collision, add a short suffix to the slug. A path-owned session must first have an authorized workspace association.

Use only metadata the issue needs:

```yaml
---
id: <stable-id>
title: <title>
type: bug | feature | example | task
status: open | started | done | dropped | promoted
priority: now | next | later
work: <link to the work item's state.md once started>
workspace: <workspace-id>
affected_repositories: [<stable repository identities when known>]
dependencies: [<issue-id or URL>]
source_plan: <optional link>
source_design: <optional link>
external_url: <set after successful promotion>
---
```

`title`, `type`, `status`, and workspace ownership are required. Affected repository identities and dependencies are required when relevant; omit optional links rather than inventing them. Do not invent assignments, estimates, or fields. Set `priority` only from the user's triage decision; leave it out until he sets one.

## Issue lifecycle

A local issue is backlog: work that has not started. When work starts, create the work item under [context routing](../references/context-routing.md), set the issue to `started` and link its `state.md` in `work`. From then on the work state owns progress, blockers and acceptance; the issue holds no `active` or `blocked` status of its own. When the work item completes, set the issue to `done`. Writing an [agent-pickup](../agent-pickup/references/packet.md) task packet counts as starting the work. An issue the user decides not to do becomes `dropped` with a one-line reason in the body. `promoted` marks an issue moved to a remote tracker under [implementation handoff](implementation-handoff.md).

Create a local issue only where no tracker owns the work. When a remote tracker owns it, the work item links the tracker key instead of a local copy.

## Request intake body

Start with the user's original description verbatim and keep the resulting readback and answers as the intent record:

```md
User: {user_description}

---

{two to five sentences reading back the problem, expected behavior, and scope}

## Open questions, when unresolved intent remains

1. **{question}**
   _Awaiting answer._

Readiness: {enough intent to proceed, or the specific missing decision}.
```

Keep the readback product-facing. Do not include paths, code snippets, diagnoses, or fix recipes unless requested. Ask only about unresolved user intent that affects the work; omit the question section when the request is sufficient. Investigate facts available from repositories or tools yourself. Mark a question `Critical:` only when work cannot begin without it. Replace answered placeholders, revise corrected framing, and mark a deferred non-critical answer `_Deferred by user; not blocking implementation._`. Never call an issue ready with a critical question open. Describe readiness plainly; do not invent a confidence percentage.

## Intake workflow

1. Confirm destination and scope authorization. Gather the description and perform only cheap destination-appropriate duplicate/triage checks.
2. Create the issue with the verbatim description, readback, any unresolved questions, and readiness. In remote mode, use only that tracker's supported metadata. In local mode, write the collision-safe record without network or tracker commands.
3. Read the saved issue back. Return its local path or remote URL, the readback, and open questions.
4. After each answer, update the owning issue, preserve prior answers, correct title/type/framing when needed, and read it back. Do not duplicate stable criterion IDs.
5. Stop when it contains enough intent to work or report the critical blocker.

For visual bugs, attach or embed supplied media only when the destination supports it and publication is authorized. Otherwise describe the visible evidence accurately; never claim an attachment exists when it does not.
