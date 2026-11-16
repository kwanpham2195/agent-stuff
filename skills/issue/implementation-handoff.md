# Implementation handoff to an issue destination

Use when the user asks to queue, split, or transfer scoped work for later implementation. Read [work-lifecycle](../references/work-lifecycle.md), the destination rules in [issue](SKILL.md), and [write-issue](../write-issue/SKILL.md). This mode includes technical context; request-intake restrictions on implementation breadcrumbs do not apply.

## Prepare and split

- Confirm an explicit or authorized-default local/remote destination and workspace/repository scope before creating anything. Inspect existing destination records for duplicates and ownership using destination-appropriate operations.
- Read the accepted plan, owning decisions, relevant evidence, and existing issues. Reuse earlier sufficient research rather than repeating ceremonies.
- Split a large plan into independently assignable and verifiable outcomes, not every implementation step. A workspace may span repositories; name affected repository identities and explicit dependencies.
- For a project-sized goal, follow [project routing](../references/context-routing.md#projects-and-bounded-work). Keep the project backlog, cross-work decisions and references with their project owner. Set `project` on each started work item and `parent` on sub-issues; organization links do not replace explicit dependencies or authorize starting work.
- The plan owns overall sequencing and decisions. Each issue owns only its scope, criteria, dependencies, and status. An execution checkpoint owns evidence and next action only when needed. Do not maintain a duplicate issue-status list in the plan.
- Preserve approval state and unresolved decisions. A proposed plan is not authorization to implement or publish.

## Choose issue boundaries

Prefer vertical slices: each issue delivers observable behavior and includes the UI, API, persistence, and checks that behavior requires. Split by user action, business rule, supported input, permission, or failure handling when those boundaries yield separately verifiable outcomes. Use technical prerequisites as separate issues when they unblock several slices or require independent migration or rollout; give each a measurable completion condition.

- Start from the plan's acceptance criteria. Map each in-scope criterion to an issue; identify any uncovered criteria or overlapping ownership before creation.
- Size by outcome and verification, without a fixed ticket count or duration. Split an issue when it contains outcomes that can ship separately. Keep implementation steps as checklist items when they have no useful independent completion evidence.
- For each dependency, name the result or contract the next issue needs. Show which issues can start immediately and which can run in parallel after prerequisites pass. Resolve dependency cycles by revising boundaries or extracting a shared prerequisite.
- When an unresolved design question determines the breakdown, propose a bounded investigation with a question, required evidence, and decision to unblock. Keep dependent implementation issues provisional.
- Check that one owner can implement and demonstrate each issue after its declared dependencies are satisfied, without reconstructing the original chat.

Example for an accepted CSV import plan, assuming duplicate handling and background processing can build independently on the basic import:

```text
A. Import a valid CSV and show created records
   ├── B. Preview validation errors before importing
   ├── C. Detect duplicates and let users choose a resolution
   └── D. Process large imports asynchronously
          └── E. Cancel an import and report partial results
```

Each connecting line means the child depends on the parent's result. The example is a proposed breakdown, not additional product requirements; derive actual issues and dependencies from the accepted scope and contracts.

For a requested breakdown review, return proposed titles, outcomes, criterion references, required evidence, dependencies, and unresolved decisions. Pause for the requested approval before creating issues.

## Make each issue executable without chat

Include outcome, rationale, scope, exclusions, approval status, affected repositories, explicit dependencies, and only assigned/authorized ownership. Add focused technical paths and contracts, labeling hypotheses and unverified behavior. Reference stable acceptance criterion IDs from their authority without copying or renumbering them; state required evidence and distinguish checks already run from proposed checks. Link the authoritative plan/design/research when accessible.

For a remote recipient, ensure essential sources are accessible: embed concise shareable essentials or obtain permission to publish/attach them. Never upload private workspace context wholesale or present a local-only path as a shareable resource. Do not invent assignments or estimates.

## Create, verify, retry

1. Create only authorized issues. After each write, read it back and verify title, scope, criteria references, dependencies, and links.
2. In batches, record successes before continuing. On partial failure, report created IDs and failure details; a retry first reconciles existing results, then creates only missing records. Apply the same no-duplicate rule to local and remote destinations.
3. Return local paths or remote URLs and unresolved blockers. Drafting and issue creation do not authorize implementation.
4. Closing or advancing an issue requires the requested evidence and permission; a worker report alone is insufficient.

## Promote local issues

Promotion requires explicit permission and a resolved configured remote destination. For each local issue:

1. Reconcile whether a remote issue already exists from an earlier attempt. If not, create it with accessible concise essentials and authorized links.
2. Read the remote issue back and verify its scope, criteria references, and dependencies.
3. Only after verification, set the local issue to `promoted`, add `external_url`, and retire its local scope/status authority in favor of the remote issue. Keep the local record as the promotion pointer and intake history, not a competing progress record.

Record each success before the next promotion. On partial failure, leave unpublished local issues usable and authoritative; retries reconcile prior remote successes and never duplicate them.
