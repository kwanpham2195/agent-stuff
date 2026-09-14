---
name: technical-writing
description: Write or review technical documentation, READMEs, RFCs, and other developer prose. Choose the document's purpose, write actionable instructions, and remove ambiguity while preserving technical accuracy.
---

# Technical writing

Write so a tired engineer can understand the document on the first read. Choose its purpose, address the reader directly, control how much each sentence carries, and remove ambiguous wording. Cut words that add no meaning; keep articles, conditions, and context that make the text precise. When a style rule makes a sentence worse, use a clearer construction.

Apply these standards within the user's scope and repository conventions. Review requests return findings unless edits are authorized. Preserve technical meaning and accepted decisions; flag missing evidence rather than inventing facts to finish the prose. Avoid rewriting unchanged passages without a concrete clarity problem.

## Choose the document's purpose

Use the Diátaxis distinction to choose the primary purpose. A filename or the word "blog" does not determine it. Separate and link substantial material that serves a different purpose. Keep a short supporting example or explanation in place when splitting it would impede the reader.

- **Tutorial:** help a learner build something successfully. State what they will build, supply prerequisites, and give steps with visible results. Explain what they should see after important actions. Keep background short and link deeper explanation.
- **How-to:** help a competent reader accomplish a task. Name the goal, give actionable steps, and include conditions, meaningful alternatives, and recovery where needed. Link background and exhaustive reference information.
- **Reference:** support lookup. Mirror the API, configuration, command, or other system described. State options, defaults, limits, errors, and version constraints. Use consistent entries and generate facts from code when practical.
- **Explanation:** answer a bounded why question. Describe constraints, decisions, history, alternatives, and tradeoffs. Distinguish observed facts from interpretation and make the reasoning explicit.

For plans, RFCs, PR descriptions, commits, and release notes, preserve their required format instead of forcing the whole artifact into a Diátaxis category. Apply the sentence and accuracy checks below to their prose.

Load specialized guidance only for the work at hand:

- Technical blog posts: [blog-guide](../references/blog-guide.md) and [write-tbp](../write-tbp/SKILL.md) own the article structure and workflow.
- Release notes: [release-notes-guide](../references/release-notes-guide.md) owns content selection and format; repository release conventions take precedence.
- Skills or agent instructions: [writing-for-agents](../writing-for-agents/SKILL.md) owns instruction contracts and context management. The applicable skill-creator workflow owns skill authoring and validation.
- PRs and commits: use the relevant writing/commit workflow for their format and authorization. This skill does not grant permission to publish or commit.

## Consult examples when useful

For a concrete example of a writing technique, read the relevant section of the [writing examples reference](../references/writing-guide.md) or [documentation examples reference](../references/docs-guide.md). These preserve earlier examples for comparison. Load them only when an example helps the current task. This skill and `unslop` remain authoritative when older guidance differs.

## Address the reader directly

- Use "you" for instructions and name the system for facts. Use "we" when a tutorial or article describes a shared exercise or the team's work.
- Prefer present tense and active voice. Name the actor when it matters. Passive voice is useful when the actor is unknown or irrelevant.
- Write procedural steps as commands. Put the condition or warning before the action it governs. Present the common case before exceptions.
- Use numbered lists for ordered steps and bullets for parallel facts. Keep list items grammatically parallel. Follow the user's table preference and repository format.
- Use sentence-case headings that identify the task or finding. Task headings start with a verb; reference headings name the thing readers look up. Keep the heading hierarchy coherent.
- Use descriptive links, code formatting for symbols and commands, and the project's UI-label formatting. Follow repository indentation in code examples.
- Avoid "simply," "easy," and "obviously" in procedures. State the action and what the reader should observe.

## Keep instructions easy to parse

These checks adapt controlled-language principles; they are not a claim of formal STE compliance.

- Give each procedural sentence one instruction. Separate independently meaningful actions so readers can follow and verify them.
- Split sentences that require rereading to recover their subject, condition, or consequence. Vary sentence length; a long sentence with one clear point can remain intact.
- Prefer the everyday word unless the technical term is more precise. Keep the same term for the same concept and the same verb for the same action.
- Keep articles and necessary verbs. "Remove the backup file" is clearer than compressed labels posing as instructions.
- Replace trailing phrases such as "ensuring seamless operation" with a concrete consequence or remove them. Keep an "-ing" form when it states a precise action or relationship clearly.

## Remove ambiguity

- Place "only," "not," and similar modifiers next to what they modify. "The worker fails only during shutdown" states a different claim from "Only the worker fails during shutdown."
- Give every pronoun a clear referent. Repeat the noun when "it," "they," "this," or "which" could refer to more than one thing.
- Break long noun strings into explicit relationships: "the script that checks the import budget."
- Keep the verbs and connecting words that reveal sentence structure. Do not drop a verb in the second half of a comparison.
- Clarify what "and" and "or" join. Use "both," "either," or an explicit condition when grouping changes the meaning. Spell out ambiguous slashes in prose. Preserve literal paths and established technical notation.
- Avoid idioms, invented metaphors, and needless synonym changes. Use real codebase terminology. Define an unfamiliar named pattern when first needed.

Before:

> Configuration of the import budget parameters is performed via budget.json. Running with --write, which updates the budget, should only be done when lowering it. If exceeded, CI fails.

After:

> `budget.mjs` reads the import limit from `budget.json`. CI fails if the import count exceeds that limit. Run `budget.mjs --write` only to lower the limit.

Treat this as a sentence-editing example, not a verified command for the current repository.

## Apply unslop

Read and apply [unslop](../unslop/SKILL.md) to every document this skill writes, edits, or reviews. Run its scan, rewrite, and self-audit before returning the result. For a read-only review, report the findings without editing the document.

The upstream skill owns the pattern catalog and punctuation rules. It is installed externally at `~/.agents/skills/unslop/SKILL.md` and stays outside chezmoi. If it is unavailable, report the missing dependency rather than claiming the pass ran.

## Verify and finish

Review only the requested artifact or passages:

1. Does the structure serve the reader's task or question? Preserve required templates and link deeper material where useful.
2. Can the reader execute each instruction with its prerequisites, conditions, and expected results? Check runnable examples in the relevant environment when authorized; mark untested examples explicitly. Label partial snippets and show the context needed to place them.
3. Are symbols, files, commands, defaults, counts, and claims correct for the referenced version? Inspect source evidence and record reproducible commands for derived counts or measurements. Do not imply that a planned check ran.
4. Can any modifier, pronoun, noun string, or conjunction be read two ways? Does each concept retain one name?
5. Can wording be removed without losing meaning, necessary context, or permissions? Keep the details needed to resume or act safely.

Return the revised artifact or review findings, with relevant verification and remaining uncertainty. A writing task does not authorize code changes, publication, or edits to the writing standards themselves.
