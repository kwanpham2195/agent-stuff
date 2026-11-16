# TypeScript sensitive data and observability

Apply [shared diagnostics and redaction](../../coding-standards/references/sensitive-data-and-observability.md).

Use Effect's `Redacted.Redacted` in Effect codebases; otherwise use the established or local shared `Redacted<T>` wrapper. It must prevent accidental logging, inspection, and JSON serialization, not merely brand a raw string.

```ts
type ApiConfig = { readonly endpoint: Url; readonly token: Redacted<string> };
await fetch(endpoint, {
  headers: { authorization: `Bearer ${Redacted.value(token)}` },
  signal,
});
// Avoid token: string through application services.
```

```ts
logger.error("User lookup failed", {
  operation: "findActiveByEmail", provider: "postgres",
  errorTag: error._tag, userId: UserId.toTelemetryField(userId),
});
// Avoid JSON.stringify(cause) or logging unknown cause.message without classification.
```

Telemetry projections must emit approved fields under shared policy. Inspect framework HTTP spans/reporters at their capture owner, including URLs, redirects, headers, bodies, and causes; [Effect HTTP clients](effect-http-clients.md) supplies library detail when applicable.
