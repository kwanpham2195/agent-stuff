# Improvement records

Add an Outcome section to the existing canonical work record only when there is something worth learning. Link detailed JSON receipts under its existing evidence directory. The work record retains status and authority; receipts add no backlog or Context Home schema.

Each candidate has a stable ID within the work item, original evidence IDs/ranges, failure class, observed acceptance and its authority, mechanism, owning source/check, permitted outcome/write scope/budget and regression gates. Preserve rejected and inconclusive candidates with reasons. Use states observed, proposed, authorized-for-trial, evaluated, deployed, followed-up, rejected or inconclusive. State transitions require evidence, not a renamed label.

Record source revision, actual loaded paths/digests, provider/model/options and available tools for each attempt. Link frozen fixture/rubric hashes, outputs and trial validity. Provider failures, incomplete outputs, changed scoring or invalid exposure invalidate a trial; they are not low reasoning scores. Acceptance needs criterion-level evidence, separately from human acceptance where required.

Use the companion [receipt validator](../scripts/improvement-evidence.py) to validate receipts and produce a read-only recurring-review delta. Pass a candidate receipt as the positional input; `--baseline <receipt>` checks matched model/options/tools, fixture/rubric hashes, exposure metadata and nonempty disjoint run IDs. Use `--prior <receipt> --as-of <UTC-time>` for recurring-review changes. It does not fetch evidence, infer truth, launch work or write state. Store its output only in the existing authorized evidence home. Structural validation cannot establish permission, semantic truth or experimental independence.

## Coverage

After each retro on a thread, add one coverage line to the Outcome section: thread ID, first and last item position, last run ID, retro date, and the retro skill revision used. Later retros read this to find their start, as [evidence sources](evidence-sources.md#repeated-retros-on-one-thread) describes.

## Measures

Count accepted task outcomes, not sessions or completed turns. Repeat mistake rate is confirmed affected tasks divided by applicable observed tasks; retain task IDs, denominator and unknown coverage. Recovery burden counts unplanned user interventions and repeated work caused by failures, excluding legitimate scope changes and required decisions. Record end-to-end timing with known queue, human wait and provider outage separately. Unknown components and token/cost usage are null, never zero. Sum usage only from verified non-overlapping records. Instruction words and tool reads are secondary diagnostics, not quality or billing measures.

## Promotion and follow-up

Promotion records the accepted source commit and last known good revision, reviewed exact target list, narrow apply receipt, byte/mode/symlink parity, and a fresh run's actual loaded path/digest plus observed behavior. Static, behavioral, deployed and observed-in-use status remain separate. Existing threads may retain earlier instructions; do not broadcast without authorization.

The deployed and followed-up states require nonempty `deployment.fresh_run_evidence` linking that fresh exposure. A source-only apply may be recorded in `deployment` under proposed, authorized-for-trial or evaluated, with fresh evidence null until observed. Human acceptance and valid passing trials remain promotion gates.

Rollback uses a reviewed reverse diff of only the candidate's owned source changes, preserves unrelated work, then applies only the same reviewed targets and checks parity. Record the rollback revision and evidence. Never broad-reset a checkout or treat an uncertain apply as failure without reconciling it.

Observe the next five applicable tasks within ten working days as a bounded pilot unless the owner records another approved window. Zero applicable tasks means incomplete follow-up. Preserve recurrence and regression evidence; reassess or roll back within the recorded authority. Future tasks remain unobserved until their actual evidence arrives.

Every `follow_up` includes `started_at` and `deadline_at`, each null or an explicit UTC timestamp in `YYYY-MM-DDTHH:MM:SSZ` form. Null preserves an unknown or not-started time; do not infer dates from a commit or source apply. A known deadline requires a known earlier start. The owner records the deadline using the approved working-day calendar; the validator does not infer holidays. A known start with an unknown deadline is valid but cannot produce an overdue alert. Existing receipts need these explicit fields, with null for unknowns.
