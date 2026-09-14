---
name: to-questionnaire
description: Turn a decision you cannot fully answer into a questionnaire for someone else to complete.
disable-model-invocation: true
---

# To questionnaire

Turn a decision the user cannot answer alone into a Markdown questionnaire. The recipient has the missing knowledge. They can complete it alone or with the user in a meeting.

**Grill the send, not the subject.** Ask the user only about who will receive it and what they need back. Then write questions that close the gap between what the recipient knows and what the user needs.

1. **Who will receive it?** Ask in one exchange for the recipient's role, expertise, and relationship to the user. This sets the tone and needed context. Done when you know who they are and what they know that the user does not.

2. **What do you need back?** Ask in one exchange for the facts or decisions the user needs from this person. Done when you have a concrete list of what the user must be able to do or decide.

3. **Write the questionnaire.** Draft questions that close the gap from steps 1–2. Follow the structure below. Write the file to `to-questionnaire-<slug>.md` in the current directory, where the slug comes from the topic. Report the path. Done when the file exists and covers every item from step 2.

## Document structure

Write a discovery questionnaire: the user lacks context and the recipient has it. Put the most important questions first because the recipient may answer only once. Group more than a few questions under `##` theme headings.

<questionnaire-template>

# <Questionnaire title>

**Purpose:** Why this questionnaire exists and the decision it supports.

**From:** <the user> — **To:** <the recipient> — **How your answers will be used:** <where they go>

## Context

One paragraph for a recipient who was not part of the prior conversation. Give enough context to answer well. Do not write a page.

## How to answer

State the deadline and rough effort. Partial answers and "I don't know" are useful. Ask the recipient to flag uncertainty rather than skip a question.

## <Theme heading>

Use one `##` section per theme. Put questions in importance order. Each question must ask one thing. Put an answer stub below it. Add one line on why it matters only when the question could be misunderstood or invite a weak answer.

<question-example>
### What load is the system expected to handle at launch?

_Why this matters: it decides whether we provision for burst traffic now or defer it._

>
</question-example>

## Anything else?

Ask for anything important that this questionnaire missed.

</questionnaire-template>
