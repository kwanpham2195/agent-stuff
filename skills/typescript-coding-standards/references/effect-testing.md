# Testing with Effect

General rules for tests are in [general testing guide](testing.md). This file adds the Effect-specific mechanics.

## Quick review

Does [general testing guide](testing.md#completion-check) pass? Does the runner suit the subject? Is all timing driven by the test clock? Is coordination explicit? Are fakes reached through the real tag? Is visible cancellation or cleanup asserted?

## Configuration

Test settings and decoding: [configuration notes](effect-configuration.md#providers).

## Fake services

Read [services and layers notes](effect-services.md#test-layers) first. When a fake needs shared state, injected failures, or inspection, add a second tag for control and serve both tags from a single layer so they see the same state. Production code only ever asks for the real tag.

```ts
export class SmsControl extends Context.Tag("SmsControl")<
  SmsControl,
  {
    readonly outbox: Effect.Effect<ReadonlyArray<Sms>>;
    readonly breakNext: (e: SmsError) => Effect.Effect<void>;
  }
>() {}

export const SmsTest = Layer.unwrapEffect(
  Effect.gen(function* () {
    const outbox = yield* Ref.make<ReadonlyArray<Sms>>([]);
    const pending = yield* Ref.make<Option.Option<SmsError>>(Option.none());
    const send = (sms: Sms) =>
      Ref.getAndSet(pending, Option.none()).pipe(
        Effect.flatMap(
          Option.match({
            onSome: Effect.fail,
            onNone: () => Ref.update(outbox, (all) => [...all, sms]),
          }),
        ),
      );
    return Layer.merge(
      Layer.succeed(SmsSender, { send }),
      Layer.succeed(SmsControl, {
        outbox: Ref.get(outbox),
        breakNext: (e) => Ref.set(pending, Option.some(e)),
      }),
    );
  }),
);
```

For a small one-off, a partial mock whose unused members fail loudly is enough.

## Fiber coordination

Use explicit signals in place of sleeps.

- `Deferred`: something happens once.
- `Queue`: pass events or work across fibers.
- `Latch`: a gate that can reopen.
- `Ref`: collect observations.

Hook into the interfaces the code already exposes. Controls meant only for tests belong on a separate test-control service.

## Running effects

- `it.effect` from `@effect/vitest` provides controllable test services, including the clock. `it.live` uses real services and fits only when real time or live runtime behavior is the subject.
- Never wait for real time. Fork the sleeping effect, then advance with `TestClock.adjust`.
- If cancellation or cleanup is visible to callers, assert on it.
- Retry and schedule tests: also see [retry and scheduling notes](effect-scheduling-and-retry.md).

```ts
it.effect("gives up after the delay", () =>
  Effect.gen(function* () {
    const fiber = yield* Effect.fork(pollOnce);
    yield* TestClock.adjust("30 seconds");
    const outcome = yield* Fiber.join(fiber);
    expect(outcome).toEqual({ status: "timed-out" });
  }).pipe(Effect.provide(StubClient.layer)),
);
```
