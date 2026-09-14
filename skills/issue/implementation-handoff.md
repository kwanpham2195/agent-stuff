# Implementation handoff to an issue destination

Use when the user asks to queue, split, or transfer scoped work for later implementation. Read [work-lifecycle](../references/work-lifecycle.md), the destination rules in [issue](SKILL.md), and [write-issue](../write-issue/SKILL.md). This mode includes technical context; request-intake restrictions on implementation breadcrumbs do not apply.

## Prepare and split

- Confirm an explicit or authorized-default local/remote destination and workspace/repository scope before creating anything. Inspect existing destination records for duplicates and ownership using destination-appropriate operations.
- Read the accepted plan, owning decisions, relevant evidence, and existing issues. Reuse earlier sufficient research rather than repeating ceremonies.
- Split a large plan into independently assignable and verifiable outcomes, not every implementation step. A workspace may span repositories; name affected repository identities and explicit dependencies.
- The plan owns overall sequencing and decisions. Each issue owns only its scope, criteria, dependencies, and status. An execution checkpoint owns evidence and next action only when needed. Do not maintain a duplicate issue-status list in the plan.
- Preserve approval state and unresolved decisions. A proposed plan is not authorization to implement or publish.

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
