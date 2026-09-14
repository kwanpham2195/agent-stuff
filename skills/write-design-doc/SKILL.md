---
name: write-design-doc
description: Write a design doc that settles hard-to-reverse decisions before anyone builds.
disable-model-invocation: true
---

# Write a design doc

A design doc makes the team think through costly decisions before implementation, keeps the project off expensive wrong paths, and coordinates the decisions across everyone who touches them. It is a **decision document**, not an implementation plan.

It is written for people who were not in your head: teammates, partner teams, stakeholders, and someone who joins in six months. Anyone you expect to read it must be able to read it without prior context.

Based on Michael Lynch's [Write an effective design doc](https://refactoringenglish.com/excerpts/write-an-effective-design-doc/). The worked example is [the Little Moments design doc](https://refactoringenglish.com/excerpts/write-an-effective-design-doc/little-moments-design-doc/) — read it when you want to see the register and depth rather than infer them.

## 1. Decide whether to write one at all

Sometimes the right amount to invest in a design doc is zero. Answer these:

- Will several people coordinate the implementation?
- Will the work take more than about three months full time?
- Will what you build run in production for years?
- Does it cross team boundaries?
- Are the goals or requirements still ambiguous?
- Could a catastrophic risk — security, legal, data loss — be prevented at design time?

Two or more yes answers justify the effort. Fewer, and say so rather than writing one out of habit.

Then size it. A doc runs from a one-pager to fifty pages with multi-team signoff, and the right size depends on the team's goals, risks, deadlines, and culture. Propose the size before drafting.

**Completion criterion:** the decision to write, and the intended size, are both stated and grounded in the questions above.

## 2. Decide what goes in it

One test governs every candidate: **what is the penalty for being wrong?**

In: decisions that are costly or impossible to reverse — the language, the storage backend, the architecture, the trust boundary, the data you retain.

Out: decisions someone can change in an afternoon. A "load more" button does not deserve design review cycles.

Specifying every possible detail means writing the implementation during the design phase. Contracts, function signatures, call stacks and test plans belong to the build, not here — reach for `/to-tickets`, `/implement`, `/tdd` and `/coding-standards` when the design is settled.

**Completion criterion:** every decision in the doc has a real reversal cost, and no section has drifted into implementation.

## 3. Load the local context

Inspect existing code and docs for vocabulary, prior art, and precedent: earlier attempts at this problem, related design docs, ADRs, `CONTEXT.md`, and the conventions the team already follows. Where the repo already keeps design docs, match that convention.

Do not introduce a term, tool, or pattern before checking whether one is already established.

**Completion criterion:** the doc uses project vocabulary, and every previous attempt at the problem is either referenced or confirmed absent.

## 4. Draft it

Pick the sections that apply from [SECTIONS.md](SECTIONS.md). Not every doc needs all of them; a doc padded with empty sections is worse than a short one.

Order it as an inverted pyramid. The early sections make sense to anyone you expect to read the doc, whatever their background; later sections may assume more context. Whatever a reader needs in order to follow the doc belongs on the first page.

Two things carry disproportionate weight:

- **Diagrams.** You can see the architecture in your head; reviewers cannot, and drawing it is the fastest way to give them the picture. Roughly half of all review feedback lands on diagrams, because they are what make an architecture arguable. Use an editable source — Mermaid, D2, Excalidraw, draw.io — and link that source so anyone can revise it. A photo of a whiteboard is not a diagram. A boxed diagram is not the only option: see [Choosing the view](SECTIONS.md#choosing-the-view) for the lighter forms and when each one reads better.
- **Scenarios.** Concrete walkthroughs of the finished system in use, step by step. They ground abstract requirements in something a reader can picture.

Frame goals as impact, never as implementation. "Minimize outages when deploying new app versions" is a goal; "Add Kubernetes" is not.

Mark anything you do not know as an open issue. Do not invent requirements, constraints, or rationale to make the doc feel finished.

**Completion criterion:** every included section earns its place, the first page is readable by every intended audience, each architectural claim has a diagram or a scenario behind it, and every unknown appears in Open issues rather than as invented detail.

## 5. Get feedback and close it out

Follow [REVIEW.md](REVIEW.md). The short version: one reviewer before many, asynchronous reading before any meeting, and a meeting only for what text could not settle.

**Completion criterion:** every comment thread is resolved or promoted to Open issues, and the doc reflects the decisions rather than the argument that produced them.

## When there is not enough context yet

If the problem, constraints, users, or success criteria are still vague, do not draft. Say that there is not enough context for a design doc, then run the `/grilling` skill — the whole frontier each round, numbered, with a recommended answer on each — until you can answer step 1 and step 2. Then draft.

Facts are your job: if a question can be answered by reading the codebase or the docs, read them instead of asking.

## Output

A design doc is a human-readable decision artifact, not an execution plan. Follow [context routing](../references/context-routing.md): reuse an existing authoritative design artifact and honor repository-required conventions. A draft intended for local review may use the current work item's optional `design.md` and may remain local. Publishing or promoting it to a shared repository or tracker requires authorization; after promotion, the local entry links the shared authority rather than maintaining a duplicate.

For a shared or repository-required design doc, save it where the repo already keeps design docs. Common locations to check: `docs/design/`, `docs/designs/`, `docs/technical-designs/`, `docs/adr/`. If the repo has no convention, use `docs/design/<slug>.md` and say where you put it. Creating or approving the document does not authorize committing or publishing it.

The filename stays stable while people comment on it — no date prefix. The date it was written belongs in the Metadata section.

Give it a short, distinctive title that is easy to say aloud. "RecencyBank" works. "Project Flying Silver Horse" does not.

## Rules

- Plain language in the objective and background: any stakeholder should follow them.
- Goals state impact; implementation choices are not goals.
- Define internal jargon inline, or use a term readers already know.
- Express targets in concrete, objective terms. "Performant on mobile" is not a target; "under 200ms at the 95th percentile" is.
- Document the threats you considered and why you judged them, even the ones you dismissed.
- Keep rejected alternatives brief. Cover the strong ones and why they lost; do not catalogue every idea anyone had.
- One source of truth. If two sections say the same thing, one of them points at the other.
- Record technical choices and rationale here while this document owns them, including approval source and worthwhile rejected alternatives. A draft or agent proposal is not accepted without actual approval or delegated authority. If a decision later earns a workspace-wide decision record or an existing repository ADR owns it, follow [context routing](../references/context-routing.md) and link that authority rather than maintaining duplicate semantics.
- Unknowns stay open issues.

## This skill does not

- implement anything, or ask to;
- specify types, function signatures, call stacks, or a test plan;
- replace `/to-tickets`, which turns a settled design into work.
