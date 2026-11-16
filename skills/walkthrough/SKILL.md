---
name: walkthrough
description: Walk the user through code or a change in chat, one chapter per reply. Use for walkthroughs of a PR, branch, commit, diff, or code area.
---

# Walkthrough

Guide the user through a fixed snapshot in chat. Use plain prose, short paragraphs, and concrete examples. For an explanation of a code flow, use [show-me](../show-me/SKILL.md) to orient the user to the capability, actors, and entry point, then trace a scenario. For a saved HTML visual, use [visual-explainer](../visual-explainer/SKILL.md) when requested. Neither replaces this chapter-by-chapter chat workflow.

## Capture and plan

Infer the source from the request. Support a GitHub PR with `gh`, a Bitbucket PR with `bb`, a branch against its base, uncommitted changes, a commit or range, or existing code in a file, directory, feature, or flow. A request to walk through code without a change means the code itself: entry points, call flow, and key types. Ask only when the intended source is truly ambiguous.

When nothing is named, use the current branch against its base if it has commits ahead; otherwise use uncommitted changes. If neither exists, ask what to cover. Resolve the actual base from the PR or repository conventions; do not guess if it is unclear.

Capture the source once before planning. Record repository identity, source and scope, head and base SHAs where applicable, and the exact patch or code snapshot used. For uncommitted changes, capture staged and unstaged content and relevant untracked files in private state, with hashes; a HEAD SHA alone does not pin them. For existing code, pin the revision and capture any relevant working-tree content. Preserve enough evidence to reproduce every excerpt, including old and new line numbers for deletions. Never edit the source to capture it.

Build chapters of related sections from that snapshot. Aim for at most four sections or 150 cited diff or code lines per chapter; split longer material into more chapters. Each section has a title, two to four sentences explaining the behavior, and exact cited hunks or excerpts with file and line numbers. For diffs, inventory all hunks and record the count and files of those not cited. Keep the inventory available for requests to explore omissions; uncited does not mean unimportant.

Save a small private JSON file outside the repository. Use the active workspace's work record when one exists; otherwise use a dated file under a private agent state directory consistent with [context routing](../references/context-routing.md). Record the snapshot or private evidence location and hashes, revision, chapter and section plan, current chapter, reviewed sections, and uncited hunk inventory. Do not put state in the source repository. If capture or persistence fails, say so and do not claim the walkthrough can resume.

## Present and continue

Present one chapter per reply. Start with a header such as `Chapter 2 of 4 · Sections 3–5` and the chapter title; leave review counts out of the header. For each section, give its short explanation and exact cited excerpts in fenced `diff` or language blocks, with file paths and line numbers. When a change is a set of parallel value changes, such as mapping rows, config entries or field renames, show it as a table (input, old value, new value) instead of raw diff lines, and cite the file and lines once. Do not add a per-chapter note about uncited hunks; mention uncited hunks only when the user asks or at the end of the walkthrough. End with one line naming the next chapter, for example `Next: Chapter 3, sign-in and retries`. At the last chapter, say the walkthrough is complete.

Respond to plain-language navigation such as next, go back, skip tests, or show uncovered hunks in a file. Update and save the current position when it changes. Mark a section reviewed only when the user indicates it looks good; save the mark locally and allow the user to change it. Answer questions in place without advancing. Do not offer hotkeys or command menus.

On `continue the walkthrough`, load the saved plan and progress for the intended walkthrough. If multiple saved walkthroughs are plausible, ask which one. Before each continuation or navigation, compare the source's current head with the recorded head and compare captured working-tree inputs when relevant. If it changed, say the walkthrough is outdated and offer to rebuild. Do not mix revisions or silently replace the plan; rebuild only on request, with fresh progress. If the source cannot be checked, say freshness is unknown and do not present it as current.

This is read-only apart from private walkthrough state. Do not post comments, approve, change remote review state, edit code, or commit. You may suggest a follow-up, but do not act on it as part of the walkthrough.
