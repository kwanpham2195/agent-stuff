# AGENTS.md

Codex CLI output: avoid Markdown tables by default; they render poorly there. Use short bullets or key: value lines instead. Only use a table when explicitly requested.

## Core

- “Make a note” => edit AGENTS.md (shortcut; not a blocker). Ignore CLAUDE.md unless explicitly asked.
- Skills are canonical for tool workflows. Keep this file to hard rules only.
- Skills listed in `~/.agents/.skill-lock.json`, skills named `plannotator-*`, `aside-browser`, `herdr`, and `tuistory` are installed and updated externally; keep them live-only under `~/.agents/skills/`, outside this repository.
- Install skills from external sources with `npx skills`.
- Config/dotfiles/packages/global tools: use `config-manager`.
- ship => changelog, commit in groups, push, pull.
- Editing here/skills: token-efficient, relaxed grammar, terse descriptions.
- Changelogs: match file style; follow `skills/references/release-notes-guide.md`; prefer one bullet per entry on one line. Do not hard-wrap changelog bullets just because prose is long.

## Writing style
- Lead with the main point. Use concise paragraphs and plain language; lists for parallel items or steps. Match technical detail to the user's background.
- Develop one main idea per paragraph, with sentences that build coherently on each other and enough explanation to support the point.

- Follow `skills/technical-writing/SKILL.md` for general prose and technical documentation.
- For technical blog posts, also follow `skills/references/blog-guide.md` and use the `write-tbp` skill.
- For release notes, also follow `skills/references/release-notes-guide.md`.

Avoid using slop words or phrases like "Bottom Line:" in conclusions, "delve," "foster," "leverage," "it's worth noting," "importantly," "Question? Answer." or "This isn't about X. It's about Y.", "genuinely" or hyphenated compound descriptions and adjectives. Do not use concluding summary statements such as "In short:..", "The simplest mental model is:...".

State the intended action directly. Avoid adding what you won't do, what will remain unchanged, or how you'll separate or categorize results. Do not use contrastive framing such as "X, not Y" or "X—not Y" that introduces an unprompted alternative that the user didn't ask about. Avoid invented compound labels like "exact-head checks" and "editorial-row layouts", vague qualifiers, and canned transitions; use plain verbs and prepositions to state the actual relationship directly.


## Project Defaults

- Need upstream file: stage in /tmp/, then cherry-pick; never overwrite tracked files.
- Bugs: add regression test when it fits.
- Fixes/refactors: delete old paths by default. "Shipped" means in a release Git tag, not main/GitHub/PR. Compat needs explicit contract: public API/CLI/config/data, tagged upgrade path, security boundary, or observed prod state. If unsure, ask before keeping aliases/shims/fallbacks. Tests alone are not contracts.
- Always ask before removing functionality or code that appears intentional.
- Docs: read repo docs before coding; follow `skills/technical-writing/SKILL.md` when writing documentation; update docs/changelog for user-visible behavior changes.
- Writing code: `coding-standards` and `write-discoverable-code` apply by default, not on request. `coding-standards` covers TypeScript and Go only - for other languages follow local precedent and say which precedent you followed.
- On the first task or resume in a working directory, make the cheap workspace routing check in `skills/references/context-routing.md`; small work stays inline. `~/.agents/context/` is private live local working data excluded from this repository. Human-facing design docs, ADRs, and changelogs keep repository-required homes; `CONTEXT.md` follows the domain-modeling glossary contract.
- New deps: quick health check for recent releases/commits/adoption.
- Upstream source for deps/repos: use `$librarian` skill.

## Developer Workflow
- Clarify ambiguous user intent, scope, acceptance, or permission before acting on the uncertain part; do not silently choose an interpretation. Look up factual unknowns yourself. Ask a small batch of related questions with tradeoffs and a recommendation; ask sequentially when one answer determines the next question.
- If product intent, scope, or success is ambiguous, use `define-outcome` to establish observable acceptance and required evidence. Reuse sufficient existing criteria; small tasks keep them inline.
- For planning, developer review, work spanning sessions, or tracker handoffs, read `skills/references/work-lifecycle.md`. It defines checkpoints, resumption, feedback, and acceptance for both direct and delegated work. Keep small tasks inline.
- For technical review/discussion, prefer `show-me`: diagrams, structural diffs, pseudocode, and concrete contracts, with short rationale. Use an existing document or PR when sufficient; keep proposals and accepted decisions distinct.
- At a requested human review or unresolved user decision, present the ready artifact/response, name what needs approval and what waits, then end the turn. Resume dependent work only after a clear response; silence or closing a review UI is not approval. Follow `skills/references/work-lifecycle.md` for review and resumption.

- Before branch/PR work: read repo `AGENTS.md`/`CONTRIBUTING.md` or any must read in the repo, check `git status -sb`, confirm base branch, and pull/ff only when user asked or workflow says so.
- Branch names: repo rules first. Otherwise use `feat/<slug>`, `fix/<ticket-or-slug>`, `test/<slug>`, or `chore/<slug>`; include ticket ID when branch/PR/commit rules require it. If required ticket missing, ask once.
- Stacked work: small ordered slices. preserve stack blocks; no Sapling/`sl` wording.
- Plans: include repo `AGENTS.md` update when a new repo-specific rule, command, branch convention, or verification lesson should persist.
- Attribution: use configured git author. Do not add AI/Codex/Pi/co-authored/generated trailers unless user or repo explicitly requires them.
- Verification report: list exact commands run and blockers. If lint/toolchain is noisy or blocked, say why and name the narrower proof that still ran.
- UI/live bugs: reproduce and verify in same surface/profile. Unit tests alone do not prove the live bug is gone.
- Before implementation, inspect the relevant code, callers, tests, and repository conventions. Exploration is sufficient when you can identify the change location, affected contracts, and verification approach. No separate research artifact is required. Investigate a remaining consequential uncertainty as a bounded question; use `research` when it needs deeper evidence gathering.

- Do not write tests for reversible, low-impact changes that mirror the implementation. If you do choose to verify your work with tests, make sure that the tests are meaningful and necessary to verify implementation.
- Run tests appropriate to the change and complete required checks. Once those pass, broaden or repeat testing only when new changes, failures, or unresolved concerns justify it; otherwise, continue toward completing the task.

## PR / CI

- Pasted GitHub issue/PR: check `git status -sb`, report dirty state, and inspect the issue/PR read-only. Push or pull only when authorized by the task; a pasted URL alone grants neither.
- PR refs: use gh pr view/diff, not web search.
- PRs: prefer rewriting/fixing the PR, then merging it, over closing and committing equivalent files directly.
- Landing own draft PR after explicit land request: ignore draft status; mark ready if needed and continue.
- fix ci: consent to pull, commit, push; fix/rerun/watch until CI green.
- CI: gh run list/view; rerun/fix until green when asked.
- rewrite commits + land: clean stack, agreed focused proof only, force-push, merge. No Codex review, PR-body proof polish, or CI babysitting unless asked.
- Replies: cite fix + file/line; resolve threads only after fix lands.
- User-facing fixes/landed PRs: changelog unless pure test/internal.
- Contributor PR authors should not edit changelog; maintainer/AI adds entry at merge.
- After landing: final includes 2-5 sentence recap of what landed.
- After landing: checkout main/master, pull --ff-only, verify git status -sb, then final.

## Runtime Safety

- PR/issue body edits: fetch via REST + jq -r, never gh pr/issue view --json body --jq .body. Example: gh api repos/OWNER/REPO/pulls/NUM | jq -r '.body // ""' > /tmp/body.md; inspect before --body-file; stop if it starts with " or shows literal \n.
- Secrets: never run env, set, export -p, or broad secret regex dumps in a normal shell. Query exact names only; redact values.

## Git

- If cwd is in a git repo: work there. Do not jump to sibling checkout unless asked.
- Branch switch/checkout ok when task needs it and repo rules allow.
- End in visible checkout/branch user expects.
- Safe by default: git status/diff/log. Push only when user asks.
- Branch changes require user consent.
- Destructive ops forbidden unless explicit: reset --hard, clean, restore, rm, etc.
- NEVER use `git add -f`, `git add -A`, or `git add .` (stage explicit paths)
- Don’t delete/rename unexpected stuff; stop + ask.
- Avoid manual git stash; if Git auto-stashes during pull/rebase, that’s fine (hint, not hard guardrail).
- Commit: Repo convention (git history) / else conventional commits
- Unrecognized changes: assume other agent; keep going; focus your changes. If it causes issues, stop + ask user.
- If user types a command (“pull and push”), that’s consent for that command.
- Big review: git --no-pager diff --color=never.
- Multi-agent: check git status/diff before edits; ship small commits.
- No amend unless asked.
- Never `git commit --no-verify`
- Never force push.
- Rebase: if conflict in a file you did not modify, abort and ask the user.

## Build / Test

- Before declaring implementation complete, run the repository's required gates (lint/typecheck/tests/docs as applicable) and verify acceptance criteria. For checkpoints or partial handoffs, record checks run, failures, and pending verification; do not delay preserving progress to run completion gates.
- Keep it observable (logs, panes, tails, MCP/browser tools).

## Code Search

Use `zvec_grep_search` when workspace-grounded wording or location is unknown, or when semantic, fuzzy, relationship, chronology, causality, comparison, or cross-file synthesis is required. Use `fffind`/`ffgrep` or native `rg`/`grep` for exact paths, identifiers, filenames, quotations, regexes, or exhaustive occurrence searches.

### zvec-grep (`zg`)

- MCP tool `zvec_grep_search` first. Use the `zg` CLI when MCP is unavailable (Pi, plain shell, scripts) or when you need `--rg`, `index`, `status`.
- Routes: positional query = hybrid lexical+semantic; `--fts` exact anchors; `--vector` pure semantic; `--fuse` one ranked list; `--rg` exhaustive managed ripgrep. MCP names them `query`/`queries`, `fts`, `vector`, `fuse`.
- Mixed task (known symbol, answer spans files): one call with semantic intent in `query` and the symbol in `fts`, then verify with `rg`/read.
- Narrow with tool filters, not post-filtering: `-g/--glob`, `-t/--type`, `--symbol-type`, `--modified-after`, `--limit` (default 7).
- MCP `root` must be an absolute workspace root; the CLI uses cwd.
- Returned snippets count as read. Do not re-open the file just to confirm them.
- `possibly_stale` with `background_refresh: running` is normal. Re-query, or force `--refresh wait` (MCP `freshness: wait_for_fresh`), only when the answer depends on a just-edited file.
- Indexed search needs an index. Unindexed workspace fails with `INDEX_MISSING` on both MCP and CLI; `--rg` still works without one. Check with `zg status`.
- Ask before `zg index`. It is a persistent write: `.zvec-grep/` at the repo root (already in the global gitignore), plus a one-time ~27 MiB model download.
- `zg index` needs no `--embedding`; it falls back to the built-in default `local/potion-code-16m-v2`. Pass `--embedding` only to override. Existing indexes keep their stored model.
- Embedding runs local. Do not run `zg auth grant` (Remote Embedding) without asking.
- Shared daemon: `zg server status` / `zg server on`. If MCP calls hang, restart the daemon; do not rebuild the index.

## Tools

### Shell

- macOS `sed -i` needs an empty arg: `sed -i '' …`. Prefer a node one-liner or `perl -pi -e`.
- Quote every glob; zsh expands `--include=*.ts` and `*.md` before the tool sees it.

### trash

- Move files to Trash: `trash …` (system command).

### Browser and terminal routing

- Default to `agent-browser` for browser automation. Use `aside-browser` only when explicitly invoked by the user; never select it automatically, including for logged-in sites. Use `terminal-browser` when requested or when continuing in a browser already opened there.
- Prefer `herdr` for dev servers, watchers, logs, and pane management when running inside Herdr (`HERDR_ENV=1`); this is the user's standing preference. Fall back to `tmux` when Herdr is unavailable and a suitable tmux session exists. Otherwise ask which surface to use. Follow the selected tool's session and ownership safeguards.
- Use `tuistory` for agent-driven TUI interaction and terminal UI tests. Do not select it merely to host a background server. Respect an existing project's process wrapper and reuse its sessions rather than starting duplicate processes.
- Keep these selection preferences here; do not fork externally maintained skill bodies to encode them. Selection does not authorize installation, upgrades, stopping shared processes, or bypassing the governed subagent workflow.

## Skills invocation

- If any skills mentioned you cannot see in your available_skills, first find them in project-local skills, otherwise find them in global ~/.agents/skills/

## User Override

- If the user's instructions conflict with any rule in this document, ask for explicit confirmation before overriding. Only then execute their instructions.

## Delegation

- For an explicit advisor request, or before offering one for consequential tradeoffs or a failing approach, read `skills/delegated-execution/advisor.md`. Default to asking before spawning; honor off/automatic preferences within their stated scope. Routine advice stays inline.

- Delegate when independent work or context isolation earns the coordination cost and the user allows it; follow `delegated-execution` when delegating.
