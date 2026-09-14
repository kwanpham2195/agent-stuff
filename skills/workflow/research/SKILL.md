---
name: research
description: "Investigate an explicit research question or consequential uncertainty and report source-backed findings. Routine code exploration before an edit stays part of implementation."
---

For research spanning sessions or feeding a developer decision, read [work-lifecycle](../../references/work-lifecycle.md). Checkpoint the question, evidence, refuted claims, open disagreements, and next investigation step. Use [show-me](../../show-me/SKILL.md) when relationships or alternatives are clearer visually; label inferred and unverified behavior.

1. State the question, scope, and what evidence would answer it. Ask a focused clarification only when needed; use `grilling` for broader requirement discovery only when that work is requested. Routine inspection of code, callers, tests, and conventions does not require this workflow.
2. Read applicable repository instructions and their context pointers, relevant prior research, PRDs, and designs. Follow documented memory locations rather than assuming every project uses the same directories.
3. Gather evidence from source files, tests, docs, issues, logs, or official external sources. Record concrete paths/lines or URLs supporting findings. Distinguish observed behavior, source-code inference, and unverified claims; cite prior artifacts when reused and check whether their conclusions still hold.
4. Answer the question at the requested depth. For code behavior, distinguish what the implementation suggests from what tests or runtime evidence establish. Keep recommendations separate from findings. Stop when the evidence answers the question, or report the missing evidence and access needed; do not expand into unrelated investigation.
5. Return the answer, supporting sources, and unresolved questions. For substantial findings needed later, follow [context-routing](../../references/context-routing.md) to reuse or select the artifact home; use the actual research date. A bounded lookup can finish inline; do not create an artifact solely because this skill was used. Link saved findings from related plans rather than duplicating them.

## Findings format

Use the following order for substantial findings, whether inline or saved. A small lookup can use one paragraph with its source and limitation; no empty sections or mandatory file.

```text
Question and scope: what is being established; exclusions
Answer: direct conclusion and whether the question is settled
Evidence:
- Finding — observed / inferred / unverified — source path/lines or URL
Unknowns and conflicting evidence: what remains; how to resolve it
Implications: optional recommendations, clearly separated from findings
Next: next investigation or decision, or research complete
```

For a saved artifact, include the actual date and relevant source revision/environment. For example, “the handler contains a deduplication guard” is source evidence; “replayed requests create exactly one row” requires an observed execution or test result. If interrupted, retain the next probe and attempted approaches so another session can resume without repeating them.

Research-only requests finish with findings and the artifact path when one was written. Continue to planning or implementation only when already authorized. Follow the user's delegation preference; if delegating, read [delegated-execution](../../delegated-execution/SKILL.md).
