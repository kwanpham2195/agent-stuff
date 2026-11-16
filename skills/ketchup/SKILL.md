---
name: ketchup
description: "Catch the user up on what changed in this chat since the user's last message, then list every call waiting on the user with enough detail to decide from the reply alone. Use for /ketchup."
disable-model-invocation: true
---

# Ketchup

Catch the user up on what changed in this chat since the last message the user wrote before `/ketchup`. Then lay out every call waiting on the user so the user can make it from your reply alone. Notifications and subagent results are not the user's messages. Assume the user remembers the user's last message and nothing after it.

Use the voice of [bro](../bro/SKILL.md) and the preferences in `USER.md` (writing and presentation): plain words, short sentences, Simplified Technical English for technical terms, no banned phrases. Say what changed for the user, not how you did it. Say "the tests pass", not "CI is green". Leave out hashes, file paths, commands, build numbers and test counts unless the user needs one to act. Name each PR, branch, thread or agent by a name the user would know, not a label you invented. Apply [unslop](../unslop/SKILL.md).

This skill applies to a task thread. In the Desk thread, answer "What needs me?" under [desk](../desk/SKILL.md#what-needs-me) instead.

## Gather what changed

Keep the turn read-only. Do not change code, start an app or job, post anything, write a checkpoint, message another thread, or spawn a helper. Collect:

- your own work since the user's last message, subagent reports, and messages from anyone else in this chat;
- the current state of each PR, CI run, thread and agent this chat touched;
- the task's `brief_attention` in its work state, when the thread owns one, so asks raised before the user's last message still show. Read the frontmatter only. If it disagrees with the chat, report both and say the state needs reconciling at the next checkpoint. Do not edit it.

Check each number you show against its source, and say so when you correct one.

An action item is a call or step only the user can take: a product choice, an approval, an irreversible action, access you lack, or a human gate from [work lifecycle](../references/work-lifecycle.md). Include every one still waiting, even if raised before the user's last message. Work you can do yourself is not an action item. Never invent a call to fill the reply. Silence, a closed review UI or a helper's recommendation is not an answer, so keep that ask open. A step the user did not ask for and the work does not need is not an action item. If such a step is irreversible and waiting on the user, give it one line and no visual.

One call can cover many items, such as each PR in a set awaiting merge. For each item collect its link, what it changes for users, the evidence behind your pick, its risk, and your pick. Write "unknown" for a fact the call needs and you lack. Leave out a link you do not have.

## Write the reply

Spend words on the calls, not the story. Keep what happened to one short paragraph, not counting pictures, and leave out work that changed nothing for the user. Give each item a sentence or two, so the reply grows with the number of items. Never cut items to save words, and never replace items with a count or a link. A link can add depth, but the reply alone must be enough to decide.

Open with one short sentence that names what waits on the user, or says nothing does. If nothing happened and nothing waits, say so and stop.

Then show what happened, pictures first: screenshots and videos the work produced, then any diagram that explains a change. Then one short bullet per thing the user asked for: what came of it, and whether it is done, still running, failed or not checked. Write each line the way you would say it out loud: "Search was slow from a missing index", not "Search review: done". Each line must stay true read alone. Name any bug found and fixed on the way. Never mark something done that still waits on the user, and leave out anything the action items cover. Under the summary, give at most three short lines that change what the user knows or must do, then one line naming work you can still do yourself.

Then list the action items. Ask the call the user owns (merge, approve, pick) and give your pick, labeled as a recommendation. A step you would take first goes in your pick, as does anything that must happen first and anything that cannot be undone. Give the number or link of each PR, issue, thread or agent a call is about. Link threads as `[title](t3-thread://v1/<threadId>)`.

- **One item:** one bullet with the call, your pick, what it changes for users, the evidence, and the risk. Name the item once.
- **Shared call:** write the call and pick once. Then one bullet per item, riskiest first: link and name, what it changes for users, evidence, risk. Name an item's pick only where it differs. State risk even when low, such as "Low risk: only the colors change."
- **Choice between options:** give every option the work weighed, each with what it gets the user and what it costs, plus its current state. The costs are the risk, so add no separate risk line. When screenshots show the options, write each option's gain and cost under its screenshot.

Say what waiting costs only when it is more than a delay, such as a deadline or lost data. Keep proposals distinct from accepted decisions.

## Visuals

A visual is a picture: a screenshot, a video, a diagram, a chart, or a generated image. A table is not a visual.

Draw when a picture beats sentences: how a design works, a PR stack with each PR's state, a before and after, or options side by side. Never draw a status list, an action list, or boxes with nothing connecting them. Never state a fact twice, in text or across visuals. Choose the form with [show-me](../show-me/SKILL.md).

Keep each visual readable at a glance: at most six boxes, at most eight words in each, plain words rather than tags like "Tests: pass". A fact that needs a sentence belongs in the text or nowhere.

In T3 Code, render diagrams and charts as in-chat HTML; elsewhere render diagrams to PNG with [mermaid-png](../mermaid-png/SKILL.md). Never show Mermaid text. Embed screenshots and videos inline when the change is visible. If a visible change has none, mark its summary line "No screenshot yet" and say what changed on screen. Draw only from facts you have, never invent a number, and never draw or generate a picture of a screen you did not capture. Link only artifacts that exist.
