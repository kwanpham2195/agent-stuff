# Comments and JSDoc

The [shared documentation rules](../../coding-standards/references/documentation.md) cover audience and tone. TypeScript adds the points below.

## Documenting fields

Explain properties of exported object types when their meaning goes beyond name and type.

```ts
/** Settings for one outgoing call. */
export type CallSettings = {
  /** Upper bound for the whole call, retries included. */
  readonly deadline: Duration;

  /** Identifier handed, unchanged, to every downstream service. */
  readonly traceId: TraceId;
};
```

## `@throws`

Reserve it for unrecoverable defects, behavior a framework demands, and `notYetImplemented` placeholders. Expected typed failures belong in the `@returns` text or in the operation's description.

## Type parameters

Use `@template` when a parameter's role or limits are not clear from the signature.

```ts
/**
 * Convert the success value, leaving any failure untouched.
 *
 * @template E - Failure type, passed through unchanged.
 * @param convert - Applied only when `outcome` succeeded.
 * @returns The converted success, or the original failure.
 */
export function mapOutcome<A, B, E>(outcome: Result<A, E>, convert: (a: A) => B): Result<B, E>;
```

## What gets a doc comment

- Every exported symbol, written where it is first declared.
- The public methods and properties of an exported class.
- Not re-exports: they rely on the original comment. Write the text out instead of using `@inheritDoc`.

Place the `/** ... */` block directly above the declaration, and include only tags that tell a caller something the signature does not.

```ts
/**
 * Validate a postal code received from an untrusted source.
 *
 * @param raw - The unchecked text from the caller.
 * @returns A `PostalCode`, or `InvalidPostalCode` when the text is rejected.
 */
export function parsePostalCode(raw: string): Result<PostalCode, InvalidPostalCode>;
```

## Checklist

Shared documentation rules pass, every exported symbol and public class member is documented at its declaration, no `@inheritDoc` shortcuts remain, unclear fields are explained, and tags follow the points above.
