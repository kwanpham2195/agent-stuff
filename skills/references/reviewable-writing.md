# Writing reviewable artifacts

Use this guidance for the human-facing prose in plans, designs, proposals, review reports, and every file saved under a workspace `review/` folder. Start with the useful point so the reader knows what the artifact explains or asks them to decide.

Develop each idea in connected prose. Explain the mechanism, reason, and consequence when they help the reader evaluate the work. Use relevant concrete examples and introduce unfamiliar terms where they first matter. Keep enough explanation and evidence for the decision.

Write paragraphs that usually contain one to three sentences. Treat that as a soft readability cue, never a required count or limit. Let sentence length vary naturally, and break the paragraph when the idea changes. Give a complex idea the space it needs rather than compressing it into fragments or a dense paragraph.

Use meaningful headings for real sections. Use lists for genuinely parallel information or sequential steps, and tables, diagrams, or code when they explain the material more clearly. Concise writing cuts filler and repetition while retaining useful explanation and evidence. Keep short status updates short.

Preserve required schemas, field names, repository templates, acceptance evidence, and machine-readable outputs. Apply this style to their explanatory prose without changing their contracts. Leave raw logs, operational state, and runtime contracts in their required formats. Choose the artifact's form for its purpose; a reviewable artifact need not become a tutorial.

## Unslop before saving

Before saving or revising a file under a workspace `review/` folder, and before presenting any reviewable artifact, run the [unslop](../unslop/SKILL.md) pass on its prose: scan for the listed patterns, rewrite, then self-audit. Repeat it for every revision, including revisions a delegated worker writes. Leave code, schemas, quoted evidence, raw output, and required template fields unchanged.

## Example

Save the draft before sending the notification. If delivery fails, the saved draft lets the worker retry the message without asking the user to recreate their work. The notification contains the draft's identifier so the recipient can open the same version.

The save and the delivery have separate completion states. A successful save therefore does not prove that the recipient received the message. Show the pending delivery beside the saved draft so the reviewer can distinguish preserved work from completed communication.
