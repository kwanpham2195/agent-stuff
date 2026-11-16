---
name: docs-review
description: "Review a documentation draft or change before it is shown to the user or published: facts, regressions, writing standards, structure and rendering. Use for docs, Confluence pages, READMEs, QA or test plans, Postman or API guides and diagrams, including drafts a delegate wrote."
---

# Docs review

Review a draft against its sources, the previous version and the writing standards before anyone reads it as finished. A fact check alone is not a review. Run every pass below, fix what you can, and report the rest.

## Inputs

Collect these before reviewing. If one is missing, say which pass it limits.

- The draft and the current published or committed version.
- The sources for its claims: code and tests for implemented behavior, recorded decisions for agreed scope, and live evidence for observed behavior in one build and environment.
- The workspace or page-set maintenance guide, if one exists. It can own page ownership, writing rules and what to leave out.
- The other documents that state the same facts: sibling pages, diagrams, API collections, test plans and FAQs.

## 1. Regressions

Diff the draft against the current version.

- Every removed sentence, link, image, attachment reference, anchor, rule ID or test-case ID needs a reason tied to the requested change. Restore the rest.
- IDs stay unique and stable. Check that no new item reuses an existing ID.
- Unchanged text stays unchanged. Revert rewording the task did not ask for.
- Title, hierarchy and the page's owner-facing scope stay as they were unless the task changed them.

## 2. Facts

- Trace each changed or new claim to its source. Mark claims you could not trace.
- Treat diagrams, examples, request bodies and expected results as claims too. A diagram that shows an old call order is stale.
- When the change alters a fact, find every other document that states it and list the ones that now disagree. Fix them in the same change when the task covers them; otherwise report them.
- Record source conflicts instead of choosing the convenient claim.

## 3. Writing

Apply the maintenance guide, [technical writing](../technical-writing/SKILL.md), [reviewable writing](../references/reviewable-writing.md) and [unslop](../unslop/SKILL.md). Check these failures by name, because they survive a quick read:

- **Walls of prose.** A paragraph that carries several cases, steps or conditions becomes a list, a table or several paragraphs.
- **Hidden sequence.** Steps a reader performs in order are a numbered list.
- **Parallel items in prose.** Fields, cases, options or outcomes that share a shape go in a table or bullets.
- **Test cases.** Each case states its setup, action and expected result separately, so a tester can mark pass or fail without rereading.
- **Lead.** Each page and section opens with what the reader needs, not background.
- **Slop.** Run the unslop scan and self-audit on every revision, including revisions a delegate wrote.

## 4. Format and rendering

- Run the target format's checks. For Confluence, read [the confluence skill](../confluence/SKILL.md#confluence-format-checks) and validate storage with its `validate_storage.py` when editing several pages.
- Render the result the way readers see it: the Confluence page after publish, the Markdown preview, or the PNG for a diagram. Check headings, tables, lists, code blocks, images and unexpected blank gaps or line breaks.

## 5. Report

Before publishing, show the user what changes, per document:

1. What changed, as a short before-and-after list. Link a side-by-side file for large changes.
2. Findings you fixed, in one line each.
3. Findings that need the user's decision, each with your recommendation.
4. Passes you could not run and why.

After publishing, report the link, the version and the rendering check you ran.

## Delegated drafts

Name this skill and the maintenance guide in the delegate's brief. Run every pass on the returned draft yourself. Do not accept a draft because its facts check out.
