---
name: write-discoverable-code
description: "Use when naming or renaming symbols, files, errors, and doc comments. Keeps changed code discoverable through text search."
license: MIT
---

Make changed code easy to locate and understand from a search result. Apply the following flow to the code in scope; it does not authorize a repository-wide naming cleanup.

## 1. Find the existing vocabulary

Inspect nearby symbols, filenames, callers, and tests. Reuse the repository's spelling for each concept. Identify framework-required names and public contracts before renaming anything.

## 2. Name the concept and action

Use the shortest exported name that identifies its domain and purpose without reading the import path. Qualify generic verbs and filenames only where local conventions do not already provide a clear meaning.

```text
sanitize             → sanitizeEmailHtml
validateConfig       → validateSmtpConfig
utils.ts             → billing-period.ts  (if that is the concept it owns)
```

The examples show intent, not a mandatory word count. Keep conventional names such as a framework's `page.tsx`, Go's `billing.Parse`, or a repository's intentional `Input`/`Output` exports when their context is established. Reuse `orgId` if that is the existing domain spelling; do not introduce `organizationId` for the same concept.

Rename stale names when behavior or audience changes, within the task's API compatibility contract. Update callers and tests in scope. Do not break a public name solely to make search easier.

## 3. Preserve searchable literals and constraints

Keep finite event names, flags, and error codes as full literals. Keep a stable phrase at an error's source; dynamic details can follow it.

```text
Hard to locate: `${entity}.${action}`          // known event assembled at runtime
Searchable:    "invoice.paid"

Hard to locate: `${prefix}: mismatch`
Searchable:    `Webhook signature mismatch for ${requestId}`
```

Put constraints callers cannot infer from a signature at the definition: units, timezone, ownership, ordering, or failure conditions. Add natural-language terms when they help searches, without duplicating the name as a sentence.

```text
Repeats the name:  /** Checks whether the session has expired. */
Adds a contract:  /** Session expiry uses server UTC time; equality counts as expired. */
```

Write only constraints supported by the implementation or agreed contract. These examples do not establish project behavior.

## 4. Give the implementation one home

Keep each shared implementation in one concept-named module. Thin orchestrators should point to that module; avoid both unrelated concepts in one large file and a file per trivial helper. Colocate tests when supported by repository convention.

When moving code, inspect references to the old location and remove the obsolete implementation if authorized. If a contract requires retaining a deprecated path, point it to the replacement rather than maintaining a second implementation.

## 5. Check the changed surface

Before finishing, search for the new public names and stable error/event literals. Confirm the definition and relevant callers are easy to locate, old references are accounted for, and comments add constraints rather than narration. Use normal language/tooling checks for renamed callers. No separate discoverability report is required unless requested; report material exceptions or compatibility limits.

Type modeling, parsing, privileged-operation contracts, and test design belong to [coding-standards](../coding-standards/SKILL.md) for TypeScript and Go; follow local precedent in other languages.
