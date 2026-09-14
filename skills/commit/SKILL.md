---
name: commit
description: "Read before making git commits. Defines scope, message format, and authorization limits."
---

1. Determine the authorized changes from the user's request and any supplied paths or globs. Inspect `git status -sb` and the scoped diff. Ask if unrelated changes make ownership or scope ambiguous.
2. Follow the documented repository convention; if absent, inspect recent subjects with `git log -10 --pretty=format:%s`. If neither establishes a convention, use `<type>(<scope>): <summary>` or `<type>: <summary>` without a scope. For example: `fix(parser): reject empty input`. Use `feat`, `fix`, `docs`, `refactor`, `chore`, `test`, or `perf`; imperative summary, at most 72 characters, no trailing period. Add a body or breaking-change marker only when needed.
3. Stage explicit intended paths only. Review `git diff --cached` before committing; if pre-staged changes are outside scope, stop and ask rather than including or unstaging them.
4. Commit with hooks enabled. Fix failures only within authorized scope; report blockers. Use configured attribution, with no added sign-off or AI/co-author trailer unless explicitly required.
5. Report the commit SHA and inspect `git status -sb` for remaining changes. Committing does not authorize pushing, amending, or switching branches.
