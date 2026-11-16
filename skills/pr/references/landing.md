# PR landing

Use this reference only after an explicit user request to land, merge, or enable merge-when-ready. Interpret “ship” according to repository and user rules; it does not imply merging when those rules define only changelog, commit, push, and pull. A green check or `watch` mode does not grant landing authority.

## Verify the run

Resolve the repository and active forge, then inspect the exact bottom-to-top PR run:

- required checks and reviews at the current head;
- exact repository, PR, base branch and SHA, head branch and SHA, and mergeability;
- whether the head changed since the last verdict and whether its base-to-head patch identity still matches;
- unresolved findings and the owning branch for each fix.

A changed head or changed patch invalidates the affected verdict and requires fresh verification. A stacked run is contiguous: stop at the first unverified or blocked PR. Read the installed `gh-stack` skill and use its supported operations to inspect stack frontier and topology; do not duplicate stack management with Graphite or an external orchestrator.

A draft may transition to ready only when the explicit land request and current repository rules permit it. Do not retarget descendants, force-push, rebase through conflicts, close PRs, or delete branches as a default landing step. If the forge or stack owner cannot provide a required capability, stop and report the blocker.

## Land and verify

Land only the verified contiguous run within the explicit approval. Operate on one frontier PR at a time through the resolved forge's supported command, binding the mutation to the verified head with a supported expected-head precondition. Recheck identity immediately before submission; if the head changed or an atomic head guard is unavailable, stop and resolve that safety gap. Keep merge-when-ready scoped to that PR when the user requested it. Do not merge an unverified descendant or infer that an auto-merge request proves readiness.

After each landing, read the actual forge state and verify the merged commit is present on the expected base. Recompute the next frontier's base, head, checks, reviews, and verdict freshness before continuing. Once the approved run is complete, check out the expected base and use the existing fast-forward-only pull rule when the repository's landing workflow requires it. Report the actual post-landing state, not the intended state.

Return the approved run and ceiling, each exact-head verdict and producer, commands or forge actions performed, post-landing evidence, the next blocked or unverified item, and any permission or capability still missing. Updating this guidance never performs a remote or cleanup operation.
