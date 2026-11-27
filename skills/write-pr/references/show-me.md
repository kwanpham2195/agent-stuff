---
name: show-me
description: Make a topic easier to grasp with a small picture, such as a sketch of code structure, a tree, a diff, or a rendered diagram.
---

Reach for a picture when it explains faster than a paragraph would. Go straight to it, write only the text it needs, and choose the lightest form that carries the point.

## Choosing a form

| What you are explaining                        | Form                       |
| ---------------------------------------------- | -------------------------- |
| Decision logic or an algorithm                 | Pseudocode                 |
| Order of calls at runtime                      | Indented call tree         |
| Screen or component layout                     | Component tree             |
| Which module owns what, or a large reshuffle   | Shallow directory tree     |
| How parts talk to each other, or data movement | Diagram rendered as image  |
| A change to something that already exists      | `diff` block               |
| A new thing the reader may copy                | Complete code block        |

Diagrams are never pasted into a PR as Mermaid source. Render them to PNG and attach the image with `gh pr edit --attach`, following [mermaid-png](../../mermaid-png/SKILL.md).

## Forms in detail

### Pseudocode

Use it for rules and algorithms. Keep the branching visible and leave out syntax.

```text
on(upload)
  if file already stored under the same hash
    return the existing link
  store the file
  return a new link
```

### Call tree

Indent each call under the one that makes it, in execution order.

```text
handleCheckout
  validateCart
  chargeCard
    createPayment
    confirmPayment
  sendReceipt
```

### Component tree

Draw the nesting, and note a state hook or a package boundary only when it affects the point being made.

```tsx
<OrderPage> (web/src/pages/order.tsx)
  useOrderQuery()
  <OrderHeader>
    <CancelButton> (shared/ui)
```

### Directory tree

Show one or two levels, with a short comment for each entry's job.

```text
server/
├── routes/      # maps URLs to handlers
├── billing/     # owns invoices and payments
└── queue/       # runs background work
```

### Diff

Choose a diff when the reader already knows the base and needs to see only what moved. Mark added lines with `+` and removed lines with `-`, and keep unchanged lines that anchor the position. The same style works for any of the forms above.

A component tree after a change:

```diff
 <OrderPage>
   useOrderQuery()
   <OrderHeader>
+    <RefundButton />
   <OrderItems>
+    <RefundBanner />
```

A directory tree after a change:

```diff
 server/
 ├── routes/
+│   └── refunds.ts      # handles refund requests
 ├── billing/
-└── invoices.ts
+└── invoices/
+    ├── create.ts
+    └── void.ts
```

A call tree after a change:

```diff
 handleCheckout
   validateCart
   chargeCard
+    checkFraudScore
     createPayment
-  sendReceipt
+  sendReceipt
+    recordAuditEntry
```

Logic after a change:

```diff
 on(upload)
-  store the file
+  if file already stored under the same hash
+    return the existing link
+  store the file
+  index the hash
```

### Full block

Show the whole thing, not a diff, when most of it is new, when leaving out the surroundings would blur who owns what or in which order things run, or when the reader will copy it.

```ts
function parseRetryHeader(value: string | null): number {
  const seconds = Number(value)
  return Number.isFinite(seconds) ? seconds * 1000 : 0
}
```

## Placement

Put each picture beside the sentence or two that explains it. Include only the calls, files, props, states, and boundaries that bear on the user's current question. Leave the rest out.
