# Autonomous runs

Use this reference when the user explicitly authorizes unattended progress toward a bounded outcome. The parent defines the stop predicate and retains authority over every external write.

## Define the bound

Record before launch:

- the user-approved completion predicate and the evidence that satisfies it;
- finite limits for attempts, elapsed time, and external operations, plus any available token or cost limits. Obtain approval before paid or external spend whose cost is unknown. Agent time and effort follow owner budgeting under [delegation authority](../SKILL.md#outcome-and-delegation-authority);
- the failure classes that stop the run and the owner who can recover them;
- the checkpoint location and the next permitted wake action.

The predicate must be observable. A child response, a green check, or a stale receipt is evidence to inspect and does not establish completion by itself.

Before leaving a loop unattended, confirm four things. Someone did the task once by hand or watched an agent do it. The agent has the tools and signals its owner would use, such as the verification skill, profiler and logs. Every stage checks its own output and can halt the run when the output misses the bar. Failures that repeated in earlier runs are now checks. If any of these fails, tell the user which one and keep the run attended.

## Run and wake

Launch bounded work through the harness's native path: Pi workflow calls in Pi, or the `Agent` tool in Claude Code (see [Claude Code routing](claude-code-routing.md)). Use stable child keys, one writer per cwd, and the smallest accepted unit. Native completion events wake the parent for running children: Pi completion events, or the background `Agent` completion notification in Claude Code. Do not build a wait or polling loop. A scheduled later wake is allowed only when the user explicitly requested it and the schedule is available. Schedule definitions are not permission to run remote or destructive operations.

Each iteration makes one change, checks it against the real artifact, and records what changed and whether the predicate moved. Revert a change that did not help, touching only edits that iteration made; if that would touch other work, stop and report. On a plateau, try a different approach; stop and report when no approach backed by evidence remains. Never relax the predicate to declare success.

Checkpoint before yielding or arming a later wake. Include the current predicate state, attempts and budgets consumed, exact head or external identity, artifacts, unresolved decisions, and the next action. Do not continue a task after an external write has an unknown outcome. Reconcile the target's actual state first, then either resume the same item or stop.

## Stop conditions

Stop when the predicate is met, a finite bound is exhausted, a user stop arrives, or an infrastructure failure prevents trustworthy progress. Workflow, child-launch, extension, and tool-setup failures are infrastructure blockers. Do not change execution mode or silently substitute a runner. A failed native path is a blocker and never a reason to switch runners. Preserve partial work and report the exact failure, identity, and recovery action.

A completion event does not authorize a merge, landing, comment, push, deletion, or live configuration change. The action requires user authority, parent review, and the relevant owner skill's checks. Return the predicate, iterations or attempts run, evidence actually observed, work that landed only when authorized, discarded or abandoned work with reasons, and remaining gates.
