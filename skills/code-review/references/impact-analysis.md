# Impact analysis

Use within [code review](../SKILL.md) when a change relies on consequential safety or compatibility assumptions, or when the user requests impact analysis. Keep Standards and Spec findings separate as the owner requires.

1. Identify the changed contract and trace affected callers, entry points, consumers, persisted data, and external effects. Follow concrete dependencies far enough to identify consequences; do not expand into a repository-wide audit without evidence. Look where a symbol search stops: the called library's own source, its pinned version and any local patch; when code runs, such as teardown, microtasks and lifecycle order; data another reader consumes, such as an API's JSON, a database column or a wire format read by another language; feature flags; and code several hops downstream. When an assumption depends on the order of events, such as retries, timeouts or concurrent callers, reading cannot settle it; model it with [statechart](~/.agents/skills/statechart/SKILL.md) as [matthew-mode](../../matthew-mode/references/capabilities.md#diagnostics-and-visual-evidence) describes.
2. State each assumption whose failure could cause a regression. Examples include an authorization check covering every entry point, a retry preserving idempotency, an old persisted value remaining readable, or a renamed symbol having no external consumers. Select assumptions relevant to this change rather than treating these examples as a checklist.
3. For each assumption, record its supporting source, what would falsify it, the consequence if false, and the smallest useful check. Search callers and configuration for reachability; inspect tests for actual coverage. An absence claim needs an exhaustive search over a named scope and a statement of what lies outside it.
4. Verify consequential assumptions with existing tests or authorized isolated probes through the affected interface. Check failure paths and side effects where relevant. Source reasoning can identify a risk but cannot establish unexecuted runtime behavior. Review-only authority does not permit source edits, deployments, data mutation, or new external access; report unavailable proof as blocked. Start with the one fact the change is safe because of; if it holds, it often clears most other risks. Take each consequential assumption as far up this ladder as is cheap and authorized, and record the level reached: (1) stated; (2) pointed at a `file:line` or the library's own source; (3) walked step by step until the bad case cannot occur; (4) run by a script or test against the real code; (5) reproduced in the running app.
5. Report confirmed defects with the affected contract, evidence, and consequence under the applicable review axis. Keep speculative risks and unverified assumptions distinct from confirmed defects. Recommend further investigation or verification when the consequence warrants it; do not invent compatibility machinery or remove functionality to close a finding.

For each material assumption, return a compact record:

```text
Assumption and affected contract:
Evidence and search bounds:
Falsifying case and consequence:
Check actually run and result, or missing proof:
Proof level reached (1-5):
Finding and review axis, or residual uncertainty:
```

Stop when consequential assumptions are supported, refuted, or explicitly blocked. A clean diff review does not prove safety for consumers or environments outside the examined scope.
