# TypeScript imports, exports, and files

The [shared rules on cohesion, helper ownership, and consumer audits](../../coding-standards/references/modules-and-dependencies.md#complexity-and-discoverability) apply. These are the TypeScript specifics.

## Naming files and placing helpers

Call a file after a subject someone would search for: `phone-number.ts`, `billing-period.ts`, `string-case.ts`, `array.ts`. A few stable, domain-neutral families may have their own file without waiting for a second consumer:

- defect and exhaustiveness helpers (`casesHandled`, `shouldNeverHappen`, `notYetImplemented`)
- `Redacted` wrappers
- tagged-union utilities (`Tags`, `ExtractTag`, `ExcludeTag`)
- result helpers, when neither Effect nor better-result is available
- genuinely general type utilities

Business or application policy stays with the domain or service that owns it. It never goes into `prelude.ts` or a miscellaneous utilities file.

## Import and export style

- Import from the module that defines the symbol. Barrels and re-exports belong at entrypoints that are intentionally public.
- Prefer named imports when the name explains the operation. Namespace imports are acceptable for a module with an established canonical API that groups related domain ownership.
- Use `import type` and `export type` for edges that carry only types.
- Dynamic `import()` is for lazy, optional, plugin, or code-split boundaries. It is not a tool for ordering loads or breaking cycles.
- Group application code with ES modules; reserve TypeScript `namespace` for interop.

```ts
import { parsePhoneNumber } from "./phone-number";
import { AccountRecovery } from "./account-recovery";
```

Done when the shared ownership and consumer rules pass and the file names, helper families, and import and export forms follow the notes above.
