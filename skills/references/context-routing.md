# Preparation and routing order

Start with the request and applicable instructions, then load the action skill early and make the cheap workspace check below. The action skill controls the depth: small work remains inline with no mandatory plan, research, issue, or artifact. Resume existing authoritative work before creating anything. Read the owning outcome and accepted decisions, then only relevant evidence; name remaining gaps and gather enough context to act. Resolve a small factual gap by direct exploration. For substantial independent questions, use the bounded exploration contract in [delegated-execution](../delegated-execution/SKILL.md) only when delegation is permitted. Ask the user only for missing intent.

Synthesize evidence and resolve consequential uncertainty before writing to an authorized destination. Do not force unrelated documents, absent PRDs/plans, or repetitive checks already preserved by a sufficient current checkpoint.

# Context and artifact routing

On the first task or resume in a working directory, make a cheap routing check using `~/.agents/context/index.md`, its workspace directory entries, and repository identity hints. Paths are hints; stable remote or repository identities are supporting evidence. A registered workspace may contain multiple repositories and the current directory may be any descendant.

- If one workspace clearly owns the directory, use only that workspace's context.
- If no workspace owns it, always ask whether to create/register a workspace, associate the directory with an existing workspace, or continue for this session without registration. Do not create one silently or persist a skip choice.
- If mappings overlap, identities conflict, or a repo may be a fork/worktree, ask rather than merging or selecting silently.
- Never retrieve or associate work across workspaces. Reject a cross-workspace task or ask the user to choose one workspace boundary. Cross-repository work inside one workspace is allowed.

Keep this check cheap: do not search the full vault, inspect unrelated workspace notes, or require a model hook, extension, tool, CLI, or startup automation. These instructions are checked on the first task/resume, not automatically at process startup.

## Accepted decisions

Store a task decision with its owning document: small-task decisions and approval in the work `index.md`, product scope and requirements in `prd.md`, technical choices and rationale in `design.md`, and execution sequencing in `plan.md`. These documents remain optional. If a repository ADR or shared decision document already owns the decision, reuse and link it.

Create `knowledge/decisions/<decision-id>.md` only for a durable decision that spans future tasks in the same workspace and lacks a repository authority. The original owning document then links to that authority instead of maintaining a duplicate. Record state (`proposed`, `accepted`, or `superseded`), decision and scope, rationale and rejected alternatives worth retaining, approver/date/approval source or explicit delegated authority, evidence, and reconsideration conditions. Superseded records retain rationale and link their replacement.

Acceptance is neither automatic promotion nor publication. Subagents may propose decisions but mark them accepted only with actual approval or explicit delegated authority. Promotion to a shared authority requires permission.

## Place context and artifacts

Small work stays inline under [work-lifecycle](work-lifecycle.md), even when a short workspace registration entry is needed. Do not require a work record, research note, full-vault search, or plan for a quick fix or bounded lookup.

1. Resume the existing authoritative artifact first, whether it is a repository document, workspace work record, plan, or tracker issue. Read only needed links and reconcile stored claims with current state. Do not copy or move it without authorization.
2. Honor an explicit artifact destination. Repository-required conventions and an existing authoritative artifact owner take precedence; surface conflicts before writing.
3. For local durable context, use `~/.agents/context/workspaces/<workspace-id>/`. The workspace is the sole context and work ownership boundary. Use `index.md` for workspace identity and directory/repository hints. Within `work/<work-id>/`, `index.md` owns the short checkpoint and may also own the outcome and acceptance contract; add `prd.md` only when separate requirements are warranted, `design.md` only when a technical or design document is warranted, and `plan.md` only when an execution plan is warranted. Keep research and artifacts beneath that work item, and reusable workspace knowledge under `knowledge/`. Root `templates/` supplies templates. Create only what the work needs; do not automatically collect every optional file or require a standalone outcome file.

If the selected store or artifact destination is inaccessible, report the blocker and next action; do not duplicate durable state elsewhere. An interim inline response is allowed.

Reuse existing skill formats, permissions, review pauses, and handoff semantics. Developer-facing artifacts retain repository-required homes, and `CONTEXT.md` remains the [domain-modeling](../workflow/domain-modeling/SKILL.md) glossary. An accepted local PRD or design draft may remain local. Promote it to a shared repository or tracker only with authorization; then link the authoritative destination from the local entry and do not maintain an independent duplicate. When a tracker takes ownership, mark the local record handed off, link it, and stop maintaining parallel scope/status; publishing, attachment, assignment, and status changes require authorization. Policy promotion also requires authorization. Creating any document does not authorize committing or publishing it.

`~/.agents/context/` is private local working data excluded from chezmoi; this describes scope, not enforced filesystem isolation. Local storage does not imply local inference, and retrieved content may reach the configured model provider. Obsidian and its verified shared configuration links are optional. This adds no sync or backup service.

Use [work-lifecycle](work-lifecycle.md) for checkpoint contents, acceptance, and resumption; this reference owns placement only.
