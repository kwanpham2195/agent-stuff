# TypeScript domain types and state

Apply [shared domain policy](../../coding-standards/references/domain-types-and-state.md).

Use brands/refined types for domain IDs, mixable units, and constrained scalars. Prefer the owning schema's branding/refinement over handwritten casts. Keep ordinary display strings and counters primitive.

```ts
function parseUserId(input: string): Result<UserId, InvalidUserId> {
  if (!isCanonicalUserId(input)) return err(new InvalidUserId(input));
  // SAFETY: the parser established the invariant; TypeScript cannot express the brand.
  return ok(input as UserId);
}
// Avoid: const id = body.userId as UserId;
```

A value class is immutable, constructs through private constructors plus parsers/smart constructors, and owns only pure value behavior. Do not put database reservation or hidden dependencies on a value object.

Use `Partial<T>` only for actual domain partiality, not convenient command inputs. Keep primary input positional; add a named options object for earned policies, such as `createUser(input, { emailVerification: "skip" })`. Predicates such as `isExpired(token): boolean` remain appropriate.

Prefer string-literal/discriminated unions over TypeScript `enum`; numeric enums require external interop. Use `_tag` unless another discriminant is actual domain vocabulary.

```ts
type Invoice =
  | { readonly _tag: "Draft"; readonly id: InvoiceId; readonly lines: NonEmptyArray<LineItem> }
  | { readonly _tag: "Sent"; readonly id: InvoiceId; readonly sentAt: Instant }
  | { readonly _tag: "Paid"; readonly id: InvoiceId; readonly paidAt: Instant };
// Avoid: { isSent: boolean; isPaid: boolean; sentAt?: Date; paidAt?: Date }
function markPaid(invoice: SentInvoice, paidAt: Instant): PaidInvoice;
```

Prefer `switch` for three or more closed variants. Use the established exhaustive `never` helper described in [errors](errors.md); do not swallow new variants in a default. External open protocols instead need the shared tested fallback policy. In Effect, intentional absence may use `Option`.
