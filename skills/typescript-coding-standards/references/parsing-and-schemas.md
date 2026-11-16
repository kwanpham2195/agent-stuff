# TypeScript parsing and schemas

Apply [shared parsing and provenance](../../coding-standards/references/parsing-and-evidence.md). `unknown` and boundary DTO types remain honest representations until parsing. `satisfies` and field types establish compile-time evidence, not cross-field runtime proof.

## Provenance

Use a typed decoder only when input is assignable to its encoded type. Do not widen or cast to force that selection. For Effect decoder selection, read [decoder selection and public parsers](effect-schema-and-data.md#decoder-selection-and-public-parsers).

```ts
const raw: unknown = JSON.parse(text);
const input = CreateUserInput.parse(raw);
// Avoid: JSON.parse(text) as CreateUserInput
// Avoid: schema.parse(body); users.create(body); // discards refined output
```

Derive each schema-owned representation type from its schema. If Effect Schema directly produces the final branded domain type, derive that type without an intermediate representation.

## Parser APIs

Name parsers `parseX(input): Result<X, ParseXError>`, smart constructors `makeX`/`createX`, and true predicates `isX(value): value is X`. Reserve `assertX` for tests/framework boundaries requiring throws. Do not alias parsers as `validateX`/`normalizeX`.

Keep reusable codecs private beside their boundary/schema and export intentional, normally unary application wrappers. Library parse options stay private unless explicitly part of the low-level contract. See the Effect decoder reference for private-codec/unary-wrapper examples.

Choose, in order: established schema library; Effect Schema in Effect projects; Standard Schema compatibility for generic helpers; Zod 4 otherwise; a handwritten parser when clearer for a small domain type. Typed parse errors follow [errors](errors.md).

```ts
const CreateUserBody = z.strictObject({ email: EmailAddressSchema, role: RoleSchema });
```

Do not export generic `isRecord`, `isObject`, or `isArray` guards as a substitute for concrete parsers. Local `Array.isArray`/object checks inside parser implementations are appropriate. Branding assertions must satisfy [TypeScript safety](typescript-safety.md).
