---
name: pr
description: "Create, update, inspect, fix, watch, or land pull requests. Use for PR preparation, maintenance, review follow-up, CI monitoring, and explicitly requested merging."
---

# PR

This skill prepares and publishes a pull request for the current branch. It owns creating a PR and ordinary updates to one. Maintenance and landing run in the modes below.

## Modes

- `inspect`: read the repository, PR, base, head, checks, reviews, and findings at their exact identities, then return a bounded report.
- `fix`: change only the branch that owns the code, and only after the user authorizes the specific finding. Record a reproduction that could fail, or proof from the source.
- `watch`: observe checks and review state on the active forge. Do not change code, review threads, or merge state. In T3, use the parent-owned watch and unwatch controls described in maintenance. A request to monitor does not authorize fixes or landing.
- `land`: only on an explicit request to land. Follow [landing](references/landing.md). A `watch` result or a passing check never triggers it.

Read [maintenance](references/maintenance.md) for the boundaries of these modes, evidence tied to the exact head, finding triage, bounded reruns, and how to preserve human notes. Read [landing](references/landing.md) only when the user explicitly asks to land. The installed `gh-stack` skill owns stacked PR topology. Do not use Graphite or any outside orchestrator.

The standards for PR titles, descriptions, release notes, API changes, change tables, and preserving human notes live in `../write-pr/SKILL.md`. Apply them.

## Workflow

1. Collect context.
   - The current branch: run `git branch --show-current`.
   - Uncommitted changes: run `git status --short`.
   - An existing PR for this branch: run `gh pr view --json number,title,url 2>/dev/null`.
   - The commits on the branch: run `git log <base-branch>..HEAD --oneline 2>/dev/null || git log -3 --oneline`. Use the repository's configured base branch, or the existing PR's base.
2. Look for overlapping work before you add to the pile.
   - List open PRs with `gh pr list --state open --json number,title,url,author,headRefName,updatedAt`. Search for related ones with `gh pr list --search "<keywords>" --state open`.
   - Read the file list of each candidate with `gh pr view <number> --json files --jq '.files[].path'`. Overlap means touching the same code, not only sharing a filename.
   - When someone already has a PR for the same goal, build on it instead of racing it. Offer to base your branch on theirs, add a review or follow-up commit, or give them your changes. Open a competing PR only when the two approaches really differ. In that case, link to theirs and say how yours differs so reviewers can choose easily.
   - If the overlap is significant, tell the user what you found before you continue.
3. Get the branch ready.
   - If you are on the base branch, create a descriptively named branch, but only if changing branches is within what the user asked for.
   - Commit only the relevant changes the user scoped. Never commit secrets or private content. A request that is only about PR text does not allow new code commits.
   - Push when that is needed to create or update the PR. Never force push.
4. Review your own diff before any human sees it. For a large or complex diff, delegate to reviewers if delegation is available and authorized. Otherwise review it yourself. Read the diff against the configured base branch and turn clear findings into small fixes. Ask:
   - Does the change solve the stated problem end to end, or does it only hide a symptom?
   - Is the codebase better afterward, with clear names, no dead or duplicated code, and no unrelated regressions?
   - Would a reviewer flag an odd abstraction, speculative generality, or code that is not needed? If so, pick the smaller and more direct version.
   - Do the comments the diff adds read well? Sweep them using the comment sweep section of `../write-pr/SKILL.md`. On a long-lived branch, an update picks up most of the comments added since the PR opened.
   - Fix what is clearly worth fixing so the human review starts from a strong diff. When a finding needs a product or design decision, take it to the user and do not guess.
   - Commit and push fixes from this pass only if that is within the PR scope the user requested. Never force push.
5. If there is no PR yet, create one with `gh pr create`. In a T3 thread, link each PR you open to the thread right away, using its URL or its repository and number. That includes every layer of a stack. A delegated creator returns the PR identity at once so its parent can register it before any further PR work. The delegate does not monitor. If the result of a create or link call is uncertain, check the actual state before you retry, so you do not open a duplicate.
6. If a PR already exists, read its title, labels, and number with `gh pr view --json title,labels,number`. When you need the body, fetch it through the REST API. Get the changed files with `gh pr view --json files --jq '.files[].path'`.
7. Edit the title or body with `gh pr edit` whenever the PR no longer matches the current diff or the `write-pr` standards.
8. Look for related issues and link them in the description with `Closes #123` or `Relates to #123` as fits.
9. Give the user the PR URL. In T3, keep the right thread's PR links accurate as ownership or PR identity changes. Unlink only a link that is wrong or obsolete. Unlinking never allows you to close or delete a PR. If the user asked for monitoring, follow the [T3 watch protocol](references/maintenance.md#t3-registration-and-monitoring).

## When something goes wrong

Commits run hooks automatically. If a hook fails on formatting, lint, types, or imports, fix it when the fix is mechanical.

If fixing a hook failure means making a real product or implementation decision, stop and ask the user.

Never bypass hooks or force push.

## Rules

- Apply `../write-pr/SKILL.md` to everything that goes into a PR.
- Leave AI attribution out of commit messages, PR titles, and PR descriptions.
- Do not list yourself or an AI tool as a co-author.
