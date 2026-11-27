---
name: show-me
description: "Explain technical work or prepare developer review artifacts with diagrams, structural diffs, short code, pseudocode, and concrete contracts."
---

Make the subject at hand easier to grasp with a visual. Lead with the view rather than an introduction, and keep the text around it short. Pick whichever format is smallest while still carrying the main point.

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

- Put each visual next to the brief text it backs up, and include only what bears on the question being asked: the calls, files, props, states, and boundaries involved.

- For a runtime question such as "what calls what", draw a call tree:

```text
handleCheckout
  reserveStock
    lockInventoryRows
    writeReservation
  chargeCard
  sendReceipt
```

- For ownership questions or a sweeping refactor, sketch a shallow directory tree with a comment on each entry:

```text
app/
├── routes/         # maps URLs to handlers
├── billing/        # owns invoices and payments
└── clients/        # wraps outbound API calls
```

- For UI structure, draw the component hierarchy and mark any state or module boundary that affects the answer:

```tsx
<CartScreen> (src/routes/cart.tsx)
  useCartTotals()
  <CartSummary>
    <PromoCodeField> (src/components/promo)
```

- When branching or ordering is the point and the real code is too long or too noisy, write pseudocode:

```text
when(upload arrives)
  if the checksum matches a stored file
    reuse the stored file
  else
    store the bytes
    record the checksum
  reply with the file id
```

- Draw states and transitions as a state diagram, data movement as a flowchart, and interactions between actors as a sequence diagram. Render each one as a PNG with [mermaid-png](../mermaid-png/SKILL.md).

- If a flow has too many parts for one diagram, split it into a short series. Each diagram repeats the one before and adds a single part.

- A `diff` block fits when the reader cares about what changes and already knows the overall shape. Format the diff to look like the subject it modifies.

Components:

```diff
 <CartScreen>
   useCartTotals()
   <CartSummary>
+    <ShippingEstimate />
   <CartFooter>
+    <SavedForLaterList />
```

Directories:

```diff
 app/
 ├── routes/
+│   └── export.ts        # serves the CSV export
 ├── billing/
-└── gateway.ts
+└── gateway/
+    ├── http.ts
+    └── retry.ts
```

Call trees:

```diff
 handleCheckout
   reserveStock
     lockInventoryRows
+    checkBackorderLimit
     writeReservation
-  chargeCard
+  chargeCard
+    recordLedgerEntry
```

Control flow:

```diff
 when(upload arrives)
-  store the bytes
+  if the checksum matches a stored file
+    reuse the stored file
+  else
+    store the bytes
+    record the checksum
```

- Print the code in full if most of it is new, if trimming it would obscure ownership or sequencing, or if the reader wants a shape to copy:

```ts
export const toSlug = (title: string) =>
  title.trim().toLowerCase().replace(/\s+/g, "-")
```

- Build one focused HTML page when the topic is a UI, a layout, a side-by-side of states, or an idea too dense for plain text. For a chat reply in T3 Code, publish it as in-chat HTML; it stays in the chat. For a saved artifact, use [visual-explainer](../visual-explainer/SKILL.md) and save the page with the work item's `review/` files or the repository's docs. Borrow the product's palette, type, spacing and components, fill the page with real labels and data, and check that it holds up on both desktop and mobile.

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
