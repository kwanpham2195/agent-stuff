# Skill and model usage audit

Read this when the retrospective asks which skills or models a session used, whether a skill was skipped, or whether one model's delegated work differed from another's.

## Count from the log

- For a Claude Code session, run `python3 -I scripts/session-usage.py <session.jsonl>`. It counts unique tool-use IDs. Report its exact numbers, not estimates from memory.
- For T3 threads, count delegate launches from `t3_thread_read` items, deduplicated as [evidence sources](evidence-sources.md#t3-code) describes.
- Count the whole thread, as [evidence sources](evidence-sources.md#t3-code) defines it. A session log continued after compaction keeps the earlier entries. State the first and last timestamps you counted.

## Skills

Report three groups separately:

1. **Loaded:** Skill tool calls in the parent.
2. **Named in briefs:** skills a delegate brief told the child to follow. Mark these as named, not confirmed, unless the child's run shows the load.
3. **Skipped:** steps where an existing skill or required guide owned the work and nobody loaded or applied it. Cite the step and the owner, for example prose published without `unslop` or the workspace writing guide.

The skipped group is the useful one. Turn each skipped owner into a candidate: a pointer, a check or a brief rule, routed to that owner.

## Models

Skip this section when the range had no delegated or subagent work.

1. Count launches per model and effort.
2. Match each delegate result to its launch and classify it: finished, stalled with nothing done, infrastructure failure (quota, sign-in, browser, transport), or the model's own mistake found in review.
3. Count launches and tasks separately. Retries and re-checks make launches higher than tasks.
4. Name the confounds: different task types, different session periods, and which model had the environment-heavy work.
5. Report a difference only when it repeats across several tasks. Route a confirmed difference to the [delegation model policy](../../delegated-execution/references/model-policy.md) as a narrow rule, for example brief size per model.

## Output

A short table per section, then candidates. Each candidate cites its evidence, its counterexample or one-off risk, and its owner.
