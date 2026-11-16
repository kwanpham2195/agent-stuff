---
name: sharpen
description: "Rewrite a task prompt to be deeper, not bigger, before it runs. Use for /sharpen."
disable-model-invocation: true
---

Make the task deeper, not bigger. Do not do the task, and do not start workers.

Answer four questions before rewriting:

1. What would a top professional in this field do here that the prompt does not ask for?
2. What raw material would they start from, instead of material already summarized for the user?
3. Which methods and tools would they use?
4. What, other than you or the user, would show the result is right?

Rewrite the prompt to ask for exactly that. Leave choices that belong to the user open and list them as questions.

Return the four answers, one line each, then the rewritten prompt. The user sends the rewrite when it reads right.
