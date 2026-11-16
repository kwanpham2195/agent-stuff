# Advisor dialogue

An advisor is a read-only thinking partner for a consequential decision. It examines evidence and tradeoffs. The parent retains coordination, and the user retains product and scope decisions. This branch uses the delegation skill's permission, ownership, and harness rules, with the decision brief and response below in place of implementation report fields.

## Select at a decision boundary

- An explicit request to consult a separate advisor or oracle, or to obtain another agent's second opinion, authorizes one advisor consultation within the requested scope, unless a conflicting delegation restriction remains unresolved.
- Otherwise, offer an advisor when several plausible approaches have consequential tradeoffs, new evidence undermines an accepted plan, or repeated failures suggest the approach needs reconsideration. First inspect enough context to state the actual decision. Uncertainty alone is not a reason to spawn.
- Do not trigger solely because a task spans files or context windows. A factual lookup belongs to research, checking completed work belongs to review, and routine implementation choices stay with the implementer.
- A request for "advice," "a second opinion," or "what do you think?" that does not ask for another agent can be answered inline. It does not by itself request a separate agent. A request to define this workflow does not authorize launching an advisor.

Default to a brief offer before spawning. Name the decision, why an advisor would help, and the proposed advisor and model when known. Ask only for missing authorization or preferences that affect this consultation. A decline applies to that decision; do not offer again unless new evidence materially changes it or the user reopens it.

## Respect user preferences

Resolve current task instructions first, then session preferences, then durable user or repository defaults. Honor "no delegation". If the user later explicitly requests an advisor, clarify only a remaining conflict rather than silently bypassing the restriction.

The user can choose:

- **Off:** no advisor and no unsolicited offers within the stated scope.
- **Ask first:** offer before launching. This is the default when no preference is known.
- **Automatic within scope:** launch for the decision triggers above without repeated approval, subject to granted scope and budgets. Announce the decision being examined.
- The advisor, the model, and the reasoning level; inherited context or an independent fresh brief; the decision scope; time and cost limits; or a one-shot answer instead of dialogue.

Do not make the user configure every option. Honor supplied choices, and otherwise use the advisor entry in [model policy](references/model-policy.md). Follow its capability checks, launch disclosure, and substitution rules. Ask before using an alternative execution mode. Use one advisor unless the user requests multiple perspectives or a council.

A preference applies only as broadly as the user stated. Do not turn a one-time approval into a standing rule, and ask before persisting a session preference globally. Record applicable preferences in an existing checkpoint when work spans sessions. The user can stop, redirect, or narrow the consultation at any time.

## Brief the advisor

```text
Decision: what must be chosen, and why now
Outcome / acceptance: desired result and criteria
Constraints: scope, permissions, compatibility, relevant user preferences
Read first: repository instructions, exact skill paths, authoritative artifacts
Evidence: established facts and sources; observations versus assumptions
Options: current candidates; parent preference labeled as a hypothesis
Unknowns: missing evidence and user-owned questions
Ready when: evidence or judgment needed to decide; agreed limits
Authority: read-only; no edits, publishing, assignments, or further delegation
```

Give the advisor enough context to understand the problem without steering it toward agreement. If the user wants independence, provide a fresh factual brief rather than the parent's full argument. Bind output through the harness when a durable artifact is needed.

## Conduct the dialogue

1. The advisor examines evidence and requests missing information through the harness's supervisor channel. The parent answers factual questions from available sources, arranges authorized probes, or asks the user for judgment.
2. The advisor returns a recommendation, alternatives, uncertainty, and what could invalidate its conclusion.
3. The parent challenges a consequential assumption or failure scenario using evidence. Do not manufacture disagreement or prescribe a fixed number of rounds. Revisit the recommendation when new evidence warrants it.
4. End with a supported decision, a bounded experiment that will settle the question, or an explicit unresolved blocker. Stop when the user asks, agreed limits are reached, or further exchange adds no evidence.

Use supervisor dialogue and retained context when the harness supports them. Do not leave a waiting advisor without a response. If dialogue is unavailable, report that limitation and ask before substituting a one-shot consultation, unless the user already requested that mode. Follow the harness's stop and resume protocol rather than restarting or resending blindly.

## Return and record

```text
Recommendation: choice and rationale
Alternatives: relevant tradeoffs
Evidence / assumptions: sources and remaining uncertainty
Challenge: question tested and how the recommendation changed or held
Invalidation: what would change the recommendation
Next experiment: smallest useful probe, if needed
User decisions: unresolved judgment or scope questions
Disposition: accepted / rejected / experiment needed / unresolved
```

The parent labels the final disposition, and an advisor recommendation is not approval. Summarize enough for the user to accept, reject, or redirect. Decide locally only within granted authority. Record accepted choices, rationale, approval source, and relevant disagreement in the owning artifact; update affected plans and acceptance criteria only after the required decision. Advice does not authorize implementation, expand scope, or establish verification success.
