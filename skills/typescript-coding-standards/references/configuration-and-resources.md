# TypeScript configuration and resources

The [shared configuration and resources guidance](../../coding-standards/references/configuration-and-resources.md) applies. Confine `process.env` and platform bindings to startup or the composition root; services should receive typed settings. Secrets use [redacted wrappers](sensitive-data-and-observability.md).

```ts
type Settings = { readonly dbUrl: Url; readonly signingKey: Redacted<string> };
```

In Effect code, load the [Effect entry point](effect.md) and every branch that matches the work; managed layers and scopes handle acquiring and releasing resources. In plain TypeScript, pass capabilities through constructors and give each resource an explicit owner. For anything security-related or consequential, draw randomness from Web Crypto or the runtime's crypto equivalent, never `Math.random()`.
