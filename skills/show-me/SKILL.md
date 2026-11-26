---
name: show-me
description: "Explain technical work or prepare developer review artifacts with diagrams, structural diffs, short code, pseudocode, and concrete contracts."
---

Help the user understand the current topic of conversation visually. Skip the preamble and keep prose brief. Pick the smallest view that makes the key point clear.

Show real code directly when it is short and says more than a table, diagram or pseudocode would. It keeps exact names, types, calls and error handling that other formats paraphrase away. Use another format when the code would be long, or when its noise would hide the point.

- Use Markdown tables for dense field comparisons and input/rule/output mappings. Distinguish absent, `null`, empty, and populated values.

Bad: `website = null -> omitted; website = "" -> sent empty`.

Good:

| Input | Output |
| --- | --- |
| `website: null` | Field omitted |
| `website: ""` | Empty string sent |

- Keep readable text decision blocks. Separate cases with blank lines and indent conditions and results.

Bad: `invalid input -> 400; dependency failure -> 502`.

Good:

```text
Invalid input
  -> HTTP 400

Dependency failure
  -> HTTP 502
```

- Show allowed values as an alphabetical list or lookup table. Preserve every value.

Bad: `Pending; Failed; Complete`.

Good:

- `Complete`
- `Failed`
- `Pending`

- Format complete JSON examples in fenced `json` blocks with two-space indentation and separate lines for object members and array items. Preserve values, types, and numeric spelling such as `1.25e2`.

Bad: `{"amount":1.25e2,"tags":["a","b"]}`.

Good:

```json
{
  "amount": 1.25e2,
  "tags": [
    "a",
    "b"
  ]
}
```

- Follow the owning document's required formats. Apply agreed presentation conventions across the requested scope.

- Show logic or an algorithm as pseudocode when branching or execution order needs explanation and the real code is too long or too noisy to show:

```text
on(save)
  if content is unchanged
    return cached result
  write new content
  return fresh result
```

- Show runtime control flow as a call tree:

```text
submitForm
  createSession
    persistPrompt
    launchAgent
  navigateToSession
```

- Show UI structure as a component tree, including state and module boundaries that matter:

```tsx
<SessionPage> (apps/example/src/routes/session.tsx)
  useSessionEvents()
  <SessionToolbar>
    <RunSkillButton> (packages/ui)
```

- Show file responsibility or a broad refactor as a shallow file tree:

```text
src/
├── commands/       # parses user actions
├── sessions/       # owns session state
└── transport/      # sends API requests
```

- Draw states and transitions as a state diagram, data movement as a flowchart, and interactions between actors as a sequence diagram. Render each one as a PNG with [mermaid-png](../mermaid-png/SKILL.md).

- When a flow has too many parts to read in one diagram, show a short series instead. Each diagram redraws the previous one and adds one part.

- Use `diff` when the point is what changes and the surrounding shape already exists. Match the diff shape to the topic.

For a component change:

```diff
 <SessionPage>
   useSessionEvents()
   <SessionToolbar>
+    <RunSkillButton />
   <SessionTimeline>
+    <SkillResultCard />
```

For a file-layout change:

```diff
 src/
 ├── commands/
+│   └── show-me.ts       # expands the slash command
 ├── sessions/
-└── transport.ts
+└── transport/
+    ├── client.ts
+    └── stream.ts
```

For a call-tree or call-stack change:

```diff
 submitForm
   createSession
     persistPrompt
+    expandSkillMention
     launchAgent
-  navigateToSession
+  navigateToSession
+    subscribeToEvents
```

For a state or control-flow change:

```diff
 on(save)
-  write content
+  if content is unchanged
+    return cached result
+  write new content
+  invalidate cache
```

- Show the whole block when most of it is new, when omitted context would hide ownership or order, or when the user needs a copyable target shape:

```ts
function expandSkill(command: string): string {
  const skillName = command.slice(1)
  return `use the ${skillName} skill`
}
```

- For a visual UI, layout, state comparison, or concept too dense for a plain-text diagram, create one focused HTML page. For a chat reply in T3 Code, publish it as in-chat HTML; it stays in the chat. For a saved artifact, use [visual-explainer](../visual-explainer/SKILL.md) and save the page with the work item's `review/` files or the repository's docs. Match the product's colors, type, spacing, and components; use real labels and data; support desktop and mobile;

- Place each visual next to the short text it supports. Keep only the calls, files, props, states, and boundaries needed to answer the user's current question.

## Planning reviews and code walkthroughs

For planning reviews, lead with proposed flow → boundary contracts → architecture → brief implementation sequence. Expand implementation details when they affect a reviewed decision.

For “walk me through this” or “how does this work?”, orient the user to the capability, actors, and entrypoint; trace one concrete scenario through its boundary contracts; then show the architecture and discuss questions or zoom into a boundary. Use the evidence and diagram guidance below to describe existing behavior and distinguish observed behavior from inferred rationale.

When designing or evaluating code in any language, apply [coding-standards](../coding-standards/SKILL.md) and its relevant references. This presentation order does not reduce the required engineering checks. For a requested assessment of changes against standards and a spec, use [code-review](../code-review/SKILL.md).

## Developer review and discussion
- When this artifact is for human review before further work, follow [the review pause](../references/work-lifecycle.md#pause-for-human-review): present the ready view and decision needed, then end the turn. Do not advance dependent implementation or revise the review target while awaiting the answer.
- Show or link the acceptance contract. If the intended outcome is unclear, read [define-outcome](../define-outcome/SKILL.md). Distinguish required visual/behavior details from illustrative ones; tie review questions to unresolved criteria and identify required human decisions.

When iterating, show the current proposal, the meaningful change from the previous version, and the specific feedback or decision needed. Label experiments and accepted decisions separately. Retain a brief reason for rejected alternatives when it informs the discussion; avoid reproducing every prior version.

For work needing shared review, show the decision being discussed and choose the smallest useful format: an inline block, existing PR/document, or a focused artifact in the repository's `docs/` convention. Use Markdown with editable diagrams by default; use HTML when interaction or layout earns it. For local workspace review artifacts, use [shared audience placement](../references/context-routing.md#place-context-and-artifacts). Keep internal dispatch, commands, and recovery detail in linked agent notes; include consequential safety and rollback constraints in the human review. Publishing or attaching requires authorization; a local file path is not a shared URL.

Include only what the decision needs:

- Problem, constraints, and the review question in a few bullets.
- Current → proposed structure or behavior. Label proposed, observed, and inferred elements distinctly.
- Pseudocode, sequence/state diagrams, or concrete input/output/error examples. Show important failure paths, ordering, and ownership boundaries.
- Short rationale, tradeoffs, and open questions with decision owners when known.
- Observable acceptance criteria and verification approach; label checks not yet run as proposed.

Label pseudocode as pseudocode; do not imply it compiles. Link implementation sources and evidence for claims. Verify diagrams against those sources, and check rendering in the intended surface when possible; disclose when rendering is unverified.

Parse complete JSON examples without rewriting significant numeric tokens. Check that presentation edits preserve rule IDs, allowed values, verification limits, and unresolved questions. Check affected links and anchors.

For ongoing discussion, read [work-lifecycle](../references/work-lifecycle.md). Record accepted decisions and unresolved disagreements, then update visuals and affected plans after feedback. Preserve rationale needed by a fresh reviewer; avoid duplicating execution progress in the review artifact.

## Diagram images

Never show Mermaid text. Render each diagram to a PNG and place it with [mermaid-png](../mermaid-png/SKILL.md).
