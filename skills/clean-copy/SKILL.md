---
name: clean-copy
description: Reimplement the current branch on a new branch with a clean, narrative-quality git commit history. Use when asked to make a clean copy branch, clean up commit history by replaying work, or rebuild a branch as reviewable commits.
---

# Clean copy

Reimplement the current branch on a new branch with a clean, narrative-quality commit history suitable for reviewer comprehension.

## Workflow

1. Gather context:
   - Source branch: `git branch --show-current`.
   - Working tree: `git status --short`.
   - Commits since the repository's configured base branch: `git log <base-branch>..HEAD --oneline`.
   - Diff summary: `git diff <base-branch>...HEAD --stat`.
2. Validate the source branch:
   - Ensure there are no uncommitted changes or merge conflicts.
   - Compare the source branch with the configured base branch and report any divergence. Do not pull or rebase implicitly.
3. Choose the new branch name:
   - Use the user's requested name when provided.
   - Otherwise use `<source-branch>-clean`.
4. Analyze the diff:
   - Study all changes between the source branch and the configured base branch.
   - Understand the final intended state before recreating it.
5. Create the clean branch from the configured base branch. Do not pull or push implicitly.
6. Plan the commit storyline:
   - Break the implementation into self-contained logical steps.
   - Each step should read like a stage of development in a tutorial.
7. Reimplement the work:
   - Recreate the final changes step by step.
   - Commit after each coherent idea.
   - Use clear commit subjects and descriptions.
   - Keep each intermediate commit coherent enough to pass the repository's normal hooks. Never bypass hooks; if a slice cannot pass, split or revise it.
8. Verify correctness:
   - Confirm the final tracked tree exactly matches the original source branch (the commit history intentionally differs).
   - Run the repository's final checks with normal hooks enabled.
9. If the user also requested a pull request, use the `pr` skill.
   - Include a link to the original branch in the PR description.

## Rules

- Never add yourself or an AI tool as an author, contributor, or co-author.
- Never include AI attribution in commits or PR content.
- The final clean branch must be identical to the source branch.
- Do not force push unless the user explicitly asks for it.
