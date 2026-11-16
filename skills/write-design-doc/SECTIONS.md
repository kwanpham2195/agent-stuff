# Sections

Use this as an open catalogue when drafting. Choose what applies, add project-specific sections when reviewers need them, and leave out empty sections. Order the document as an inverted pyramid. Put anything a reader needs to follow the design on the first page.

## Nearly always

**Title.** Use a short, distinctive name that is easy to say aloud. Name the thing instead of using a codename nobody can decode.

**Metadata.** Record the author, date written, authoritative URL, and approvals with timestamps once they arrive.

**Objective.** State what the project is for in one plain sentence that any stakeholder can understand.

**Background.** Explain why the team is doing this and what problem it solves. Use a narrative rather than bullets. Include previous attempts and why they did not stick.

**Goals.** Describe the intended impact. "Minimize outages when deploying new app versions" is a goal. "Add Kubernetes" is an implementation choice.

**Non-goals.** Name what a reader might reasonably assume is in scope and give the reason each item is excluded.

**Scenarios.** Walk through the finished system step by step when concrete behavior helps the reader assess the design.

**Alternatives considered.** Describe the strong options you rejected and why. Keep this brief.

**Open issues.** For each unresolved design question, state the problem, current options, and immediate next action. Move settled questions to Resolved issues and retain the final rationale.

## When they apply

**Related documents.** Link test plans, functional specifications, related design docs, and earlier versions.

**Users, roles, and permissions.** Describe the people or systems that interact with the design, their needs, and the permissions or responsibilities that affect behavior.

**Product behavior.** Describe important workflows, interactions, notifications, or deliberately omitted features. Include choices that coordinate implementation or define what users experience, even when each choice is individually reversible.

**Assumptions and compatibility.** Record relevant assumptions about users, clients, platforms, existing data, or integrations. State compatibility requirements that constrain the design.

**Migration and import.** Explain how existing users, data, or clients move to the proposed system when migration can affect architecture, privacy, or user behavior.

**Failure and recovery behavior.** Explain failures that affect users, data, dependencies, or operations, and describe the recovery behavior that belongs to the design.

**Glossary.** Define internal tools and systems that a cross-team or new reader would not know. Prefer a clear term or inline definition when possible.

**Constraints.** Explain the budget, client, infrastructure, or dependency limits that shape the design.

**Service level objectives.** Set measurable targets for uptime, latency, and scale, and explain their consequences. For example, 99% availability allows up to 3.65 days of outage a year.

**Monitoring and alerting.** Explain how the team will measure service targets and detect failures or severe slowdowns in production.

**Interfaces.** Show the UI, API or CLI semantics, protocols, or file formats that reviewers need to assess. Include a bounded payload, signature, or type when the contract itself is under review. Keep UI sketches rough and omit pixel-level choices unless they carry product risk.

**Architecture.** Describe relevant components, responsibilities, communication, and data flow. Add an editable diagram when it makes those relationships easier to assess. A small product change may need no architecture section.

**Dependencies and infrastructure.** Cover language, hardware, storage, and third-party packages in proportion to their replacement cost and effect on the design.

**Security.** Describe attack points, trust boundaries, considered threats, and mitigations. Record dismissed threats and the reasons for dismissing them.

**Privacy.** State which sensitive data the system handles, how long it retains that data, who can access it, and how the system protects it at rest and in transit.

**Data retention.** State what the system deletes, when deletion occurs, whether deletion is permanent, and how long backups retain deleted data.

**Legal and licensing.** Record regulatory duties, contractual limits, and open-source licence decisions.

**Logging.** State which events the system logs, at what level, where it stores them, how long it retains them, who can read them, and what must never appear in a log.

**Timeline.** Define milestones with dates when delivery sequencing affects stakeholders or design risk. Choose milestones that produce something useful for review, such as a clickable prototype with dummy data.

**Resolved issues.** Retain settled open issues with the reasoning that led to the decision.

**Appendix.** Put data formats, exports, and long reference material here when they would interrupt the main document.

## Choosing the view

A boxed architecture diagram is not always the clearest view. The `/show-me` skill has worked examples of pseudocode, call trees, component trees, shallow file trees, plain-text flow diagrams, and diffs. Pick the smallest view that makes the point, and put it next to the text it supports.

Which form suits which section:

- **Architecture.** Use a rendered diagram for component communication and data flow. Use a shallow file tree when the decision concerns module ownership.
- **Scenarios.** Use a call tree or a rendered sequence diagram to trace a scenario from the user's action to the result.
- **Interfaces.** Use a component tree for UI shape or a small code block for an API, signature, payload, or file format that needs a copyable target.
- **Alternatives considered.** Use a diff against the current design when reviewers need to judge a focused change within an established structure.
- **Timeline.** Show what each milestone adds when the sequence carries design or stakeholder risk.

These read well partly because they are plain text: reviewers can edit them in a comment, and they diff cleanly between revisions. That satisfies the editable-source rule without any tooling.

**The bound.** Use enough detail to evaluate the decision. A file tree can show which module owns a responsibility. A selected function signature can define the boundary under review. Exhaustive internal types, complete call stacks, and task-level implementation detail belong in the build. Cut a view back when its extra detail no longer helps reviewers assess the design.

## Notes on a few of them

**Goals versus non-goals.** A non-goal with no reason reads as an oversight. State whether it is outside the team's control, deliberately deferred, or owned elsewhere.

**Open issues.** An empty Open issues section is a signal of a mature design, not a section you forgot. Leave it there and write "None."

**Alternatives considered.** Compare the factors that decided the choice, such as cost, operational burden, lock-in, and failure behavior. Avoid an abstract pros-and-cons list.

**Diagrams.** One diagram of how data moves is usually worth more than three of how things are grouped.
