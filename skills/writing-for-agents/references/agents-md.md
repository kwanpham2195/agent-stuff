# AGENTS.md files

Use this reference when writing or revising a repository's `AGENTS.md`. The file holds rules that
stay true while the code changes. It is not a description of the code.

## What belongs in it

Keep a rule only when it applies to most tasks in the repository and an agent would get it wrong
without being told:

- conventions the code does not make obvious, such as naming, error handling or layering;
- how to find the part of the code that owns a behavior, as a search or a starting point;
- how to verify a change: the one command or check that must pass;
- constraints with a reason, such as "never edit generated files; regenerate them with `make gen`".

## What stays out

- File maps, option values, plugin lists and walkthroughs of the current code. They go stale on the
  next change. Point to discovery instead: what to search, which file is authoritative.
- Rules for one kind of work. Put them in the skill or reference that owns that work, and add a
  one-line pointer only when that skill might not load otherwise.
- Session findings, task state and anything true only today.
- Local paths, machine names and links to private notes. The file must read correctly to someone who
  has only the repository.

## Shape

- Start at the repository root. Add an `AGENTS.md` in a subfolder only when that folder has rules of
  its own; keep it shorter than the root file.
- Keep it short enough to read in full on every task. When it grows, move situational rules out
  rather than compressing wording.
- Write a warning as "Don't X; do Y instead", so the agent knows the right move.
- Write a procedure as numbered steps, and a choice between approaches as a small decision table.
- Link to deeper docs in the repository instead of copying them.

## Harnesses

Codex, Cursor and Claude Code read `AGENTS.md` themselves. Claude Code (v2.1.277 or later) reads it
when the folder has no `CLAUDE.md`, so a repository needs no `CLAUDE.md`. Add one only when a
Claude-specific rule is needed; when both exist, Claude reads only `CLAUDE.md`, so start it with
`@AGENTS.md`.
