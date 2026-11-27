# TypeScript parsing and schemas

Follow the [shared guidance on parsing and provenance](../../coding-standards/references/parsing-and-evidence.md). Until it is parsed, treat data as `unknown` or as the boundary's DTO type. `satisfies` and field types give compile-time evidence only; they do not prove rules spanning fields.

## Picking a library

In order of preference: the schema library the project already uses; Effect Schema in Effect projects; Standard Schema compatibility for generic helpers; Zod 4 otherwise; a handwritten parser when it is clearer for a small domain type. Typed parse failures follow the [error guide](errors.md).

```ts
const SignupBody = z.strictObject({ email: EmailSchema, plan: PlanSchema });
```

Do not export generic `isRecord`, `isObject`, or `isArray` guards in place of concrete parsers. Local `Array.isArray` or object checks inside a parser are fine. A cast that applies a brand must meet the [safety guide](typescript-safety.md).

## Provenance

Use a typed decoder only for input that is already assignable to its encoded type. Do not widen or cast just to qualify. For decoder selection in Effect, see [decoder selection and public parsers](effect-schema-and-data.md#pick-the-decoder-by-the-input-you-hold).

```ts
const raw: unknown = JSON.parse(text);
const input = SignupBody.parse(raw);
// Never: JSON.parse(text) as SignupBody
// Never: schema.parse(body); service.create(body); // throws away refined output
```

Derive every schema-owned representation type from its schema. If Effect Schema already produces the final branded domain type, derive from that directly, with no intermediate representation.

## Parsers and names

- Parsers are `parseX(input): Result<X, ParseXError>`.
- Smart constructors are `makeX` or `createX`.
- Real type predicates are `isX(value): value is X`.
- `assertX` is for tests or frameworks that need a throw.
- Do not rename parsers to `validateX` or `normalizeX`.

Keep reusable codecs private next to the boundary or schema, and export deliberate wrappers, usually taking one argument. Library parse options stay private unless the low-level contract includes them. The Effect schema notes show the private-codec-plus-wrapper pattern.
