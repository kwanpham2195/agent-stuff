# Effect

Read this before touching Effect code, then open whichever of the files indexed at the end apply to your change.

## Defaults

1. Sequence work with `Effect.gen`, and label service operations with `Effect.fn`, matching the surrounding code.
2. Deal with expected failures from the typed error channel at the closest place that can respond meaningfully. Defects and interruption pass through untouched.
3. Wrap Promise-based and platform calls once, in the module that owns that dependency, so business logic stays in Effect.

If you depart from one of these, say why.

## Trust the installed version

Effect renames and relocates APIs between releases, and some modules are flagged unstable. Snippets in these notes illustrate a pattern, not guaranteed spellings. Before relying on any function, locate it in the project's installed `effect` package and check its signature there.

## Index

| File | Open it when you are... |
| --- | --- |
| [effect-schema-and-data.md](effect-schema-and-data.md) | defining models, brands, unions, or decoders |
| [effect-services.md](effect-services.md) | defining services or layers, or wiring an app |
| [effect-testing.md](effect-testing.md) | testing anything involving time, fibers, or fakes |
| [effect-streams.md](effect-streams.md) | handling event feeds, queues, or paginated data |
| [effect-http-clients.md](effect-http-clients.md) | calling a remote HTTP API |
| [effect-scheduling-and-retry.md](effect-scheduling-and-retry.md) | retrying, polling, backing off, or timing out |
| [effect-configuration.md](effect-configuration.md) | reading settings or secrets |
| [effect-caching.md](effect-caching.md) | memoizing, expiring, deduplicating, or batching lookups |
| [effect-alchemy.md](effect-alchemy.md) | composing Alchemy infrastructure with runtime code |
