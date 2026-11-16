# Modules and dependencies

A module is any unit with an interface and implementation: a function, class, file, package, service, or adapter. Its interface includes signatures, invariants, ordering, failure modes, configuration, performance, and side effects. A seam lets behavior vary without editing its caller.

## Responsibilities

Names describe responsibilities, not required folders or language constructs:

- Domain module: owns intrinsic meaning, invariants, calculation, parsing, value behavior, and legal transitions. It is pure and independent of I/O, frameworks, persistence, ambient time/randomness, and mutable globals.
- Application service: owns cohesive application policy, authorization enforcement, effect sequence, and dependency failure classification. It accepts application/domain values and exposes precise native failure contracts.
- External adapter: owns protocol, framework, database, runtime, SDK, and third-party translation/mechanics. Inbound adapters parse then render outcomes; outbound adapters implement application-owned capabilities.
- Composition root: constructs, wires, and owns top-level resources.

```text
external input -> inbound adapter -> application service -> domain decisions
                                       |
                                       -> capability -> outbound adapter -> external system
                                       -> private concrete client -> external system
```

An inbound adapter may call pure domain behavior directly with parsed input. Pure permission decisions belong in domain code; inbound adapters verify credentials and produce parsed actors; services gather context and enforce permissions; adapters render missing/denied outcomes. Use domain-specific authorization evidence, not an invented generic access bag.

## Cohesion and deletion test

A module owns one cohesive concept, capability, or policy. Its low-burden interface hides meaningful complexity, invariants, sequencing, and incidental steps. Callers should say what they want without knowing unrelated methods, raw records, hidden effects, nullable state bags, or internal ordering.

Apply the deletion test before adding or preserving an abstraction:

```text
Earned: deleting it spreads meaningful translation/policy/complexity across callers
Unearned: deleting a forwarding wrapper makes complexity disappear
```

Check existing owners, services, clients, schemas, errors, and helpers before adding one. Reuse a capability as-is; extend it only when the added behavior shares its owner and reason to change. A concrete client may remain private when an adapter would only forward. Its owner still translates failures before they cross the public contract. Extract an adapter for meaningful mechanics/translation, reuse, or real variation.

Weigh reader load on two axes: layers to trace between a question and its answer, and state the reader must hold. Prefer the narrowest state scope: a returned value, then a local, a field, module state and, last, a global. Derive values instead of syncing copies. A new reader should answer "where does X come from, and what can change it?" in under 30 seconds. Do not split modules by pipeline phase, such as load, validate, transform and save; phase-named modules repeat the same domain rules in each step. Repeated workarounds, recurring special cases, or callers that need internal rules show a wrong shape; reconsider the design before adding another special case.

For each new abstraction, report owners/direct implementations considered and why reuse or extension does not fit. Keep lasting rationale beside owning code or in existing decision documentation; follow repository ADR policy.

## Interfaces and dependency ownership

Design meaningful capabilities from caller-facing inputs, outputs, failures, and contracts before implementation, using native language constructs. Compose rather than inherit except for framework requirements or genuine substitutability. Depend on the smallest cohesive behavior, not every method of a concrete repository; avoid an interface for every class/method by habit.

Make services, configuration, clocks, randomness, and IDs explicit dependencies. Keep operation-specific authorization evidence and scoped handles explicit inputs. Use callbacks when higher-order behavior is itself the capability. Avoid dependency bags repeatedly passed through calls; concentrate lifetime and dependency ownership at the owning service/composition root.

Broader services compose smaller cohesive capabilities only after those seams earn their place. Keep policy and effect order visible while delegating substantial calculations and reusable mechanisms to their owners. Entrypoints do not duplicate shared business policy.

Name capabilities for stable domain/operational meaning, such as UserStore or EmailSender, not their current consumer. Put specific behavior in operation names. Architecture suffixes belong only where they describe established meaning. Dependency variables name their held object without naming-only churn; implementation qualifiers identify observable/provider differences, not construction trivia.

## Dependency categories

- In-process computation/memory: test directly through its interface and deepen freely.
- Local-substitutable infrastructure: use representative local substitutes when SQL/filesystem/protocol semantics matter; do not add a port solely for testing.
- Remote owned service: define a transport seam, with a production transport and faithful test adapter.
- True external service: inject a meaningful capability and replace through that seam in tests.

Follow these categories alongside the deletion test. A private concrete client remains legitimate until a separate capability earns ownership.

## Complexity and discoverability

Use active complexity policy without hiding domain decisions or effect order. Extract one owned calculation, translation, persistence operation, or policy, retaining exact inputs, failures, dependency requirements, transaction scope, resource lifetime, and ordering. Fewer branches do not justify forwarding helpers, generic machinery, option bags, or dispatch indirection.

Remove reads/validation only after tracing producers and distinct invariants. Compare runtime work separately from API/type-only substitutions. Improve cohesion rather than weakening lint or splitting merely to satisfy a metric.

Files/packages have searchable subjects and cohesive owners, not arbitrary size limits. Stable generic helpers have specific subjects; domain/application policy stays with its owner, not miscellaneous utilities. Export only intentional consumer/public contracts. Review public, dynamic, type-only, and external consumers before changing exports; a test-only hit is not application demand and no local hit does not prove a public API dead. Apply compatibility policy.

## Completion

Every operation is traced to effects and observable outcomes, each concern has one owner, dependencies are explicit, framework/provider details stay private, and every abstraction has deletion-test and existing-owner evidence. Extraction preserves effect/failure/lifetime semantics, naming remains meaningful, and public contracts retain intentional consumers and documentation.
