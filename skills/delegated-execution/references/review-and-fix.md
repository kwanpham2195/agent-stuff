# Review and fix

Use when the user asks an agent to review work and also change it. The request authorizes edits to the named paths and nothing else. The [model policy](model-policy.md#concurrent-subagents) owns role accounting and model choice: the child counts as review and implementation, and a model the user names wins.

## Before launch

1. Confirm one writer. Make no edits in the checkout while the child runs. List the unrelated uncommitted files the child must leave alone.
2. Write a brief the child can use with no conversation history:
   - the change set: commit SHAs or the diff base, and where the intent lives (issue, spec, or the user's request);
   - the repository rules to read first, such as `AGENTS.md`, the applicable coding standards, and the writing rules;
   - any upstream or source material to compare against, marked read-only;
   - what to check: fidelity to the source idea, contradiction with or duplication of neighboring rules (search before calling something missing), steps a fresh reader could misread, conflicts with the user's rules, broken links and paths, and wording;
   - the edit scope: named paths only, minimal edits that keep the intent, no new features or files;
   - what it must not do: commit, stage, stash, reset, push, install, change schedules or live configuration, start subagents, or message other threads, unless the user allowed it;
   - the checks to run and report with their exact results;
   - the report: findings by severity with `file:line` and whether each is fixed; one line per edit; what it left alone and why; what it could not verify.
3. Tell the child to report suggested changes to live configuration, such as scheduled-task contracts, instead of editing them.

## After the child finishes

1. Read the full diff of every changed file. Treat each edit as a proposal. Check it against the source idea and the user's rules, and revert or ask about any edit that adds scope.
2. Re-run the checks yourself. Do not rely on the child's report.
3. Install and commit under the repository's commit rules, using explicit paths. Leave the user's other uncommitted work alone.
4. Report to the user what the child found, what changed, what you left alone, and what remains unverified.

A second round is a new delegation with a new brief.
