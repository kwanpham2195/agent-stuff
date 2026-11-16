# TypeScript errors

Apply [shared failures and defects](../../coding-standards/references/errors.md). Every known failure appears as a custom tagged error in the return type, even if the immediate caller cannot recover.

Use Effect's typed error channel in Effect projects; `better-result` when available/accepted in scope; otherwise the established result shape or a small local tagged union. Do not add an error dependency merely from preference. Outside Effect, prefer `better-result`'s `TaggedError` for custom expected-error classes when available even if Result itself is not adopted.

```ts
type Result<T, E extends Error> =
  | { readonly _tag: "ok"; readonly value: T }
  | { readonly _tag: "err"; readonly error: E };
// Prefer:
function findUser(id: UserId): Promise<Result<User, UserNotFound | UserStoreUnavailable>>;
// Avoid: Promise<User> rejecting for ordinary absence/storage failures
```

Promise rejection is throwing. The direct third-party owner catches unknown rejection and classifies it before it crosses the module interface. Check cancellation first. Framework-required throws stay at the framework boundary; encode/document distinguishable public expected variants with its mechanism.

Custom errors extend `Error`, `better-result`'s `TaggedError`, or the pinned [Effect Schema error constructor](effect-schema-and-data.md#errors). Use a stable `as const` tag, safe structured fields, useful stable message, and optional `cause: unknown`.

```ts
export class UserStoreUnavailable extends Error {
  readonly _tag = "UserStoreUnavailable" as const;
  constructor(
    readonly operation: "findActiveByEmail",
    readonly provider: "postgres",
    readonly cause: unknown,
  ) {
    super(`User store unavailable during ${operation}`);
  }
}
```

Required lookup returns `UserNotFound`; intentional optional lookup may return `User | undefined` or Effect `Option`. Keep precise operation unions, not `Result<User, AppError>`.

Reuse established defect helpers where semantics/reuse earns them; otherwise keep local or native:

```ts
casesHandled(unexpectedCase: never): never;
shouldNeverHappen(message?: string): never;
notYetImplemented(message?: string): never;
```

Known configuration failures remain typed until startup safely reports/terminates.

## Boundary translation

For tagged Effect unions prefer `Effect.catchTag`/`catchTags` to preserve explicit category policy and unchanged application errors. New tags remain visible in inference. Use `Effect.mapError`/shared mappers only when the whole input channel intentionally has one meaning, retaining concrete errors and requirements. Defects/interruption and cause-level supervision follow shared rules.
