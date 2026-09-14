# Sections

The catalogue to pick from when drafting. Choose what applies; a doc padded with empty sections is worse than a short one. Order them as an inverted pyramid — anything a reader needs in order to follow the doc goes on the first page.

## Nearly always

**Title** — short, distinctive, easy to say aloud. Names the thing, not a codename nobody can decode.

**Metadata** — author, date written, the authoritative URL for this doc, and approvals with timestamps once they arrive.

**Objective** — one plain sentence, in language any stakeholder understands, saying what this is for.

**Background** — why the team is doing this and what problem it solves. Narrative, not bullets. Include previous attempts at the problem and why they did not stick.

**Goals** — framed as impact. "Minimize outages when deploying new app versions", not "Add Kubernetes".

**Non-goals** — what a reader might reasonably assume is in scope but is not, each with its reason. The reasons matter as much as the list.

**Scenarios** — concrete step-by-step walkthroughs of the finished system in use. This is what lets a reader picture the solution instead of parsing requirements.

**Architecture** — a diagram plus prose describing each component and why it is shaped that way. Editable source (Mermaid, D2, Excalidraw, draw.io), linked so anyone can revise it.

**Alternatives considered** — the strong options you rejected and why. Brief. Not a catalogue of every idea anyone floated.

**Open issues** — each entry states the problem, the options on the table, and the immediate next action. Move them to Resolved issues as they close, keeping the discussion and the final rationale.

## When they apply

**Related documents** — test plans, functional specs, neighbouring design docs, earlier versions of this one.

**Glossary** — internal tools and systems a cross-team or new reader would not know. Better still, define terms inline so nobody has to jump around.

**Constraints** — budget, client, infrastructure, or dependency limits that shape the design.

**Service level objectives** — measurable targets for uptime, latency, and scale, with their consequences spelled out. "99% availability, which allows up to 3.65 days of outage a year."

**Monitoring and alerting** — how you will measure those targets in production. If the service goes down, how do you find out? If it slows by 100x, how do you know?

**Interfaces** — UI sketches, API or CLI semantics, file formats. Keep UI sketches rough; pixel decisions are cheap to reverse and do not belong here.

**Dependencies and infrastructure** — language, hardware, storage, third-party packages. Spend the words on what is hard to change later, not on what you could swap in a day.

**Security** — attack surface, trust boundaries, the threats you considered, and the mitigation for each. Record the threats you dismissed and why.

**Privacy** — what sensitive data you handle, how long you keep it, who can reach it, and how it is protected at rest and in transit.

**Data retention** — what is deleted, when, and whether deletes are hard, plus how long backups hold what was deleted.

**Legal and licensing** — regulatory obligations, contractual limits, open-source licences.

**Logging** — which events are logged, at what level, kept how long, readable by whom, and what must never appear in them.

**Timeline** — milestones with dates. Choose milestones that produce something useful to stakeholders: a clickable prototype on dummy data before the data plumbing is real.

**Resolved issues** — closed open issues, with the discussion and the reasoning that settled them. This is what makes the doc worth reading a year later.

**Appendix** — data formats, exports, long reference material that would break the flow of the doc.

## Choosing the view

A boxed architecture diagram is not always the clearest thing to draw. The `/show-me` skill holds the full catalogue of forms and worked examples — pseudocode, call trees, component trees, shallow file trees, Mermaid, diffs — and it applies here. Pick the smallest view that makes the point, and put it next to the short text it supports rather than in a diagram appendix.

Which form suits which section:

- **Architecture** — Mermaid for how components talk and where data flows; a shallow file tree when the point is which module owns what.
- **Scenarios** — a call tree, or a Mermaid sequence diagram, walking one scenario from the user's action to the result. Easier to check against reality than a paragraph.
- **Interfaces** — a component tree for UI shape; a small block for an API or file format when the reader needs a copyable target.
- **Alternatives considered** — a **diff** against the current design. When the surrounding shape already exists and only part of it changes, showing the change alone is far easier to judge than two full diagrams side by side.
- **Timeline** — what each milestone adds, as a diff against the milestone before it.

These read well partly because they are plain text: reviewers can edit them in a comment, and they diff cleanly between revisions. That satisfies the editable-source rule without any tooling.

**The bound.** These are sketches at the altitude the decision needs, not contracts. A file tree that shows which module owns a responsibility is design. Full function signatures, exhaustive type definitions, and a complete call stack are the implementation, and putting them here means writing the build during the design phase. If a view has grown past the decision it exists to settle, cut it back.

## Notes on a few of them

**Goals versus non-goals.** A non-goal with no reason attached reads as an oversight. Say why it is out: out of your control, deliberately deferred, or someone else's problem.

**Open issues.** An empty Open issues section is a signal of a mature design, not a section you forgot. Leave it there and write "None."

**Alternatives considered.** Compare on the dimensions that decided it — cost, operational burden, lock-in, how it fails — rather than listing pros and cons in the abstract.

**Diagrams.** One diagram of how data moves is usually worth more than three of how things are grouped.
