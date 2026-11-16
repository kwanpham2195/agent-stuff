# Go observability

Apply [shared sensitive data and diagnostics](../coding-standards/references/sensitive-data-and-observability.md). Use established Go logging/tracing/reporting mechanisms, not Effect wrappers or a TypeScript generic.

Use a project-native protected secret value whose formatting/serialization is redacted. Keep raw fields inaccessible to accidental logging and expose raw data only at final I/O. Check formatting and marshaling paths, not just one log call.

```go
logger.ErrorContext(ctx, "merchant lookup failed",
    "operation", "findByID", "provider", "postgres",
    "errorKind", safeErrorKind(err), "merchantID", approvedID)
// Avoid logging arbitrary request structs, credential-bearing errors, or raw causes.
```

Pass context through adapter work for established trace correlation. Keep `errors.Is`/`errors.As` classification and safe fields separate from raw error serialization. Native error strings follow [Go error style](ERROR_HANDLING.md); automatic HTTP/RPC reporting still needs checking at its actual capture owner.
