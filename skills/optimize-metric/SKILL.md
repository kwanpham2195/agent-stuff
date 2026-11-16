---
name: optimize-metric
description: "Iteratively improve a user-selected measurable outcome with a frozen workload, noise-aware measurements, bounded hypotheses, and parent-reviewed reversible edits. Use for repeated optimization experiments; do not use for comparative skill evaluation or one-off bug diagnosis."
metadata:
  short-description: Optimize one measured outcome safely
---

# Optimize a metric

Use this skill when the user wants repeated, evidence-based improvement of one measurable outcome. The supervising parent owns the experiment contract, reviews actual diffs and results, and accepts or rejects each change.

## Agree before attempting

Agree the following with the user and record it in the existing authorized work record before the first attempt:

- the outcome, metric name, unit, direction of improvement, realistic workload, and relevant workload dimensions;
- the measurement command or API, repeat count, noise estimate or threshold, and the frozen scoring method;
- the regression gates that must remain green;
- the target, finite maximum attempts and elapsed time, and any cost limit. Disclose unknown costs and obtain approval to proceed under the known bounds;
- write scope, rollback authority, and who may approve a kept change.

If the metric, direction, workload, target, authority, or measurement is ambiguous, ask a focused question. Do not choose a proxy or silently grant permission.

## Establish the baseline

Ground the workload and architecture before choosing a change. The workload must represent the reported case and expose the dimensions that can move the result, such as input size, history, state, or concurrency. If no realistic case reproduces the concern, stop and report the missing evidence. Repairing the reproduction needs separate authorization.

Validate the measurement's sensitivity with contrasting realistic workloads. Freeze one repeatable measurement procedure only after it separates the relevant cases. Run enough repeats to estimate noise, record the baseline with units and uncertainty, and retain the original baseline artifact. Run every regression gate and require a green baseline before changing the target.

Explain the number before trusting it. Name the resource or code path that limits the baseline, using a profile or system counters taken during a run, not a guess from reading code. Ask why the number is not twice as good. Bound each possible gain: a part that takes 10% of the run time can cut the run time by at most 10%, so a larger gain means the measurement is wrong. Have the measurement report completed work, such as requests served or rows written, and the error count beside the metric, so a gain from doing less work or from failing shows. Measure the user-facing path as well as any microbenchmark. Alternate the compared sides between repeats and report the median and range.

Hold the workload, scoring, measurement procedure, and gates constant for the rest of the run. Compare every result with the current accepted state and the original baseline.

## Run bounded attempts

Read the existing attempt log before each attempt. Record one row or entry per attempt, including failures and blocked attempts:

`id | hypothesis | isolated change | before | after | delta | uncertainty/noise | gates | verdict | artifacts | note`

For each attempt:

1. State one mechanism-specific hypothesis and its predicted metric change.
2. Make one isolated change within the approved write scope. Delegation is optional and follows the active harness's [delegated execution owner](../delegated-execution/SKILL.md). The parent owns launches and reconciles terminal results. Do not duplicate model APIs, use a nested agent, or bypass the selected harness owner.
3. Inspect the actual diff and run the frozen measurement with the approved repeats.
4. Run all regression gates, even when the measurement improves.
5. Keep the change only when the gates pass, the measurement shows no less completed work and no more errors, and the gain exceeds the stated noise threshold. Otherwise reject it.
6. For a rejected change, use the approved rollback method to reverse only edits owned by this attempt. If reversal lacks permission or cannot preserve unrelated work, stop before another attempt and report the retained change. Never use `git reset`, `git restore`, or broad cleanup that could discard unrelated work.
7. Record the verdict, measurements, gate evidence, failure reason when relevant, and artifact paths before starting another attempt.

A parent review of the diff and results is required for each kept or rejected change. A result that merely might help, a code inspection, or a passing command that ran no meaningful tests does not establish a gain.

## Stop safely

Stop and report when any of these occurs:

- the target is reached and the agreed stop predicate is satisfied;
- the attempt, time, or cost budget is exhausted;
- the user or parent withdraws permission;
- measurements cannot be collected, the harness is invalid or insensitive, or a required native tool blocks progress;
- repeated rejects or a plateau leave no cheap, evidence-based hypothesis.

Do not add a minimum-effort quota, run an unbounded wake or retry loop, relax the target or noise threshold, or stack unmeasured changes. Preserve partial work and blocked evidence. Commit kept changes under the global local-commit policy only after the agreed acceptance and regression gates pass and the parent accepts the change. Preserve rejected or incomplete attempts in the authorized work record. Opening a pull request, pushing, publishing, and changing unrelated files require separate authorization.

## Report the result

Return the baseline and final values with units, direction, delta, repeats, and uncertainty. List attempts, kept changes, rejected or blocked changes, regression-gate evidence, artifacts, elapsed time and usage, unknown costs or limits, residual risks, and the best next hypothesis. If no change is kept, say so and retain the original baseline.

Static instruction checks should cover these paths: a normal improvement records and keeps a gate-passing gain; a noisy or rejected change is reversed only with permission; an ambiguous metric pauses for clarification; an invalid harness stops without an attempt; and an exhausted budget returns the partial record without another retry.

Read [work lifecycle](../references/work-lifecycle.md) for authorized records, checkpoints, review pauses, and recovery. Read [delegated execution](../delegated-execution/SKILL.md) before any optional delegation.
