# Go vocabulary

Shared responsibility/interface/seam terminology is defined in [modules and dependencies](../coding-standards/references/modules-and-dependencies.md); shared failure meaning is defined in [errors](../coding-standards/references/errors.md).

Go-specific terms:

- Domain package: a pure package centered on a domain concept/type family, exposing named values, constructors/parsers, predicates, transitions, formatting, and neutral projections.
- Service package: a dependency-bearing cohesive use-case package accepting parsed values, coordinating policy/effects, and returning values plus native `error`.
- Adapter package: an HTTP/RPC, queue, persistence, platform, or SDK boundary that parses/projects and implements consumer-facing interfaces.
- Named domain type: a Go defined type distinguishing semantic values from primitive representation, such as `type MerchantID string`.
- Typed error match: a category callers handle through `errors.Is`/`errors.As`, using sentinel categories, structured error types, and deliberate cause wrapping.

These terms do not require corresponding package suffixes or folders. Do not interpret shared precise failures as a requirement to introduce a TypeScript-style Result/union in Go.
