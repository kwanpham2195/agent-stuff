# Reading configuration

How to declare settings with `Config`. Decisions about who may read the environment and how startup reacts to bad input are in the [configuration and resources guide](configuration-and-resources.md).

## Quick review

- Each setting is read through a `Config`.
- Secrets are redacted.
- No default can mask a malformed value.
- When two providers exist, it is stated which wins.

## Config-aware constructors

Beside a constructor that takes plain, decoded options you may offer one that takes a record of `Config` values (typed with `Config.Wrap`, resolved with `Config.unwrap`). Only add it for a real caller that composes configs like this.

## Providers

Values come from the process environment unless you swap the provider, and that swap belongs at the program's entry point.

- The provider layer substitutes the source for a whole app or test run.
- A second provider can be added as a fallback; document which takes priority.
- Translate key naming style with the provider's helpers rather than spelling each name twice.

Tests that supply settings: [Effect testing notes](effect-testing.md#configuration).

## Guidance

- Secrets go through `Config.redacted`, so they cannot be logged by accident.
- A default fills in a missing key only. A present but malformed value must still error.
- Mark a genuinely optional setting with `Config.option`.
- Do validation inside the config (schema-based or fallible mapping) instead of in the consumer.
- A fallback combinator swallows every parse error. Use it only if that is what you want.
- Use `Config.nested` to share a key prefix.

## Pattern

Describe the whole settings group as one `Config`, decode it when the service layer is built, and let a bad value stop startup with a typed error.

```ts
const settings = Config.all({
  apiKey: Config.redacted("PAYMENTS_KEY"),
  endpoint: Config.url("PAYMENTS_URL"),
  timeoutMs: Config.integer("PAYMENTS_TIMEOUT_MS").pipe(Config.withDefault(5000)),
});

export const PaymentsLive = Layer.effect(
  Payments,
  Effect.map(settings, makePayments),
);
```
