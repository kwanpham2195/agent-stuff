# Retry, polling, and timing

`Schedule` values say when to go again. Use them for retries, polling, and recurring jobs rather than loops with manual sleeps.

## Quick review

Who owns each retry or loop, and what stops it? Is every retried effect safe to repeat? What happens to a failed pass or item? Do tests avoid real time?

## Related timing tools

`Effect.timeout` bounds how long something may take, `Effect.delay` postpones the start, `Effect.sleep` is for when waiting is the point. For tests, advance a test clock ([Effect testing notes](effect-testing.md)).

## Background loops

For a worker that does a pass over and over:

- Log expected failures of a pass and keep going.
- Do not swallow defects; supervision should see them.
- Cause-level recovery belongs only in a top-level supervisor that is meant to log and carry on.

```ts
const worker = pass.pipe(
  Effect.tapError((e) => Effect.logError("pass failed", e)),
  Effect.ignore,
  Effect.repeat(Schedule.spaced("5 seconds")),
);
```

Within a pass over many items, isolate failures item by item, with limited concurrency, but only if skipping the item or retrying it next pass is the intended outcome.

## Server-suggested delays

When a typed error holds a requested wait, compute the delay from the error as the larger of your backoff and that value, in the schedule rather than inside the retried effect. HTTP-specific handling lives in [effect-http-clients.md](effect-http-clients.md).

## Semantics worth remembering

- `Effect.retry` reacts to typed failure only; a defect or interruption is never retried.
- `Effect.repeat` reacts to success; a failure stops it.
- The first attempt happens before the schedule is asked anything. "Recurs 3 times" therefore gives four runs at most.
- `spaced` measures from the end of one run; `fixed` holds a steady rhythm.
- Backoff is `exponential` or `fibonacci`, nearly always with `jittered` added.
- Every retry needs a ceiling: attempts, elapsed time, or both.
- Use `Effect.retryOrElse` if running out of attempts should trigger a fallback.
- Retry the narrowest step that is safe to repeat and let the last failure surface unless there is a genuine fallback. For side-effect duplication risks, see [workflow and idempotency guide](workflows-transactions-and-idempotency.md).

```ts
const backoff = Schedule.exponential("200 millis").pipe(
  Schedule.jittered,
  Schedule.intersect(Schedule.recurs(5)),
);

const sync = (id: string) =>
  pushRecord(id).pipe(
    Effect.retry(backoff),
    Effect.tapError((e) => Effect.logError("sync gave up", e)),
  );
```

Exact combinator names differ by release; check the installed version.
