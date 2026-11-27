# TypeScript testing

The [shared testing and verification rules](../../coding-standards/references/testing.md) apply. Size the checks to what changed and lean on existing coverage that is already enough. If several components must work together for the change to matter, add one happy-path test that enters through the real public interface. Cover the errors that matter at the nearest realistic boundary. Skip tests that merely restate a low-stakes, easily reversed change. If a flaky third party or an impractical setup, runtime, or cost prevents a check, say exactly what blocked it.

Module patching with `vi.mock` or `jest.mock` is not allowed. Substitute dependencies through constructors, faithful adapters, Effect services and layers, or local infrastructure that behaves like the real thing.

Assert on a spy only when the call itself is the behavior users or neighbors can observe. Otherwise read the public record of a recording implementation instead of spying on a method with `vi.spyOn` or `jest.spyOn`. This small allowance is specific to TypeScript; the Go rules are stricter.

```ts
expect(await passwordReset.requestReset(email)).toEqual(ok({ delivery: "queued" }));
expect(emailAdapter.sentEmails).toContainEqual({ to: email, template: "reset" });
// Reading the recorded output beats spying on the provider's send method.
```

Write property tests with `fast-check`; in Effect code, prefer Effect's FastCheck support and arbitraries derived from schemas. Keep `.test.ts` and `.test.tsx` files, and domain `.arbitrary.ts` files, beside the code unless the repository lays things out differently. Arbitraries for valid data should build values with the production parsers. Corrupt boundary fixtures are written separately, as the shared rules describe.

In Vite+ projects use `vp test` and ordinary APIs from `vite-plus/test` unless Effect-specific testing applies. In non-Effect Vitest property tests use established Fast-Check integration such as `@fast-check/vitest`. Effect tests follow [Effect testing](effect-testing.md).

For Drizzle persistence not depending on Cloudflare semantics, use in-memory `better-sqlite3`, real migrations, and the production service-facing adapter. Cloudflare D1, Durable Objects, Agents, bindings, workerd serialization, Workers APIs, alarms, WebSockets, or runtime-specific behavior require `@cloudflare/vitest-pool-workers` and relevant local bindings/runtime. Node-only evidence does not prove workerd behavior. These are scoped implementation choices, not permission to add dependencies outside the task.

## Regression evidence for parsing and recovery

The [shared evidence rules for parsing and recovery](../../coding-standards/references/testing.md#persistence-parsing-and-recovery) apply. In TypeScript, such a regression test should also pin the exact public parser, error, and Effect requirement types, using the compile-time section below.

## Completion check

Complete when [shared testing completion](../../coding-standards/references/testing.md#completion) passes, changed behavior and important expected errors have proportionate evidence or a concrete blocker, and each applicable TypeScript tool/runtime and public inference rule below is checked. Broaden or repeat passing checks only for new changes, failures, or unresolved concerns.

## Compile-time behavior

Check that normal call sites compile when they should and fail when they should, and check the function's full contract without helper annotations or casts: arguments and options, result, expected errors, and Effect requirements. Asserting only on parameters lets a widened error or requirement channel slip by. Parsing/recovery regressions and runtime claim limits follow [shared testing](../../coding-standards/references/testing.md#persistence-parsing-and-recovery).
