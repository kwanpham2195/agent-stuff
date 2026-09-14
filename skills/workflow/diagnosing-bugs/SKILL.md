---
name: diagnosing-bugs
description: "Use when diagnosing bugs or performance regressions. Requires evidence for the reported symptom and verification against the original scenario."
---

Follow reproduce → investigate → fix when authorized → verify. Revisit an earlier step when evidence changes the hypothesis. Record why a step is blocked or inapplicable rather than silently skipping its evidence.

## 1. Establish the reproduction

Read relevant project context and enough code to reach the user's exact symptom. Choose the shortest practical feedback loop: an existing test, CLI/HTTP invocation, browser interaction, or a small isolated harness. Match the reported environment/profile where it affects behavior.

Record starting conditions, trigger, expected behavior, and actual behavior. An unrelated exception or a check that only asserts “did not crash” is insufficient when the report concerns incorrect output.

Minimize the scenario where practical while retaining the failure. For intermittent bugs, record failures/trials and test conditions; a single clean run is not proof of a fix. For performance, use comparable inputs and conditions before and after, recording the measured quantity and baseline.

**Ready to investigate:** the symptom is observed and a repeatable trigger is identified, or the available evidence and reproduction limitation are explicit. If blocked, report attempts and request the missing environment, redacted artifact, or instrumentation authority. Source inspection may narrow the cause but does not establish a reproduced failure.

## 2. Test a falsifiable hypothesis

State a prediction, run a targeted probe, and record its result. Consider alternatives when evidence is ambiguous; do not impose a fixed hypothesis count.

```text
Hypothesis: The retry appends an item already persisted by the first request.
Prediction: Replaying the same request ID creates a second row.
Probe: Replay the captured request against an isolated fixture; count matching rows.
Result: Record the observed count, then retain or reject the hypothesis.
```

Change one relevant variable at a time where feasible. Use targeted instrumentation and tag temporary logs with a unique prefix for cleanup. If a probe contradicts the hypothesis, revise it; do not keep patching the first plausible explanation.

**Ready to fix:** evidence connects the cause to the reported symptom. A diagnosis-only request ends with findings and uncertainty; it does not authorize implementation.

## 3. Fix through the real failure path

When implementation is authorized, add a regression test at the seam that exercises the actual failure when feasible. Observe it fail before the fix and pass afterward. If no suitable seam exists, report the limitation instead of substituting a shallow test. Keep the original reproduction so minimization does not hide the broader scenario.

## 4. Verify and close the investigation

Rerun the original scenario and required checks appropriate to the change. For intermittent/performance issues, repeat comparable trials or measurements and report residual uncertainty. Remove task-owned temporary instrumentation and account for retained diagnostic artifacts; do not delete shared resources.

Use this compact result shape, inline or in the existing work artifact:

```text
Symptom / environment:
Reproduction: command or actions; expected → observed
Cause: supporting evidence, or remaining hypothesis
Change: fix made, or diagnosis-only recommendation
Verification: actual commands/results; original scenario; regression evidence
Remaining: untested cases, blockers, retained artifacts, next action
```

Keep credentials in environment variables and redact sensitive output and captured artifacts. Request a redacted artifact if safe handling is uncertain. For a necessary human-operated loop, use `scripts/hitl-loop.template.sh`. Architecture follow-ups require user interest.
