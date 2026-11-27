---
name: prepare-system-design-interview
description: Prepare a bounded system design interview with a candidate brief and a separate private interviewer guide, tailored to role, seniority, and duration. Not for coding or general interview preparation.
---

# Prepare a system design interview

Before drafting or materially revising the candidate brief or private interviewer guide, read and apply [Writing reviewable artifacts](../references/writing.md).

## Establish the exercise

Take the role, seniority, and available duration. A CV is optional. Ask about missing intent that affects exercise choice, expected depth, or success criteria rather than inventing requirements. Reuse sufficient context already supplied.

Define observable competency expectations at the target seniority before writing reference reasoning. For the same-role hiring round, keep core competencies, constraints and assessment anchors consistent. Use an optional CV for additional probes, not different passing standards. Treat CV statements as claims to explore, not demonstrated skills. Choose a small set of relevant competencies and a bounded problem that can reveal them in the available time. Do not require a candidate to use technologies from their CV or from the reference design.

Separate supplied requirements, explicit interview assumptions, proposed choices, and illustrative reference answers. Confirm assumptions that materially change the exercise unless the user delegated those choices. If intent is sufficient but a material choice needs approval, you may produce a provisional draft: label it, list the approval question at handoff, and do not present it as ready for candidate use. If the missing choice prevents a coherent exercise, ask before drafting. Do not impose a universal duration, language, database, architecture, or scale.

## Produce separate audience outputs

Keep simple requested outputs in text or Markdown. Produce only the requested materials, with these audience boundaries:

- Choose a fully specified brief or staged clarification to suit the competencies. The candidate brief states the problem, supplied functional and nonfunctional requirements, exclusions and expected discussion; identify assumptions to explore and disclose constraints before assessing the design against them. Define target measurement boundaries. Private probes need not be revealed, but must not introduce hidden grading requirements.
- The private interviewer guide holds timing, clarification replies, reference reasoning, probes, and evidence notes. Read [interviewer-guide.md](references/interviewer-guide.md) when preparing it.

Keep private material out of candidate exports, downloads, print views, and linked resources. A hidden panel in the same candidate file is not separation. Do not copy a real CV or private interview notes into reusable skill resources or the candidate deliverable. Use personal context only in the authorized private preparation material and only as needed.

Use these reasoning criteria at a depth that fits the interview: impact goals, assumptions, component responsibilities and data flow, contracts, scenario traces, failure and recovery behavior, ordering, tradeoffs, risks and open issues, and operations. Ask for reasoning rather than a complete implementation plan.

Only when an actual design document is requested, consult the sibling [write-design-doc skill](../write-design-doc/SKILL.md) if available. If absent, use the criteria above without requiring that skill or a full document.

## Conditional formats and examples

- For an interactive or HTML guide, reuse [the standalone HTML skeletons](references/html-customization.md) and read [interactive-guide-checks.md](references/interactive-guide-checks.md). Preserve their design and working navigation while customizing content. HTML is optional; honor explicit text or Markdown requests.
- When a visual helps explain the design, use [show-me](../show-me/SKILL.md) to choose the useful view: architecture for responsibilities, sequence for interactions, or state diagrams for lifecycle guarantees. Do not require every view.
- When creating or adapting architecture, sequence or other diagrams, use [visual-explainer](../visual-explainer/SKILL.md). Preserve the template's visual style, editable sources and technical meaning. Keep reference answers out of candidate diagrams unless deliberately included in the approved exercise. Verify HTML diagrams through [interactive-guide-checks.md](references/interactive-guide-checks.md).
- For a concrete chat exercise example, read [chat-example.md](references/chat-example.md). Its timing, scale, and architecture are illustrative, not defaults.

## Check and hand off

Check that the phases fit the duration, clarification replies agree with the candidate brief, and the selected failures exercise the intended competencies. Ensure the reference reasoning allows defensible alternatives and the evidence scheme distinguishes assistance from independent reasoning. Uncovered topics are not automatic failures.

When maintaining this skill, walk through [evaluation cases](references/evaluation-cases.md); these instruction checks do not prove generated-interview behavior.

Report the changed or delivered paths, assumptions needing approval, checks actually performed, and remaining limits. For UI work, include functional and visual coverage separately. Do not claim behavioral or browser validation from a document walkthrough alone.
