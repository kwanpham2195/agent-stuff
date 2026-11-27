# Calling HTTP APIs

Prefer Effect's `HttpClient` for outbound requests. Depending on the release it ships in a platform package or an unstable entrypoint, so find where the installed version exposes it. If a boundary cannot take the dependency, see the plain `fetch` section.

## Quick review

`HttpClient` used, or a recorded reason for `fetch`; status checked before decoding; typed failures; no transaction around a request; each retry has an owner and a safety argument.

## Plain `fetch`

Allowed at an edge that cannot use the Effect client. The duties stay the same: forward the abort signal, check the status before the body, decode with a schema, map every failure to a typed error.

```ts
const getQuote = (symbol: string) =>
  Effect.tryPromise({
    try: (signal) => fetch(`${baseUrl}/quotes/${symbol}`, { signal }),
    catch: (cause) => new QuoteUnreachable({ cause }),
  }).pipe(
    Effect.filterOrFail(
      (res) => res.ok,
      (res) => new QuoteRejected({ status: res.status }),
    ),
    Effect.flatMap((res) =>
      Effect.tryPromise({
        try: () => res.json(),
        catch: (cause) => new QuoteMalformed({ cause }),
      }),
    ),
    Effect.flatMap((json) =>
      Schema.decodeUnknown(Quote)(json).pipe(
        Effect.mapError((cause) => new QuoteMalformed({ cause })),
      ),
    ),
  );
```

How to decode: [parsing guide](parsing-and-schemas.md). Keep diagnostics free of secrets and personal data: [sensitive-data guide](sensitive-data-and-observability.md). Move to the Effect client once you need shared transforms, retries, or rate limits and can add it.

## Retrying and pacing

Only repeat what is safe to repeat.

- The client has a transient-retry helper for connection errors, timeouts, and standard retryable statuses.
- When the decision depends on a domain error or a provider-specific payload, retry the operation itself.
- A rate-limit wrapper can read limit headers and space calls apart. It requires a limiter service and may add an error type.

Custom schedules and server-provided waits: [retry and scheduling notes](effect-scheduling-and-retry.md).

## Requests and responses

- Configure base URL, default headers, and auth once by transforming the client.
- Use the JSON and accept-header helpers; the schema-aware body helper validates outgoing data.
- Filter on status first, then decode with the response helper that suits you (body only, or status and headers as well).

## One place for the protocol

Give each remote call a named effect that covers the whole exchange: address, headers, credentials, sending, status classification, decoding, error translation, and any retry or pacing. Put it in an adapter or private client. Code above it sees domain inputs, outputs, and typed errors only.

Do not hold a database transaction across a network wait. For the adapter-or-not question see [module and adapter guide](modules-services-and-adapters.md); for calls that may repeat, [workflow and idempotency guide](workflows-transactions-and-idempotency.md).
