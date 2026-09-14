---
name: handoff
description: "Prepare a checkpoint for another session or agent to resume research, discussion, planning, or implementation without the conversation."
disable-model-invocation: true
metadata:
  argument-hint: "What will the next session be used for?"
---

Read [work-lifecycle](../references/work-lifecycle.md) for checkpoint contents, its copyable checkpoint format, and resume checks. Use that format when creating a new handoff; keep an existing artifact's structure when updating it. Tailor the handoff to the next session's purpose; if unspecified, preserve the current objective and next action.

1. Identify the authoritative entry artifact. Update it when authorized, keeping decisions, evidence, unresolved questions, progress, and next action current. Link other sources instead of duplicating their contents.
2. If no entry artifact exists, use the requested path. For continuing project work, use the lifecycle's durable location. For a one-off transfer with no project home, resolve the OS temporary directory, create a unique file, and explain that temporary storage may be cleaned up. Respect read-only scope by returning the checkpoint inline.
3. Include exact relevant skill paths and why to load them. Identify resources unavailable in the target environment; a local path is not an accessible link for another machine or a tracker recipient.
4. Include only observed execution and verification results. Preserve pending decisions and withheld permissions. Exclude credentials and unnecessary personal information; do not use a handoff to authorize additional actions.
5. Return the absolute path or inline checkpoint, the next concrete action, and any blocking resource gap. Tell the next agent to reconcile current state before repeating commands or continuing work.

Do not create a second full summary when an existing plan or research artifact already carries the context. A short entry note linking authoritative sources is enough. Publishing a tracker handoff uses the `issue` skill and requires authorization.
