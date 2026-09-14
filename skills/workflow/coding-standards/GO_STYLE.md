# Go Style

Go style favors clarity, simplicity, and concision over cleverness. Names, comments, and structure should make the code's purpose and rationale obvious to the next reader.

## Style principles

In priority order:

- **Clarity** — purpose and rationale clear to the reader (not the author). Comments explain why, not what; names are self-describing.
- **Simplicity** — simplest way that accomplishes the goal. No unnecessary abstraction. Complexity is added deliberately, with documentation, typically for performance.
- **Concision** — high signal-to-noise ratio. Repetitive code obscures differences; factor it out (e.g. table-driven tests).
- **Maintainability** — easy to modify correctly. APIs grow gracefully. Avoid unnecessary coupling and unused features.
- **Consistency** — consistent with the broader codebase. Local consistency matters most within a package; it does not override the principles above.
- **Least mechanism** — prefer core language constructs (channel, slice, map, loop, struct) → stdlib → external libraries, in that order. Don't employ sophisticated machinery without reason.

## Naming

### Package names

Lowercase, no underscores, concise. Avoid `util`, `helper`, `common`, `model` — name by what the package provides. Avoid names likely to be shadowed by common local variables (e.g. `usercount` over `count`). Multi-word: unbroken lowercase (`tabwriter`, not `tabWriter` or `tab_writer`).

Exception: `_test` suffix for black-box tests (`linkedlist_test`).

Good:
```go
package creditcard
package tabwriter
package usercount
```

Bad:
```go
package credit_card   // underscores
package util          // meaningless
package tabWriter     // mixed case
```

### Receiver names

Short (1-2 letters), abbreviation of the type, consistent across all methods of the type. Not `this` or `self`. Omit if unused.

| Bad | Good | Type |
|-----|------|------|
| `func (tray Tray)` | `func (t Tray)` | `Tray` |
| `func (self *Scanner)` | `func (s *Scanner)` | `*Scanner` |
| `func (this *Service)` | `func (svc *Service)` | `*Service` |

### Constant names

MixedCaps, no `K` prefix, no `MAX_SNAKE_CASE`. Name by role, not value.

```go
// Good
const MaxPacketSize = 512
const DefaultTimeout = 30 * time.Second

// Bad
const TWELVE = 12           // name by value
const KMaxRetries = 3       // K prefix
const MAX_SNAKE_CASE = 100  // snake case
```

### Initialisms

Same case within the initialism: `URL`/`url`, not `Url`. `ID`/`id`, not `Id`. `DB`/`db`, not `Db`.

Multi-initialism: each initialism same case internally but not necessarily matching each other (`XMLAPI` exported, `xmlAPI` unexported).

Initialisms with lowercase letters in prose (`gRPC`, `iOS`, `DDoS`): appear as in prose when unexported (`gRPC`), all-same-case when exported (`GRPC`, `IOS`, `DDoS`).

| Unexported | Exported |
|------------|----------|
| `url` | `URL` |
| `id` | `ID` |
| `db` | `DB` |
| `xmlAPI` | `XMLAPI` |
| `gRPC` | `GRPC` |
| `iOS` | `IOS` |
| `dDoS` | `DDoS` |

### Function and method names

Avoid repetition — don't repeat:

- Package name: `yamlconfig.Parse`, not `ParseYAMLConfig`
- Receiver type: `WriteTo`, not `WriteConfigTo`
- Parameter names: `Override`, not `OverrideFirstWithSecond`
- Return types: `Transform`, not `TransformToJSON`

Noun names for functions that return a value; verb names for functions that do something. No `Get` prefix (`Counts`, not `GetCounts`); use `Compute`/`Fetch` for expensive operations.

Type suffix for type-variant functions (`ParseInt`/`ParseInt64`); omit for the primary version (`Marshal`/`MarshalText`).

### Variable names

Length proportional to scope, inversely proportional to usage count:

- Small scope (1-7 lines): single letter or short word ok.
- Large scope (25+ lines): multiple words.

Omit type words (`users`, not `userSlice`; `count`, not `numUsers`). Omit context words (in `UserCount` method, `count` not `userCount`). Use `raw`/`parsed` or `Str` suffix when same value appears in multiple forms.

Single-letter conventions:
- `r` for `io.Reader` / `*http.Request`
- `w` for `io.Writer` / `http.ResponseWriter`
- `i` for loop index

Don't drop letters to save typing (`Sandbox`, not `Sbx`).

### Test double naming

Test double package: append `test` to production package name (`creditcardtest`).

Single double for one type: `Stub` (not `StubService`). Multiple behaviors: name by behavior (`AlwaysCharges`, `AlwaysDeclines`). Multiple types: `StubService`, `StubStoredValue`.

Local variables in tests: prefix when double is juxtaposed with production types (`spyCC`, not `cc`).

## Commentary

### Doc comments

All top-level exported names must have doc comments; unexported types/functions with unobvious behavior should too. Full sentences starting with the symbol name. An article ("a", "an", "the") may precede.

```go
// A Request represents a request to run a command.
type Request struct { ... }
```

### Comment sentences

Complete sentences: capitalized and punctuated. Sentence fragments: no requirements. Doc comments are always complete sentences. End-of-line struct field comments can be phrases.

### Package comments

One per package, immediately above the package clause, no blank line. If multiple files, exactly one file has it. Long package docs: use `doc.go`. `main` packages: use the binary name, not `package main`.

### What not to comment

- Don't restate what the code does; explain why.
- Don't restate implied behavior (e.g. "context cancellation returns `ctx.Err()`" is implied — don't document it unless behavior differs).
- Don't document every parameter; document the error-prone or non-obvious ones.

### Signal boosting

When code looks common but is subtly different, add a comment to call attention:

```go
if err := doSomething(); err == nil { // if NO error
```

Also use for single-character-critical lines (`=` vs `:=`, hidden `!`).

### Examples

Runnable examples in test files (`example_test.go`), not production source. Show up in godoc. If not runnable, example code in comments is acceptable.

### Named result parameters

Add names when caller must take action:

```go
func NewContext(parent Context) (ctx Context, cancel func())  // caller must call cancel
```

Not `(Context, func())`.

Name when two+ results have the same type: `(left, right *Node)`.

Don't name for naked returns in medium functions. Don't name when it creates repetition (`(node *Node)` is redundant). Types can be clearer than names (`context.CancelFunc` vs `func()`).

## Imports

### Import grouping

Four groups, separated by blank lines, in order:

1. stdlib
2. project/vendored
3. protobuf (if used)
4. blank imports (`import _`)

```go
import (
    "context"
    "fmt"

    "github.com/org/project/internal/domain"
    "github.com/org/project/internal/store"

    _ "github.com/lib/pq"
)
```

### Import renaming

Don't rename unless:

- Collision (rename the more local/project-specific one).
- Uninformative name (`util` → something better).
- Removing underscores from generated packages.

Same local name across files for consistency.

### No dot imports

`import .` is prohibited; it hides where symbols come from.

### Blank imports

`import _` only in `main` packages or tests that require them. Not in library packages. Exception: `embed` for `//go:embed` directives.

## Variable declarations

### Initialization

Prefer `:=` over `var` when initializing with a non-zero value. Use `var` for zero-value declarations.

```go
x := 42        // good: non-zero
var x int      // good: zero value
var x int = 42 // bad: use := instead
```

### Nil slices

Prefer `var s []T` over `s := []T{}` for empty slice declarations. `nil` slices are functionally equivalent to empty slices (`len`, `cap`, `range` all work). Don't design APIs that distinguish `nil` from empty — use `len(s) == 0`, not `s == nil`.

### Composite literals

Field names required for types from other packages:

```go
r := csv.Reader{Comma: ','}        // good
r := csv.Reader{',', '#'}           // bad: positional
```

Field names optional for package-local types but recommended for clarity. Omit zero-value fields when clarity is not lost.

Repeated type names may be omitted in slice/map literals:

```go
s := []*Type{{A: 42}, {A: 43}}     // good
s := []*Type{&Type{A: 42}, &Type{A: 43}} // bad: redundant
```

Closing brace on its own line at the same indentation as the opening brace.

### Size hints

Preallocate capacity when the size is known:

```go
s := make([]T, 0, n)
m := make(map[K]V, n)
```

### Channel direction

Specify `<-chan T` or `chan<- T` when the channel is unidirectional.

## Function arguments

### Long signatures

Don't let signatures get too long. If parameters exceed ~5, consider:

- **Option struct** — collect some/all args into a struct passed as the last parameter.
- **Variadic options** — `func New(opts ...Option) *T` with `WithX(x)` closures. Use when callers set few options and most use defaults.

## String concatenation

- `+` for few strings (simplest, no import).
- `fmt.Sprintf` for formatted strings (when format verbs are needed).
- `strings.Builder` for piecemeal construction (amortized linear time).
- Backticks for constant multi-line string literals.

## Global state

Libraries should not force clients to use global-state APIs. Avoid package-level mutable state for time, randomness, loggers, clients, and configuration. If a default instance is needed for convenience, document it and keep it as an opt-in, not the primary API.

(See also [GO_CONTRACTS.md](GO_CONTRACTS.md) "Interfaces and dependencies" for dependency injection patterns.)

## Panics

- Don't panic for expected failures — return `error`.
- Don't recover panics to avoid crashes — propagating corrupted state is worse.
- `log.Fatal` (or `os.Exit` with a diagnostic) for invariant violations where internal state is unrecoverable; `panic` is not reliable for this because deferred functions can deadlock.
- Exception: internal panic/recover within a package where panics never escape the package boundary (e.g. deeply nested parsers). The public API must `recover` and translate to `error`.
- `panic("unreachable")` after non-returning functions like `log.Fatal` is acceptable.

## Rejected framings

- **"The existing code uses `Get` prefix, so I will too."** New code follows naming conventions; don't copy violations.
- **"Comments should restate the code."** Comments explain why, not what.
- **"`nil` and `[]T{}` are different."** Don't design APIs that distinguish them.
- **"An interface before a need exists."** Create interfaces when behavior varies or tests substitute, not preemptively. (See also [GO_CONTRACTS.md](GO_CONTRACTS.md).)
- **"Dot imports save typing."** They hide symbol origins.
