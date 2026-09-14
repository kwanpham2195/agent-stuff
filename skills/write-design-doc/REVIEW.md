# Getting feedback, and closing out

Most design reviews fail the same way: a meeting is scheduled as the first step. It should be the last.

## The order

1. **One reviewer first.** Before the doc goes anywhere else, give it to a single trusted reader — the person who will implement it, the client, or whoever owns the system upstream. Early confusion is cheaper to fix in front of one person than ten.
2. **Then asynchronous reading.** Send it out and give reviewers at least two working days to read it uninterrupted. Broadcasting to a large group at once invites the bystander effect: everyone assumes somebody else is reading carefully.
3. **Resolve in the document.** Answer comments by changing the doc, not by explaining in chat. If a reviewer misread something, every later reader will misread it the same way unless the text changes.
4. **A meeting last, if at all.** Reserve it for the contentious points that text could not settle. Never hand out a doc nobody has seen and read excerpts aloud while people listen — that produces agreement, not thinking.

## Working the comment threads

Drive threads to a close, aggressively. A doc whose margins are full of unresolved discussion becomes unreadable within a year: nobody can tell which suggestions were taken.

After two or three exchanges on the same thread, stop and promote it: move it into **Open issues** as its own section, representing each position fairly and naming who holds it. That gives a real disagreement the room a margin comment cannot, and it keeps the main text clean.

When an issue settles, summarize the reasoning at the top of the section, update the design to match the decision, and move it to Resolved issues. The rationale is the part future readers need.

## Tooling

Use something with inline comments, stable URLs for each thread, and visible change history. The URLs matter — a thread you cannot link to is a thread you cannot promote or reference later.

## After it ships

Run a blameless postmortem on the design itself: what took longer than expected, which dependency let you down, what the doc failed to consider. Aim it at the process, not at people.

Collecting answers anonymously first, then aggregating by how often and how badly each thing bit, keeps the discussion out of groupthink. Take the aggregate into a meeting and turn it into changes for the next design.
