# Configuration and resources

Read environment/runtime configuration once at startup or the earliest composition boundary. Parse into meaningful values and pass them inward. Known missing/invalid configuration uses [expected failure contracts](errors.md); startup renders a safe diagnostic and may terminate. Credentials follow [sensitive-data rules](sensitive-data-and-observability.md).

Entrypoints/bootstrap own top-level effects and resource acquisition, lifetime, and release. Non-entrypoint imports remain inert: do not start servers, open connections, read environment, register handlers, or perform I/O during import/initialization.

Confine mutable singleton/global state to framework/composition boundaries. Immutable constants and pure lookup tables are ordinary values. A required synchronized cache or singleton has explicit lifecycle/ownership and documentation; libraries do not force callers into global APIs.

Time, randomness, and ID generation are explicit capabilities in dependency-bearing modules. Pure functions accept concrete timestamps/generated values. Consequential production randomness, including security, identifiers, sampling, fairness, and user-visible outcomes, uses runtime cryptographic randomness behind an injectable capability.

Each acquired resource has one owner that releases it on success, failure, and cancellation/interruption. Detached work uses an explicit lifetime owner; see [workflows](workflows-transactions-and-idempotency.md).

## Completion

Every configuration source is parsed once at composition, failures are safe native errors until startup rendering, every resource has a complete lifetime, imports stay inert, global state stays contained, and time/randomness/IDs enter through explicit inputs or capabilities.
