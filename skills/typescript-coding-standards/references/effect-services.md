# Services and layers

In Effect a service is a capability that appears in the type of every program using it, with the implementation supplied when the app is assembled. Ownership and adapter placement are covered in [module and adapter guide](modules-services-and-adapters.md).

## Service or plain value?

It earns a service if it reaches outside the process, manages a resource or lifecycle, depends on time, randomness, or config, or genuinely has different production and test implementations. First check whether Effect already supplies it (`Clock`, `Random`, `FileSystem`, `HttpClient`).

Plain functions or values are better for request data, calculations, parsers, per-call options, framework objects confined to an adapter, and thin forwarding wrappers. "I want to substitute it in a test" alone does not justify a service. Record which you chose and why.

## Test layers

Tests should use the production interface. Provide an in-memory implementation that honors the observable contract, or a real local substitute when persistence, transactions, serialization, or protocols matter. A narrow fake used by one test can stay in that test. Name reusable fakes by behavior (`InMemoryStore`, `RecordingNotifier`). More in [Effect testing notes](effect-testing.md).

## Module surface

Expose one namespace per module and keep schemas, codecs, and internals private. If the toolchain permits it, `export * as Notifier from "./notifier.js"` gives uniform access; otherwise use plain named exports.

## Naming operations

Wrap public and significant methods in `Effect.fn("Module.operation")` for spans and clean stack traces; use `Effect.fnUntraced` for small internal helpers. Concerns that need both the arguments and the finished effect (error mapping, annotations, timeouts) can be passed as trailing functions:

```ts
const read = Effect.fn("Docs.read")(
  function* (id: DocId) {
    return yield* store.get(id);
  },
  (effect, id) => effect.pipe(Effect.mapError(toDocsError("read", id))),
);
```

Share an error-mapping helper only when many operations mean the same thing by it; otherwise map errors explicitly ([error guide](errors.md#boundary-translation)).

## Choosing layer constructors

| Acquisition | Constructor |
| --- | --- |
| Value already in hand | `Layer.succeed` |
| Cheap synchronous build | `Layer.sync` |
| Effectful build | `Layer.effect` |
| Needs cleanup | `Layer.scoped` |
| Config picks the layer | `Layer.unwrapEffect` |

`Layer.provide` hides a dependency your module owns; `Layer.provideMerge` also forwards it; `Layer.mergeAll` joins independent layers. Layers are shared by identity, so name them as constants and compose them flat at the entrypoint. `Layer.fresh` forces separate instances and should be rare. Anything that starts a listener, stream, or worker should fork it into the layer's scope ([stream notes](effect-streams.md)).

## A typical module

```ts
export class Notifier extends Context.Tag("app/Notifier")<
  Notifier,
  {
    readonly notify: (
      user: UserId,
      text: string,
    ) => Effect.Effect<void, DeliveryFailed>;
  }
>() {}

export const NotifierLive = Layer.effect(
  Notifier,
  Effect.gen(function* () {
    const transport = yield* Transport;
    const notify = Effect.fn("Notifier.notify")(function* (user: UserId, text: string) {
      yield* transport.deliver({ user, body: text });
    });
    return Notifier.of({ notify });
  }),
);
```

Some projects use `Effect.Service` to bundle tag and default layer. Follow what exists.

- Interface, tag, and expected errors live in the module that owns the capability.
- Yield dependencies once, while building the layer; yield per-request context in the method that needs it.
- Leave unmet requirements in the type until the module that actually decides the implementation supplies them.
- Operation-specific values (credentials, scoped handles) stay as parameters.
- Inject service objects, not individual callbacks; keep interfaces cohesive and domain-shaped.

## Quick review

Is the service-or-value decision justified? Does every piece have a single owner? Are dependencies acquired at build time and request context where it is used? Do constructors fit the acquisition? Is background work scoped? Are helpers keeping full error and requirement types? Do tests hit the production interface?
