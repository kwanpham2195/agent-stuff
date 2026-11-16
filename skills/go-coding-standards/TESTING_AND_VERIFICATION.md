# Go testing and verification

Apply [shared tests and evidence](../coding-standards/references/testing.md). Go retains its stricter prohibition: no module/global monkey-patching or method spies. Observable interactions use injected recording/fake adapters with public records. Avoid sleep-based timing.

Prefer table tests for pure domain behavior, `httptest` for HTTP adapters, temporary directories/files for filesystem boundaries, real parser/codec tests for DTOs/rows, and representative local databases for SQL/driver semantics. Integration tests prefer real HTTP/RPC transports over mocked transports.

## Native test conventions

- Prefer `t.Error` for checks that may continue; use `t.Fatal` for failed setup or when remaining checks are meaningless.
- Never call `t.Fatal`/`t.FailNow` from spawned goroutines. Return failures through a channel or errgroup to the test goroutine.
- Use field names in table-case struct literals.
- Scope setup to individual tests; avoid global `TestMain` when per-test setup suffices.
- Use `t.Errorf("Func(%v) = %v, want %v", input, got, want)` with function/input and got-before-want.
- Avoid third-party assertion libraries. Use `go-cmp/cmp` for struct comparisons rather than manual field lists, subject to task dependency permission.

```go
tests := []struct { input string; want []string }{
    {input: "x", want: []string{"x"}},
}
```

## Gates

Use established repository gates first. If absent, default to `gofmt`, `go test ./...`, and `go vet ./...`. Run `golangci-lint` when already used; do not add a new lint stack merely for these standards. Report exact commands and concrete blockers; matching shared policy does not claim behavioral efficacy of these instructions.
