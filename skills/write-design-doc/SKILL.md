---
name: write-design-doc
description: Write a design doc that makes a proposed system understandable and settles consequential decisions before implementation.
disable-model-invocation: true
---

# Write a design doc

Before drafting or materially revising the design, read and apply [Writing reviewable artifacts](../references/reviewable-writing.md).

Write for builders, reviewers, operators, and stakeholders without prior context.

This skill is a faithful adaptation of Michael Lynch's [Write an effective design doc](https://refactoringenglish.com/excerpts/write-an-effective-design-doc/). The [Little Moments design doc](https://refactoringenglish.com/excerpts/write-an-effective-design-doc/little-moments-design-doc/) shows the depth and project-specific sections that a substantial design may need. The instructions below remain usable without either page.

## 1. Decide whether to write one at all

Answer these before proposing a design doc:

- Will several people coordinate the implementation?
- Will the work take more than about three months full time?
- Will what you build run in production for years?
- Does it cross team boundaries?
- Are the goals or requirements still ambiguous?
- Could a catastrophic security, legal, or data-loss risk be prevented at design time?

One yes answer probably justifies a design doc. Two or more make the effort strongly advisable. Use judgment because a single catastrophic risk may matter more than several minor coordination concerns.

Then size it to the team's goals, risks, deadlines, and culture. Infer an appropriate depth from the request and proceed with the draft. Ask only when a consequential scope choice remains unresolved.

**Completion criterion:** the decision to write, and the intended size, are both stated and grounded in the questions above.

## 2. Decide what goes in it

Use one question to choose the depth for each topic: **what is the penalty for being wrong?**

Give costly or difficult decisions enough detail for reviewers to challenge them. Examples include the language, storage backend, architecture, trust boundaries, and retained data.

Keep cheap decisions brief unless they define user behavior, establish a shared contract, constrain another owner, or help reviewers understand the proposed system. A pagination control rarely needs design review by itself. The behavior of a complete user flow may still belong in the design.

Include enough interface detail to evaluate the design. API or CLI semantics, example payloads, file formats, and selected function signatures are appropriate when the contract is the subject of review. Leave exhaustive internal types, complete call stacks, task breakdowns, and implementation-level test plans to the build. Use the repository's issue workflow or [work-lifecycle](../references/work-lifecycle.md#plan-act-verify-accept) when the settled design needs a durable implementation plan.

**Completion criterion:** each topic has enough detail for its risk and coordination cost, and the doc does not prescribe implementation details that reviewers do not need to assess the design.

## 3. Load the local context

Inspect existing code and docs for vocabulary, prior art, and precedent: earlier attempts at this problem, related design docs, ADRs, `CONTEXT.md`, and the conventions the team already follows. Where the repo already keeps design docs, match that convention. For warranted ADRs, read [ADR format](../references/adr-format.md); repository-specific rules take precedence.

Do not introduce a term, tool, or pattern before checking whether one is already established.

**Completion criterion:** the doc uses project vocabulary, and every previous attempt at the problem is either referenced or confirmed absent.

## 4. Draft it

Use [SECTIONS.md](SECTIONS.md) as an open catalogue. Choose the sections that help reviewers understand this system, and add project-specific sections when the design needs them.

Order it as an inverted pyramid. The early sections make sense to anyone you expect to read the doc, whatever their background; later sections may assume more context. Whatever a reader needs in order to follow the doc belongs on the first page.

Use concrete views when they make the design easier to assess:

- **Diagrams.** Draw architecture, component relationships, protocols, or data flow when prose would make those relationships hard to follow. Keep an editable source such as Mermaid, D2, Excalidraw, or draw.io beside the doc, embed the rendered PNG, and link the source so reviewers can revise it. Never paste Mermaid text into the doc; see [mermaid-png](../mermaid-png/SKILL.md). See [Choosing the view](SECTIONS.md#choosing-the-view) for lighter forms.
- **Scenarios.** Walk through the finished system step by step when reviewers need to understand user behavior, system interaction, ordering, or failure handling.

Frame goals as impact, never as implementation. "Minimize outages when deploying new app versions" is a goal; "Add Kubernetes" is not.

Record unresolved questions that could change the design as open issues. Leave minor implementation questions to the implementation workflow. Do not invent requirements, constraints, or rationale to make the doc feel finished.

**Completion criterion:** every included section earns its place, the first page is readable by every intended audience, concrete views clarify the relationships or behavior that reviewers need to assess, and unresolved design questions appear in Open issues.

## 5. Get feedback and close it out

Follow [REVIEW.md](REVIEW.md) for review order and comment resolution.

**Completion criterion:** every comment thread is resolved or promoted to Open issues, and the doc reflects the decisions rather than the argument that produced them.

## When there is not enough context yet

If the problem, constraints, users, or success criteria are still vague, do not draft. Use [define-outcome](../define-outcome/SKILL.md) to settle intent and observable acceptance. Resolve missing facts through RPI's research steps. Draft only when you can answer step 1 and step 2.

Facts are your job: if a question can be answered by reading the codebase or the docs, read them instead of asking.

## Output

Follow [context routing](../references/context-routing.md) for artifact ownership, local drafts, promotion, and accepted decisions. Reuse an authoritative design and honor repository conventions. Local drafts may remain local; publishing or promotion requires authorization.

For a shared or repository-required design doc, save it where the repo already keeps design docs. Common locations to check: `docs/design/`, `docs/designs/`, `docs/technical-designs/`, `docs/adr/`. If the repo has no convention, use `docs/design/<slug>.md` and say where you put it. Commit a completed, verified draft as a proposal under [commit](../commit/SKILL.md). Document approval does not authorize publication or implementation beyond the requested scope.

The filename stays stable while people comment on it. Put the date in the Metadata section instead of the filename.

Give it a short, distinctive title that is easy to say aloud. "RecencyBank" works. "Project Flying Silver Horse" does not.

## Rules

- Plain language in the objective and background: any stakeholder should follow them.
- Define internal jargon inline, or use a term readers already know.
- Express targets in concrete, objective terms. "Performant on mobile" is not a target; "under 200ms at the 95th percentile" is.
- Document threats relevant to the system and the reasons for consequential security decisions. Omit hypothetical warnings and checklists that do not affect the design.
- Keep rejected alternatives brief. Cover the strong ones and why they lost; do not catalogue every idea anyone had.
- One source of truth. If two sections say the same thing, one of them points at the other.
- Record technical choices and rationale here while this document owns them, including approval source and worthwhile rejected alternatives. A draft or agent proposal is not accepted without actual approval or delegated authority. Link a superseding workspace decision record or an existing repository ADR rather than duplicating its semantics.

## This skill does not

- implement the design or grant permission to implement it;
- provide an exhaustive internal specification, task breakdown, or implementation-level test plan;
- replace the repository's issue or execution-planning workflow.
