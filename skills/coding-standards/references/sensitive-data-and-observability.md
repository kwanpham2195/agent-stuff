# Sensitive data and observability

Use established tracing, logging, metrics, and reporting hooks. Preserve active correlation/trace context across changed requests, jobs, workflows, adapters, and external calls. If no mechanism exists, report that fact rather than inventing one incidentally.

Keep domain decisions independent of telemetry. Pure code returns decisions and may expose explicit safe projections; the imperative shell observes them.

Wrap tokens, API keys, passwords, raw credentials, and secrets at the input boundary in a representation that prevents accidental logging, inspection, and serialization. Preserve protection through application code and unwrap only at the final-I/O owner requiring raw data. Use the language/project's appropriate wrapper rather than prescribing one generic type syntax.

Treat personal data as private by default. Emit only minimal approved fields after required minimization/sanitization. Domain IDs are safe only when approved, not merely because they are IDs.

Errors, logs, traces, metrics, reports, snapshots, and panic summaries contain only redacted secrets and approved personal-data representations. Never serialize arbitrary values, causes, environment, request bodies, or entire domain objects for diagnostics.

```text
Prefer: operation + provider + stable error category + approved ID + retry count + state
Avoid:  serialize the caught value or request payload for "more context"
Avoid:  log only "failed" without correlation or meaningful classification
```

Use bounded summaries derived from allowlisted fields. A defect helper receives safe explicit context, not the whole object.

Inspect automatic instrumentation as well as logs. Framework spans/reporters may capture URLs, headers, redirects, bodies, or causes before inner middleware. Apply redaction/allowlisting at the actual capture/report owner, preserving safe correlation, failure classification, and interruption. Test the emitted interface with representative sensitive input; protecting one application field does not prove a framework-generated cause safe.

## Completion

Secrets stay protected from ingress to final I/O; each diagnostic field is approved/minimized/redacted; changed failures retain applicable operation, safe ID, provider, category, and retry/state context; established hooks and correlation remain connected; automatic capture is checked at its real owner; domain logic stays independent.
