---
name: issue
description: "Capture a user request or hand off scoped implementation work to a local workspace issue or an authorized configured remote tracker."
---

# Issue

## Choose mode and destination

- **Request intake:** preserve a new bug, idea, or request and clarify user intent using the body below.
- **Implementation handoff:** queue, split, or transfer agreed work. Follow [implementation-handoff](implementation-handoff.md); its technical body replaces the intake body.
- **Destination:** use local workspace storage, GitHub, or another configured tracker. User phrases such as `/issue local`, `/issue github`, `split plan into local issues`, and `promote local issues` select skill behavior; they are not commands to parse or execute.

Before any create, the destination and workspace/repository scope must be explicit in the request or authorized by a workspace default. Otherwise ask before writing. Resolve remote project/repository ambiguity too. Once destination and scope are authorized, intake may create before follow-up questions. Drafting does not authorize publication, assignment, status changes, or implementation.

Use [write-issue](../write-issue/SKILL.md) for title and content standards. Its GitHub API, types, and labels apply only to GitHub mode; use the configured integration for another remote tracker. Local mode never runs tracker commands and requires no network, repository, plan, or work directory.

## Local issue record

Store a local issue at `~/.agents/context/workspaces/<workspace-id>/issues/<issue-id>.md`. Generate a stable collision-resistant ID (a UUID-derived value is sufficient), check that the destination does not exist, and never overwrite on collision. A path-owned session must first have an authorized workspace association.

Use only metadata the issue needs:

```yaml
---
id: <stable-id>
title: <title>
type: bug | feature | example | task
status: open | active | blocked | done | promoted
workspace: <workspace-id>
affected_repositories: [<stable repository identities when known>]
dependencies: [<issue-id or URL>]
source_plan: <optional link>
source_design: <optional link>
external_url: <set after successful promotion>
---
```

`title`, `type`, `status`, and workspace ownership are required. Affected repository identities and dependencies are required when relevant; omit optional links rather than inventing them. Do not invent assignments, estimates, or fields. Closing as `done` requires the workflow's evidence and authorization.

## Request intake body

Start with the user's original description verbatim and keep the resulting readback and answers as the intent record:

```md
User: {user_description}

---

{two to five sentences reading back the problem, expected behavior, and scope}

## Open questions

1. **{question}**
   _Awaiting answer._

Confidence: {n}%, {ready_status}.
```

Keep the readback product-facing. Do not include paths, code snippets, diagnoses, or fix recipes unless requested. Ask only about user intent or context, not facts available from repositories or tools. Mark a question `Critical:` only when work cannot begin without it. Replace answered placeholders, revise corrected framing, and mark a deferred non-critical answer `_Deferred by user; not blocking implementation._`. Never call an issue ready with a critical question open. Confidence describes intake sufficiency, not implementation confidence.

## Intake workflow

1. Confirm destination and scope authorization. Gather the description and perform only cheap destination-appropriate duplicate/triage checks.
2. Create the issue with the verbatim description, readback, open questions, and confidence. In remote mode, use only that tracker's supported metadata. In local mode, write the collision-safe record without network or tracker commands.
3. Read the saved issue back. Return its local path or remote URL, the readback, and open questions.
4. After each answer, update the owning issue, preserve prior answers, correct title/type/framing when needed, and read it back. Do not duplicate stable criterion IDs.
5. Stop when it contains enough intent to work or report the critical blocker.

For visual bugs, attach or embed supplied media only when the destination supports it and publication is authorized. Otherwise describe the visible evidence accurately; never claim an attachment exists when it does not.
