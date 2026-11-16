---
name: pr
description: "Create, update, inspect, fix, watch, or land pull requests. Use for PR preparation, maintenance, review follow-up, CI monitoring, and explicitly requested merging."
---

# PR

Create or update a pull request for the current branch. Creation and ordinary updates remain governed by this workflow; maintenance and landing use the explicit modes below.

## Modes

- `inspect` reads the exact repository, PR, base, head, checks, reviews, and findings and returns a bounded report.
- `fix` changes only the owning branch after the user authorizes the finding and records a falsifiable reproduction or source proof.
- `watch` observes the active forge's checks and review state without changing code, review threads, or merge state. In T3 use the parent-owned app watch/unwatch controls under maintenance; a monitoring request does not authorize fixes or landing.
- `land` requires an explicit land request and follows [landing](references/landing.md); it never follows from `watch` or a green check alone.

Read [maintenance](references/maintenance.md) for these boundaries, exact-head evidence, finding triage, bounded reruns, and human-note preservation. Read [landing](references/landing.md) only for an explicit landing request. Stacked PR topology belongs to the installed `gh-stack` owner; do not use Graphite or an external orchestrator.

Use `../write-pr/SKILL.md` as the standards reference for PR titles, descriptions, release notes, API changes, code changes tables, and human-note preservation.

## Workflow

1. Gather context:
   - Current branch: `git branch --show-current`
   - Working tree: `git status --short`
   - Existing PR: `gh pr view --json number,title,url 2>/dev/null`
   - Recent branch commits: `git log <base-branch>..HEAD --oneline 2>/dev/null || git log -3 --oneline`, using the repository or existing PR's configured base branch.
2. Check for overlapping work so we don't step on a teammate's toes:
   - List open PRs touching the same area: `gh pr list --state open --json number,title,url,author,headRefName,updatedAt`, and search for related work: `gh pr list --search "<keywords>" --state open`.
   - Compare their changed files against ours (`gh pr view <number> --json files --jq '.files[].path'`) to judge real overlap, not just a shared filename.
   - If someone already has a PR open for this: prefer building on their work over racing it. Offer to base our branch on theirs, contribute a review or a follow-up commit, or hand our changes over. Only open a competing PR when the approaches genuinely diverge, and when we do, link to theirs and explain how ours differs so the choice is easy for reviewers.
   - Surface what you found to the user before proceeding when there's meaningful overlap.
3. Prepare the branch:
   - If on the configured base branch, create a descriptive branch only when branch mutation is within the user's requested scope.
   - Commit only relevant, explicitly scoped changes, excluding secrets and private content. A content-only PR request does not authorize new code commits.
   - Push when required to create or update the requested PR. Never force push.
4. Run an initial review pass before asking a human to look. For a large or complex diff, use delegated reviewers when delegation is available and authorized; otherwise review inline. Inspect the diff from the configured base branch, then fold clear findings into scoped fixes:
   - Does the change actually solve the stated problem, end to end, rather than papering over a symptom?
   - Does it leave the codebase better than we found it — clearer names, no dead or duplicated code, no drive-by regressions?
   - Any weird abstractions, premature generality, or unnecessary code that a reviewer would flag? Prefer the smaller, more direct version.
   - Sweep the diff's added comments for slop, following `../write-pr/SKILL.md` § The comment sweep. On an update, this catches whatever the branch grew since the PR was opened, which on a long-lived branch is most of it.
   - Fix what's clearly worth fixing so the human review starts from a strong diff. If a finding needs a product or design call, raise it with the user instead of guessing.
   - Commit and push fixes from this pass only when those mutations are within the user's requested PR scope. Never force push.
5. If no PR exists, create one with `gh pr create`. When running in a T3 thread, immediately link every opened PR, including each stack layer, to the thread using its actual URL or repository/number. A delegated creator immediately returns the PR identity so its parent registers it before further PR work; it does not own monitoring. Reconcile an uncertain create/link receipt before retrying rather than opening a duplicate.
6. If a PR exists, read its title, labels, and number with `gh pr view --json title,labels,number`. When the body is needed, fetch it through the REST API and inspect the changed-file list with `gh pr view --json files --jq '.files[].path'`.
7. Update the title or body with `gh pr edit` if the existing PR does not match the current diff or the `write-pr` standards.
8. Search for related issues and link them in the PR description with `Closes #123` or `Relates to #123` where appropriate.
9. Share the PR URL with the user. In T3 maintain the correct thread's PR links as ownership or PR identity changes; unlink only a mistaken or obsolete link, never as permission to close/delete a PR. Requested monitoring follows the [T3 watch protocol](references/maintenance.md#t3-registration-and-monitoring).

## Handling problems

Committing automatically runs hooks. Fix formatting, lint, type, or import issues when the fix is mechanical.

If a hook failure requires meaningful product or implementation decisions, stop and ask the user how to proceed.

Never force commit or force push.

## Rules

- Follow `../write-pr/SKILL.md` for all PR content standards.
- Do not include AI attribution in commit messages, PR titles, or PR descriptions.
- Do not add yourself or an AI tool as a co-author.
