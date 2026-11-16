---
name: define-outcome
description: "Clarify ambiguous product intent, scope, or observable acceptance for a feature or change."
---

Deliver a compact acceptance contract that a fresh developer, agent, or reviewer can evaluate without the conversation. Reuse sufficient existing criteria.

## Establish the target

1. Read the request and relevant existing product decisions, issues, examples, and behavior. Extract what is already agreed; distinguish user requirements, observed facts, and your proposals.
2. Identify the user, situation, problem, desired outcome, scope, and exclusions. For discretionary new work, capture why it matters now and what evidence would make it unnecessary when those affect the decision. Reuse stated intent; do not require a business case for a routine fix. Keep agreed stop conditions with the owning criteria. Ask only questions requiring user intent or judgment. Investigate factual questions yourself. Do not invent users, targets, constraints, or approval to fill the template.
3. Describe observable scenarios with starting conditions, action, and expected result. Include failure and boundary cases relevant to the risk; do not enumerate speculative cases. Include performance, accessibility, compatibility, or safety constraints only when required or materially relevant, and confirm proposed thresholds.
4. For each criterion, specify evidence: automated test, live demonstration, measurement, or human review. State the environment or fixture when it affects the verdict. Identify the decision owner for subjective acceptance; if unknown, leave it unresolved rather than assigning someone.
5. Present unresolved assumptions and proposed criteria for confirmation. Existing explicit requirements need no redundant approval. Do not proceed past a consequential unresolved decision; research or prototypes may continue within authorized scope.

## Record the contract

Keep small contracts inline. For durable work, follow [context-routing](../references/context-routing.md) for the authoritative contract home and link it from plans. Do not create a PRD or standalone outcome or acceptance file by default. Follow [work-lifecycle](../references/work-lifecycle.md) for checkpointing and resumption.

Use this shape only as far as it helps:

```text
User / situation / problem:
Desired outcome:
Scope / exclusions:
Why now / agreed stop conditions: when relevant

A1: Given … when … then …
Evidence: method, conditions, expected observation
Human decision owner: when required

Relevant failure / boundary scenarios:
Open assumptions and decisions:
Approval: agreed requirements versus proposed additions
```

Use stable criterion IDs when plans, issues, or tests need to reference them. When a PRD, design document, or issue already owns criteria, plans reference those IDs instead of duplicating them. For visual or interaction requirements, use [show-me](../show-me/SKILL.md) to include mockups, diagrams, sample outputs, or behavior sketches. Mark which details are required and which are illustrative. Specify implementation only when it is an actual constraint.

## Verify without redefining success

- Keep required evidence distinct from evidence actually collected. Before checks run, criteria are pending.
- Report evaluated criteria as **passed**, **failed**, **blocked**, or **awaiting human review**, with supporting results or the missing evidence. Reserve **passed** for criteria whose required evidence is satisfied; passing automated checks does not substitute for required human acceptance.
- Evaluate both behavior correctness and whether it achieves the agreed user outcome. Report incomplete or untested criteria rather than declaring the whole task done.
- When feedback changes the target, record the decision, rationale, and approval source. Update affected plans, visuals, issues, and checks through links to the owning contract. Do not weaken criteria merely to match the implementation.

Finish definition when the outcome, scope, observable criteria, and evidence approach are clear enough to guide the next authorized step. If they are not, return the unresolved decisions and who or what can settle them. Defining acceptance does not authorize implementation or publishing.
