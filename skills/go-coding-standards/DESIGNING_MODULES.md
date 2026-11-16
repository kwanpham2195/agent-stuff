# Go package and module design

Apply [shared ownership, deletion test, and dependency categories](../coding-standards/references/modules-and-dependencies.md). Go package-level structure implements those responsibilities without mandatory architecture folders.

Define narrow interfaces at their consumer when real variation, translation, or substitution earns a seam. Prefer 1-3 cohesive methods; compose small interfaces when needed. Keep internal interfaces unexported. Do not introduce an interface just because a concrete implementation exists.

```go
type UserStore interface {
    FindActiveByEmail(ctx context.Context, email EmailAddress) (ActiveUser, error)
}
func NewPasswordReset(users UserStore, clock Clock) *PasswordReset
// Avoid requiring every method of a concrete mega-store.
```

Use explicit constructors for dependencies; avoid global time/randomness/loggers/clients/config. A required compatibility singleton stays at composition. Public capability names remain stable rather than consumer-qualified; consumer ownership of the interface does not require putting the consumer in its name.

## Decision records

Go retains its stronger existing rule: record a new production adapter/service decision in an ADR when it introduces an external dependency, platform capability, persistence model, runtime boundary, or dependency-provisioning pattern. Skip this for test-only fakes, one-file framework glue translating no policy, or methods added to an established cohesive adapter. Follow repository ADR requirements and [ADR format](../references/adr-format.md).

Shared helper ownership and resource rules live in [modules](../coding-standards/references/modules-and-dependencies.md) and [resources](../coding-standards/references/configuration-and-resources.md); no TypeScript `prelude.ts` or Effect mechanism is prescribed to Go. Package names/style follow [Go style](GO_STYLE.md).
