---
name: go-coding-standards
description: "Use for Go code and design. Apply shared engineering rules with Go contracts, style, and tooling additions."
---

# Go coding standards

Apply the [shared workflow and reference chooser](../coding-standards/references/workflow.md) first, including every triggered shared reference. This plain reference does not enter the router, so standalone Go invocation loads shared rules without recursion.

Apply [Go contracts](GO_CONTRACTS.md) and [Go style](GO_STYLE.md) to every Go change. Read matching additions:

- Terms and package roles: [vocabulary](VOCABULARY.md).
- Named values and state: [domain modeling](DOMAIN_MODELING.md).
- Failure contracts: [errors](ERROR_HANDLING.md).
- Safe diagnostics: [observability](OBSERVABILITY.md).
- Packages and dependencies: [modules](DESIGNING_MODULES.md).
- External input: [boundaries](BOUNDARIES_AND_PARSING.md).
- Cancellation/concurrency/workflows: [async work](ASYNC_AND_WORKFLOWS.md).
- Tests and gates: [testing](TESTING_AND_VERIFICATION.md).

Use native Go error matching, context, package interfaces, and resource ownership. Do not import TypeScript, Effect, or Cloudflare prescriptions from examples. Keep unsafe escape hatches local and justified with `SAFETY:` behind precise interfaces. Tests use real seams, never module patches or method spies. Report constraints and verification under the shared workflow.
