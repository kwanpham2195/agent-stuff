# TypeScript configuration and resources

Apply [shared configuration and resources](../../coding-standards/references/configuration-and-resources.md). Keep `process.env` and platform bindings at startup/composition, not scattered through services. Use typed configuration with [redacted secrets](sensitive-data-and-observability.md).

```ts
type AppConfig = { readonly databaseUrl: Url; readonly apiToken: Redacted<string> };
```

For Effect configuration, resources, time, or randomness, load [Effect](effect.md) and every matching branch. Managed Layers/scopes own acquisition and release. Plain TypeScript uses explicit constructor capabilities and resource owners; security/consequential randomness uses Web Crypto or runtime-equivalent crypto, not `Math.random()`.
