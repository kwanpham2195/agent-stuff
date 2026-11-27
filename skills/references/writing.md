# Writing reviewable artifacts

Use this guidance for the prose of every artifact a person reviews, the user included: plans, designs, proposals, review reports, docs, issues, PRs, drafts of messages to send, and every file saved under a workspace `review/` folder. Chat replies and scheduled job reports keep their own rules. Start with the useful point so the reader knows what the artifact explains or asks them to decide.

Develop each idea in connected prose. Explain the mechanism, reason, and consequence when they help the reader evaluate the work. Use relevant concrete examples and introduce unfamiliar terms where they first matter. Keep enough explanation and evidence for the decision.

Write paragraphs that usually contain one to three sentences. Treat that as a soft readability cue, never a required count or limit. Let sentence length vary naturally, and break the paragraph when the idea changes. Give a complex idea the space it needs rather than compressing it into fragments or a dense paragraph.

Use meaningful headings for real sections. Use lists for genuinely parallel information or sequential steps, and tables, diagrams, or code when they explain the material more clearly. Concise writing cuts filler and repetition while retaining useful explanation and evidence. Keep short status updates short.

Preserve required schemas, field names, repository templates, acceptance evidence, and machine-readable outputs. Apply this style to their explanatory prose without changing their contracts. Leave raw logs, operational state, and runtime contracts in their required formats. Choose the artifact's form for its purpose; a reviewable artifact need not become a tutorial.

## Which rules apply

- Style: apply `writing-guidelines`, then the [clarity rules](#clarity-rules-for-non-native-readers) below. Where they conflict with the writing section of `USER.md`, follow `USER.md`.
- [unslop](../unslop/SKILL.md): only when the user asks.
- Formats: [PR text](../write-pr/SKILL.md), [issue text](../write-issue/SKILL.md), [design docs](../write-design-doc/SKILL.md) and [release notes](release-notes-guide.md).
- Reviewing a draft: [docs-review](../docs-review/SKILL.md).
- Text agents read: [writing-for-agents](../writing-for-agents/SKILL.md).

## Check against the writing guidelines before saving

Before saving or revising a file under a workspace `review/` folder, and before presenting any reviewable artifact, check its prose against the `writing-guidelines` rules and fix every finding. Where those rules and the writing section of `USER.md` differ, follow `USER.md`. Repeat it for every revision, including revisions a delegated worker writes. Leave code, schemas, quoted evidence, raw output, and required template fields unchanged.

## Example

Save the draft before sending the notification. If delivery fails, the saved draft lets the worker retry the message without asking the user to recreate their work. The notification contains the draft's identifier so the recipient can open the same version.

The save and the delivery have separate completion states. A successful save therefore does not prove that the recipient received the message. Show the pending delivery beside the saved draft so the reviewer can distinguish preserved work from completed communication.

## Clarity rules for non-native readers

The codebase is the word list. Write the real symbol, file, flag, or command name, not a synonym or a description of it.

Don't invent jargon. Use the words a developer would say out loud: "move", "delete", "a budget that only decreases", not "evacuate", "ratchet", or "endgame". A named pattern is fine when the doc says what it means the first time.

### Vary the rhythm

The writing guidelines and the rules below decide what a document says and how much each sentence carries. A doc can obey all of them and still read machine-written: every sentence clipped short, no view anywhere, nothing specific.

- Mix sentence lengths on purpose. Short sentences land a point. Longer ones that take their time carry a fact with its condition or consequence.
- One thought per sentence does not mean one length per sentence. Split the sentence that carries two thoughts. Keep the long sentence that carries one.
- Have a view where the mode allows it. Explanation weighs trade-offs, so say what you make of them instead of listing pros and cons. Reference stays dry.
- Be specific over sterile. Not "schema changes can cause issues" but "a column rename fails the build".

### Make statements load one at a time (STE rules)

- One instruction per sentence. One thought per sentence everywhere else.
- Split dense sentences when doing so improves clarity. Word counts are editing cues, not limits.
- Put the warning or condition before the step it guards: "If hot oil touches your skin, injuries can occur."
- Keep "the" and "a": "Remove backup file" reads two ways. "Remove the backup file" reads one.
- Give each word one meaning and one job, then keep it. If "check" means inspect, don't also use it for restrain.
- Pick one word per action and stick to it: "start", not "start" here and "initiate" there.
- Write procedures as direct commands, never as narration and never in the passive: "Install the component", not "the component must be installed".
- Avoid "-ing" words where you can. They take too many grammatical jobs and breed misreadings.

### Leave no sentence open to two readings (Global English)

- Keep words like "only" and "not" next to the word they change: "only fails on growth" and "fails only on growth" say different things.
- Break up long noun strings: "the proto import budget check script" becomes "the script that checks the proto-import budget".
- Make every "it", "they", and "this" point at one obvious thing. Repeat the noun when in doubt. Never use "this" or "which" to point at a whole clause.
- Don't drop verbs: "Phase 1 moves the converters and Phase 2 the runtime" leaves Phase 2 without one. Give it one.
- Keep the small words that show structure. "Ensure that the switch is off" keeps "that" because it makes the sentence parse one way. Never trade clarity for word count.
- Repeat the article in a series when it prevents a misread: "the client and the host", not "the client and host", when they are two things.
- Say which parts "and" or "or" joins when a sentence can group two ways. "Both...and", "either...or", and "if...then" are free disambiguators.
- Use periods, not semicolons. Replace an em dash with a new sentence.
- Make text in parentheses a full grammatical unit or its own sentence. Never form plurals with "(s)".
- No slashes: write "a, b, or both" instead of "a/b" or "and/or".
- Call each thing by one name, everywhere. A doc that says "the gate", "the ratchet", and "the budget check" for one thing teaches three things. Rewording an unchanged sentence between edits costs the same way. Don't churn what didn't change.
- Skip idioms, colloquialisms, Latin abbreviations, and metaphors. A non-native reader, a translator, and an agent all parse plain constructions best.
