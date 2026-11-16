# Workflows, transactions, and idempotency

## Cancellation and work ownership

Operations waiting on I/O, timers, retries, queues, subprocesses, workflows, resources, or long computation accept caller-owned cancellation when supported. Propagate it downstream. Dependency-specific timeouts compose with rather than replace that lifetime. If a dependency cannot cancel, check around its call and document the limitation. Classify cancellation before wrapping ordinary dependency failures.

Every async task is awaited, returned, collected, or handed to explicit detached-work machinery. Detached work identifies owner, lifetime, cancellation, failure handling, and observability.

Start independent work concurrently unless ordering, backpressure, rate limits, transactions, workflows, or an external contract require serialization. User/data/file/queue-sized work uses bounded concurrency, with limits justified by API rates, pools, CPU, memory, or runtime constraints rather than magic numbers. Prefer the project's shared primitive. Sequential execution alone does not solve overload. Choose aggregation semantics explicitly: stop-on-failure and useful partial results are different contracts, and aggregate failure does not necessarily cancel peers.

## Workflow selection

Use ordinary calls when no atomic state change is needed. Use a datastore transaction for changes that must commit/roll back together within one store. Close transactions before network calls or long-running work.

Use a saga/durable workflow or explicit orchestration record when progress must survive loss/redelivery, delays, compensation, resumability, timers, human approval, cross-service coordination, or multiple transaction boundaries. Externalize progress/retry/compensation state; do not rely on an in-memory call stack. Do not introduce workflows merely for layering when calls/transactions suffice.

Retry ownership and durability follow operation authority, side-effect safety, and required lifetime. Short technical retries may belong to adapters; business recovery policy belongs to its service/workflow.

## Idempotency

Require an explicit strategy for real duplicate paths: retries, redelivery, resumption, concurrent submission, or repeated external requests. Treat mutating request commands, especially creates, as retryable by default; clients, proxies, queues, and humans retry after lost responses.

Choose and record the strategy at the duplication owner:

- stable caller idempotency key;
- natural ID with unique constraint;
- persisted replay/deduplication record;
- state-machine transition guard;
- transactional outbox for state plus publication intent;
- transactional inbox for deduplication plus resulting state.

State the guarantee for every retried side effect. Creates retain logical identity on retry; transitions retain original completion metadata.

```text
Prefer: receive stable identity -> transaction saves/replays entity and outbox -> deliver after commit
Avoid:  save entity -> call provider, with no durable intent/recovery for a crash between steps
```

Atomic state guards follow [persistence](persistence.md).

Anything a run leaves behind, such as a lock, temp file, half-written record or claimed job, must be recognizable as stale by the next run. Judge staleness by evidence that holds wherever the previous run could have stopped, not only in the common case. For example, write to a temporary path and rename it into place, or compare artifacts by content rather than creation order.

## Uncertain outcomes and compensation

Timeout, interruption, or lost response does not prove a remote mutation failed. Model uncertainty when the provider cannot prove outcome. Select reconciliation, operator disposition, or safe retry from actual idempotency evidence.

Persist identity and recovery intent before external mutation when needed to undo a remote commit whose response can be lost. Preserve receipts, outboxes, leases, checkpoints, and compensation tombstones. Define delayed-write safety and the point of no return: required post-commit publication failure must not trigger invalid compensation. Fewer steps/writes alone do not justify removing a checkpoint.

## Completion

Cancellation and each task have owners; concurrency and aggregation match contracts; transactions close before remote/long work; every duplicate path and retry has a stated guarantee; durable work persists necessary authority; uncertainty and compensation preserve recovery evidence and point-of-no-return semantics.
