# Preference review

Use this reference when a retrospective may turn session behavior into guidance about the user's preferences.

## Classify the evidence

Keep these evidence types separate:

- **Explicit preference**: the user states a desired behavior or corrects the agent toward it.
- **Repeated pattern**: the same choice appears across relevant sessions or tasks.
- **Task constraint**: a choice applies only to the current repository, artifact, or authorization.
- **Hypothesis**: an interpretation that has not been confirmed by the user.

A single choice is usually a task constraint. A correction is evidence of a preference, but still record its scope. Search only the authorized workspace history through the [recall owner](../../recall/SKILL.md) when repeated evidence is needed.

## Propose narrowly

For each proposed preference, record:

- the exact public evidence and its session or artifact scope;
- the behavior the preference would change;
- contradictory examples or a reason the evidence may be one-off;
- the narrowest owner and invocation boundary;
- whether the change needs user approval, global policy approval, installation, or automation authority.

Do not infer a global preference from tone, silence, one experiment, or an agent's workaround. Do not turn a preference hypothesis into a rule without explicit user approval. USER.md owns personal facts, stable preferences, taste and explicit tradeoffs. Link that owner rather than duplicating preferences in operating policy or creating HUMAN.md. Technical fixes that improve compliance with an already explicit preference do not change that preference.
