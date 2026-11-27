# Go boundaries and parsing

Apply [shared parsing and evidence](../coding-standards/references/parsing-and-evidence.md). Go decoding into a struct establishes field representation, not domain/cross-field integrity.

```go
type createCustomerRequest struct {
    CustomerID string `json:"customer_id"`
}

func (h *Handler) CreateCustomer(w http.ResponseWriter, r *http.Request) {
    var req createCustomerRequest
    // Decode, reject unknown command fields, parse CustomerID, then call service.
}
// Avoid passing http.Request or a raw decoded request to domain/service packages.
```

Keep HTTP/RPC/framework contexts, env maps, unparsed JSON, SDK models, and ORM rows inside adapters. Repository adapters return reconstructed domain/service values, not generated rows, unless the repository package is itself the declared service boundary.

Use concrete `ParseX` functions and native `(value, error)` contracts; choose the established Go parser/schema/codec convention. For JSON commands, use strict unknown-field handling such as `json.Decoder.DisallowUnknownFields` where applicable; deliberately extensible metadata remains explicit.

Define transport structs/codecs for process/RPC/queue hops and parse on receipt; do not assume arbitrary local interfaces, error types, or handles survive serialization. Separate protocol and persistence projection structs even when both encode JSON. Read [Go contracts](GO_CONTRACTS.md) for public error matching and [observability](OBSERVABILITY.md) for safe startup/config diagnostics.
