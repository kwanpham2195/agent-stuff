# TypeScript modules, services, and adapters

Apply the [shared ownership and deletion test](../../coding-standards/references/modules-and-dependencies.md). The roles below describe responsibilities; they do not require particular TypeScript constructs or folder layouts.

Domain logic may be plain functions, immutable value classes, or static-style classes. A service with dependencies in plain TypeScript gets an interface plus an implementation class that receives its collaborators as service objects through the constructor; capabilities tied to a single operation remain explicit arguments. For Effect services, tags, `make`, layers, and requirements, see [Effect services](effect-services.md).

## Naming capabilities

Name a capability for what it does, not for one consumer (avoid `UsersForPasswordReset`). When the interface and its normal implementation would naturally share a name, prefix the interface with a short `I`:

```ts
export interface IMailer {
  sendReceipt(order: Order): Result<void, SendReceiptError>;
  sendShippingNotice(order: Order): Result<void, SendShippingNoticeError>;
}
export class Mailer implements IMailer { /* ... */ }
```

When implementation names are naturally distinct, skip the prefix:

```ts
export interface CustomerDirectory {
  findByPhone(phone: PhoneNumber): Promise<Result<Customer, CustomerLookupError>>;
}
export class SqlCustomerDirectory implements CustomerDirectory { /* ... */ }
export class AccountRecovery {
  constructor(private readonly customers: CustomerDirectory) {}
}
```

A concrete class with a wider surface may satisfy a consumer's narrower interface. Do not create an interface for every single method when no real seam exists.

## When an adapter is justified

A `Mailer` can use a private `SendgridClient` directly while a separate `MailSender` would only pass calls through. Add the sender abstraction, with provider-specific implementations, once there is real variation or meaningful protocol work behind it. Run the shared check for an existing owner first, and report why reusing or extending it does not work.

## Reducing complexity without losing cohesion

Whatever you extract must keep the exact success and error types and Effect requirements, along with ordering, transaction, and resource rules from the shared guidance. Fewer branches do not mean less work for the caller. Follow the [lint policy](lint-and-policy.md), and do not split code only to satisfy a metric.

Where generic helpers and files live is covered in [imports and files](imports-exports-and-files.md). Keep domain and application policy out of `prelude.ts` and utility grab-bags. In Effect, pass dependencies as context capabilities, not as ad hoc bags of values.
