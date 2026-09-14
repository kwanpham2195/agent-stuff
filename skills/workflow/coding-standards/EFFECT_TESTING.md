# Effect testing

Apply the test levels, observable-outcome rules, and completion check in [`TESTING_AND_VERIFICATION.md`](TESTING_AND_VERIFICATION.md) to every Effect test. This reference adds Effect runtime, time, synchronization, and test-Layer rules.

## Defaults

- Use `it.effect` by default.
- Use `it.live` when real time or live runtime services are the behavior under test.
- Drive sleeps, schedules, retries, leases, and timeouts with `TestClock.setTime` or `TestClock.adjust`.
- Fork a sleeping effect before advancing `TestClock`.
- Assert interruption and finalization when they are observable parts of the behavior under test.

For retry or schedule tests, also read [`EFFECT_SCHEDULING_AND_RETRY.md`](EFFECT_SCHEDULING_AND_RETRY.md).

```ts
it.effect("finds a user", () =>
  Effect.gen(function* () {
    const users = yield* UserRepo.Service
    const result = yield* users.find(UserId.make("u1"))
    expect(Option.isSome(result)).toBe(true)
  }).pipe(Effect.provide(UserRepo.layerTest)),
)
```

## Explicit synchronization

- Use `Deferred` for one-shot readiness or completion signals.
- Use `Queue` to hand test-controlled work or observed events across fibers.
- Use `Latch` for reusable open/close coordination gates.
- Use `Ref` for shared test observation state.
- Coordinate through an existing lifecycle, status, or result interface. Put test-only controls on a test-control service; public interfaces expose observations required by production callers.

```ts
it.effect("publishes exactly once", () =>
  Effect.gen(function* () {
    const ready = yield* Deferred.make<void>()

    const fiber = yield* Effect.gen(function* () {
      yield* Deferred.succeed(ready, undefined)
      return yield* publisher.publishNext()
    }).pipe(Effect.forkScoped)

    yield* Deferred.await(ready)
    const message = yield* Fiber.join(fiber)

    expect(message).toEqual(expectedMessage)
  }),
)
```

## Reusable test implementations

Read [`EFFECT_SERVICES.md`](EFFECT_SERVICES.md#test-layers) before designing a reusable test Layer. When reusable state, failure injection, or observation belongs to a real service seam, expose a `TestService` for test control and inspection while production code continues through the real `Service` tag.

```ts
export interface Interface {
  readonly send: (message: Message) => Effect.Effect<void, SendError>
}

export class Service extends Context.Service<Service, Interface>()(
  "@app/Notifier",
) {}

export interface TestInterface extends Interface {
  readonly sentMessages: () => Effect.Effect<ReadonlyArray<Message>>
  readonly failNextSend: (error: SendError) => Effect.Effect<void>
}

export class TestService extends Context.Service<TestService, TestInterface>()(
  "@app/Notifier/Test",
) {}

export const layerTest = Layer.effectContext(
  Effect.gen(function* () {
    const sent = yield* Ref.make<ReadonlyArray<Message>>([])
    const nextFailure = yield* Ref.make<Option.Option<SendError>>(Option.none())

    const service = TestService.of({
      send: Effect.fn("Notifier.Test.send")(function* (message) {
        const failure = yield* Ref.getAndSet(nextFailure, Option.none())
        if (Option.isSome(failure)) return yield* Effect.fail(failure.value)
        yield* Ref.update(sent, (messages) => [...messages, message])
      }),
      sentMessages: Effect.fn("Notifier.Test.sentMessages")(function* () {
        return yield* Ref.get(sent)
      }),
      failNextSend: Effect.fn("Notifier.Test.failNextSend")(function* (error) {
        yield* Ref.set(nextFailure, Option.some(error))
      }),
    })

    return Context.empty().pipe(
      Context.add(Service, service),
      Context.add(TestService, service),
    )
  }),
)
```

Keep service members function-valued, including zero-argument operations, so `Effect.fn` applies uniformly. `Layer.mock` fits a tiny local partial implementation whose omitted members fail loudly when called.

## Configuration

For tests that provide runtime configuration or choose whether to exercise Config decoding, read [`EFFECT_CONFIGURATION.md`](EFFECT_CONFIGURATION.md#providers).

## Version audit

Effect 4 guidance here was audited against `effect@4.0.0-beta.85` and `@effect/vitest@4.0.0-beta.85`. Keep `effect` and `@effect/vitest` on the same version. Re-audit testing, schema-generation, and property-test assumptions when either package is upgraded.

Use `@effect/vitest` rather than `@fast-check/vitest` in Effect 4 codebases. Effect depends on Fast-Check, re-exports it from `effect/testing`, and `@effect/vitest` owns the integration.

In Vite+ projects, still run tests through `vp test`. If the package manager requires an explicit `vitest` peer for `@effect/vitest`, pin it to the exact Vitest version bundled by the installed Vite+ version.

## Property tests

- `it.prop` for synchronous properties over Fast-Check arbitraries.
- `it.effect.prop` for properties whose predicate returns an Effect, especially with Effect Schema or test services.

Property callbacks must assert or return a failing Effect when false. Merely succeeding with boolean `false` does not fail the test.

## Schema-derived generation

Effect Schema is the default source of valid generated domain values.

Prefer passing schemas directly to `it.effect.prop` or deriving with:

```ts
const arbitrary = Schema.toArbitrary(schema)
```

Built-in schema constraints should guide generation before rejection filtering. Use `Schema.toArbitrary(schema, { report: true })` while developing custom schemas to detect opaque-filter warnings.

Do not manually duplicate a schema's arbitrary in a separate factory unless the schema cannot derive an efficient or meaningful generator. Export custom arbitraries only when they add deliberate generation semantics or are reused independently.

For the audited Effect 4 beta versions:

- use tuple form when passing schemas to `it.effect.prop`;
- record form is safe for Fast-Check arbitraries;
- plain `it.prop` accepts Fast-Check arbitraries only;
- schema generation laws can use `TestSchema.Asserts`:
  - `.arbitrary().verifyGeneration()`;
  - `verifyLosslessTransformation({ params })`;
  - `decoding()` and `encoding()` focused assertions.

Re-check these compatibility notes after upgrading Effect or `@effect/vitest`.

## Completion check

The completion check in [`TESTING_AND_VERIFICATION.md`](TESTING_AND_VERIFICATION.md#verification-completion-criterion) passes; the test runtime matches the behavior under test; every temporal test drives time with `TestClock`, with sleeping effects started before the clock advances; concurrent readiness and ordering use explicit synchronization; reusable test implementations cross the production service tag while test controls remain on the test-control tag; observable interruption and finalization contracts are asserted; every applicable service, retry/schedule, and configuration pointer above has been followed; and every version-specific API was checked against the installed `effect` and `@effect/vitest` versions.
