# Getting feedback, and closing out

Most design reviews fail the same way: a meeting is scheduled as the first step. It should be the last.

## The order

1. **Choose the needed review.** For substantial designs, start with one trusted reader when useful. Use the user's designated reviewers and existing team workflow. A completed draft does not require a new review gate unless the task or repository requires one.
2. **Allow asynchronous reading.** When review is authorized, provide enough time for the document's depth and the team's schedule. Prepare the document and proposed recipients before asking for any missing sharing permission. Do not impose a fixed waiting period or send it to new recipients without authority.
3. **Resolve in the document.** Answer comments by changing the doc, not by explaining in chat. If a reviewer misread something, every later reader will misread it the same way unless the text changes.
4. **A meeting last, if at all.** Reserve it for the contentious points that text could not settle. Never hand out a doc nobody has seen and read excerpts aloud while people listen — that produces agreement, not thinking.

## Working the comment threads

Drive threads to a close, aggressively. A doc whose margins are full of unresolved discussion becomes unreadable within a year: nobody can tell which suggestions were taken.

After two or three exchanges on the same thread, stop and promote it: move it into **Open issues** as its own section, representing each position fairly and naming who holds it. That gives a real disagreement the room a margin comment cannot, and it keeps the main text clean.

When an issue settles, summarize the reasoning at the top of the section, update the design to match the decision, and move it to Resolved issues. The rationale is the part future readers need.

## Tooling

Use the user's chosen review channel. Inline comments, stable thread URLs, and change history help with substantial shared reviews; ordinary chat with the exact document version also works. Do not require a new tool or publication merely to review a local draft.

## After it ships

When requested or warranted by observed problems, run a blameless retrospective on the design: what took longer than expected, which dependency failed, and what the doc missed. Keep it focused on the process.

Collecting answers anonymously first, then aggregating by how often and how badly each thing bit, keeps the discussion out of groupthink. Take the aggregate into a meeting and turn it into changes for the next design.
