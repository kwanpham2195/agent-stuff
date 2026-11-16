# Domain values and state

Use semantic domain types for every domain/entity identifier, mixable unit, and constrained scalar. Construct them through parsers or smart constructors that establish their invariants. Keep display text, counters, indexes, and implementation-only values primitive until they gain domain meaning or a realistic mix-up risk. Reuse existing concepts when their vocabulary and invariant match.

Keep value objects immutable and pure. They own value behavior, not infrastructure dependencies or I/O. Caller code does not reimplement constructor or transition invariants.

## Operation inputs

Push optionality outward. Branch or parse before calling an operation that requires a value. Use explicit operation inputs rather than broad entity records or partial-field bags, unless partiality is the actual domain concept, such as an owned patch command.

Keep the primary input obvious. Add named options when real callers select related policies or names prevent argument-order mistakes. Each option must change caller-required behavior. Keep zero/one-input operations simple; library parse options remain private unless deliberately part of the public contract.

Use independent booleans when all combinations are valid and booleans for predicate results. Behavior controls use named policies or domain values.

```text
Prefer: createUser(input, emailVerification = skip)
Avoid:  createUser(input, true)
Prefer: isExpired(token) returns a boolean
```

These examples express contracts, not required syntax.

## Lifecycle

When states permit different data, operations, or transitions, use state-specific representations and legal transition functions. A simple status plus a transition function suffices when it expresses all lifecycle rules.

```text
Prefer:
  Draft invoice carries nonempty lines
  Sent invoice carries sentAt
  Paid invoice carries paidAt
  markPaid accepts Sent and produces Paid
Avoid:
  isSent + isPaid + optional sentAt + optional paidAt
  markPaid accepts any state and trusts callers to check it
```

Handle closed variant sets exhaustively using the language's native mechanism or explicit coverage of all states. Do not silently swallow future variants. At open external protocols, define and test an explicit unknown-variant policy.

For persisted invariants, use constraints, uniqueness, and guarded writes where practical as well as read-time parsing. Reject contradictory rows rather than normalizing away invalid authority.

## Completion

Every changed identifier, unit, constrained value, input, option, boolean, and lifecycle has an intentional representation and owner. Constructors and transitions establish invariants; required inputs are present before calls; closed states are exhaustive and open protocols have tested fallback policies; persisted invariants have boundary parsing and appropriate storage guards. Report compatibility constraints that prevent a local application.
