# TypeScript modules, services, and adapters

Apply [shared ownership and deletion test](../../coding-standards/references/modules-and-dependencies.md). Roles describe responsibilities, not required TypeScript constructs or folders.

Plain functions, immutable value classes, and static-style classes are valid domain implementations. Dependency-bearing plain TypeScript services use explicit service interfaces and implementation classes with constructor-injected service objects. Operation-specific capabilities remain explicit inputs. Effect services, tags, `make`, Layers, and requirements follow [Effect services](effect-services.md).

## Capability names

Use stable capability names, not consumer-qualified `UsersForPasswordReset`. When interface and ordinary implementation naturally share a name, use a compact `I` prefix:

```ts
export interface IEmailService {
  sendWelcomeEmail(...): Result<void, SendWelcomeEmailError>;
  sendPasswordResetEmail(...): Result<void, SendPasswordResetEmailError>;
}
export class EmailService implements IEmailService { /* ... */ }
```

Naturally distinct implementation names need no prefix:

```ts
export interface UserStore {
  findActiveByEmail(email: EmailAddress): Promise<Result<ActiveUser, UserLookupError>>;
}
export class PostgresUserStore implements UserStore { /* ... */ }
export class PasswordReset {
  constructor(private readonly users: UserStore) {}
}
```

A wider concrete implementation can satisfy a narrow consumer contract. Avoid interface confetti such as a named interface for every individual method without a meaningful seam.

## Adapters and concrete clients

An EmailService may use a private ResendClient while EmailSender would only forward. Introduce EmailSender with ResendEmailSender/MailgunEmailSender when variation or meaningful mechanics earns it. Apply the shared existing-owner audit and report why reuse/extension does not fit.

## Cohesive complexity reduction

Preserve exact TypeScript success/error types and Effect requirements through helpers, along with shared ordering, transaction, and resource constraints. A lower branch count does not prove reduced caller burden. Follow [lint policy](lint-and-policy.md) without weakening enforcement or partitioning solely to fit metrics.

Generic helpers and file placement follow [imports and files](imports-exports-and-files.md). Keep domain/application policy out of `prelude.ts` or utilities. Effect uses context capabilities rather than ad hoc dependency bags.
