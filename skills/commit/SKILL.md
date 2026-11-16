---
name: commit
description: "Read before making git commits. Defines scope, message format, and authorization limits."
---

## Automatic local commits

Global policy authorizes local commits for completed, verified slices of the current task. Commit each coherent slice after its required checks and acceptance criteria pass; do not wait for a separate commit request or accumulate a large finished task. This includes code, documentation, skills, and chezmoi configuration. Explicit task restrictions and repository-specific rules take precedence.

Ask before committing when ownership is mixed or required verification is blocked. Preserve incomplete work in its authorized context record; make a WIP commit only when explicitly requested. A completed proposal may be committed as a proposal while implementation approval remains pending. Context checkpoints retain their lifecycle permission even when the implementation they describe is incomplete.

## Commit procedure

1. Determine the authorized changes from the user's request and any supplied paths or globs. Inspect `git status -sb` and the scoped diff. Ask if unrelated changes make ownership or scope ambiguous.
2. Follow the documented repository convention; if absent, inspect recent subjects with `git log -10 --pretty=format:%s`. If neither establishes a convention, use `<type>(<scope>): <summary>` or `<type>: <summary>` without a scope. For example: `fix(parser): reject empty input`. Use `feat`, `fix`, `docs`, `refactor`, `chore`, `test`, or `perf`; imperative summary, at most 72 characters, no trailing period. Add a body or breaking-change marker only when needed.
3. Stage explicit intended paths only. Review `git diff --cached` for scope, secrets, and unintended generated files before committing; if pre-staged changes are outside scope, stop and ask rather than including or unstaging them. Never include another owner's changes without permission.
4. Commit with hooks enabled. Fix failures only within authorized scope; report blockers. Use configured attribution, with no added sign-off or AI/co-author trailer unless explicitly required.
5. Report the commit SHA and inspect `git status -sb` for remaining changes. Committing does not authorize pushing, amending, or switching branches.
