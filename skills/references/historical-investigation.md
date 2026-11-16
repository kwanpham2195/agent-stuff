# Historical investigation

Use during research, including RPI's research steps, when a current decision depends on why behavior appeared, changed, or remained. Keep the question bounded to the relevant contract and revision range.

1. Establish current behavior from source, callers, tests, and available runtime evidence. Name the historical question and the evidence that would settle it.
2. Trace the relevant path or symbol through Git history. Useful read-only probes include `git log --follow -- <path>`, `git log -S'<symbol>' -- <path>`, `git log -G'<pattern>' -- <path>`, and `git blame -L <start>,<end> -- <path>`. Inspect the full relevant patch with `git show <commit> -- <path>` and its surrounding code. Blame identifies a touching commit, which may only be formatting or a move. For defensive code such as a retry, timeout or flag, also look for incident or outage evidence where access permits; ordinary history often omits why it was added.
3. Follow cited issues, PR discussions, tests, release notes, and decision documents where access permits. Use the existing repository-host tooling owner. Do not fetch new history or modify remote state without the required permission. Record shallow history, missing discussions, renamed paths, and inaccessible sources as limits.
4. Separate what each source establishes. A patch shows what changed; a contemporary statement supports stated intent; a test demonstrates only its exercised conditions. Inferred motivation remains an inference, even when plausible. A commit author or message alone does not establish the current requirement.
5. Check whether later changes superseded the decision and whether the original constraint still exists. Preserve conflicting evidence. Absence from the searched history does not prove absence everywhere, and historical intent does not authorize removing present behavior.

Return the answer with revision, path or discussion citations, search bounds, observed facts, inferred intent, and unresolved evidence. Explain the consequence for the current decision separately. Use research's existing artifact and checkpoint rules rather than creating a second history record.
