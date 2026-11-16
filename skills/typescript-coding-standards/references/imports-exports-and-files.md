# TypeScript imports, exports, and files

Apply [shared cohesion, helper ownership, and consumer audit](../../coding-standards/references/modules-and-dependencies.md#complexity-and-discoverability).

Import directly from the owning file; barrels/re-exports serve intentional package/public entrypoints. Use named imports for self-describing operations/classes/helpers. Namespace imports may preserve related domain ownership when the module has an established canonical API.

```ts
import { parseEmailAddress } from "./email-address";
import { PasswordReset } from "./password-reset";
```

Use `import type`/`export type` for type-only edges. Static imports are the ordinary default. Dynamic `import()` belongs to lazy/optional runtime/plugin/code-splitting boundaries, not ordinary dependency timing or cycle repair. Use ES modules for application grouping; TypeScript `namespace` requires interop.

Prefer searchable subjects such as `email-address.ts`, `billing-period.ts`, `string-case.ts`, and `array.ts`. Stable domain-independent helper families may have their own subject without waiting for a second consumer:

- exhaustive/defect helpers (`casesHandled`, `shouldNeverHappen`, `notYetImplemented`);
- `Redacted` wrappers;
- union operations (`Tags`, `ExtractTag`, `ExcludeTag`);
- Result operations when neither Effect nor better-result is used;
- genuinely broad type operations.

Keep policy with domain/service owners, not `prelude.ts` or miscellaneous utilities. Complete when shared ownership/consumer rules pass and imports, exports, module syntax, and helper families follow these TypeScript additions.
