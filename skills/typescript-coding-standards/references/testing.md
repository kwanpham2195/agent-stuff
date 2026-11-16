# TypeScript testing

Apply [shared tests and verification](../../coding-standards/references/testing.md). Match checks to the changed behavior and reuse sufficient existing coverage. Use an end-to-end happy-path test through the real public entrypoint when integration across components is material to the change. Exercise important expected errors at the closest reliable real interface. Do not add tests that mirror reversible, low-impact changes. Report concrete blockers from unreliable third parties or unreasonable setup/runtime/cost.

`vi.mock`/`jest.mock` module patching is forbidden. Replace via constructors, faithful adapters, Effect services/Layers, or representative local infrastructure.

A spy assertion is allowed only when the interaction itself is observable behavior. Prefer public records from a recording implementation over `vi.spyOn`/`jest.spyOn` on implementation methods. This narrow TypeScript allowance does not apply to Go's stricter addition.

```ts
expect(await passwordReset.requestReset(email)).toEqual(ok({ delivery: "queued" }));
expect(emailAdapter.sentEmails).toContainEqual({ to: email, template: "reset" });
// Prefer this production seam over spying on the provider's send method.
```

Use `fast-check` for ordinary TypeScript properties; in Effect prefer its FastCheck integration and Schema-derived arbitraries. Colocate `.test.ts`/`.test.tsx` and domain `.arbitrary.ts` files unless repository layout differs. Valid arbitraries construct through owning production parsers; independent corrupt boundary fixtures follow shared rules.

In Vite+ projects use `vp test` and ordinary APIs from `vite-plus/test` unless Effect-specific testing applies. In non-Effect Vitest property tests use established Fast-Check integration such as `@fast-check/vitest`. Effect tests follow [Effect testing](effect-testing.md).

For Drizzle persistence not depending on Cloudflare semantics, use in-memory `better-sqlite3`, real migrations, and the production service-facing adapter. Cloudflare D1, Durable Objects, Agents, bindings, workerd serialization, Workers APIs, alarms, WebSockets, or runtime-specific behavior require `@cloudflare/vitest-pool-workers` and relevant local bindings/runtime. Node-only evidence does not prove workerd behavior. These are scoped implementation choices, not permission to add dependencies outside the task.

## Parsing and recovery regressions

Follow [shared parsing/recovery evidence](../../coding-standards/references/testing.md#persistence-parsing-and-recovery). TypeScript regression checks additionally retain exact public parser/error/Effect requirement contracts under the compile-time guidance below.

## Completion check

Complete when [shared testing completion](../../coding-standards/references/testing.md#completion) passes, changed behavior and important expected errors have proportionate evidence or a concrete blocker, and each applicable TypeScript tool/runtime and public inference rule below is checked. Broaden or repeat passing checks only for new changes, failures, or unresolved concerns.

## Compile-time behavior

Test accepted/rejected ordinary call sites and the whole function contract without rescue annotations/casts: input, arity/options, success, expected errors, and Effect requirements. Parameter-only assertions miss widened channels. Parsing/recovery regressions and runtime claim limits follow [shared testing](../../coding-standards/references/testing.md#persistence-parsing-and-recovery).
