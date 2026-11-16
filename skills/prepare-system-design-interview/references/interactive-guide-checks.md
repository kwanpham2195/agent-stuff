# Interactive guide checks

Read this only when creating or reviewing an interactive or HTML interview guide. Match the requested format and actual use context. Do not add an application merely to present a short brief.

## Interaction and information design

Keep candidate and interviewer artifacts separate. Make the private guide's audience clear. Put explanations next to the step they explain, reduce repeated cards, and collapse secondary detail.

Provide editable diagram sources. Check actors, arrow direction, message names, and branch guards against the scenario. Distinguish architecture from a lifecycle trace. If the guide has manual lifecycle steps, each step must update the diagram, detail text, state, and relevant architecture emphasis together. Backward steps, reset, and branch changes must also agree.

Provide clear jump navigation. Phase switching and section jumps should move focus and scroll to the intended content below any sticky header. Preserve keyboard navigation, visible focus, and useful control names.

Preserve notes through phase changes, theme changes, resize, and supported export. State whether storage is session only, persistent locally, or remote, and what export includes. Do not imply that local storage is private from other users of the same browser profile. For session-only notes, show a persistent loss warning and warn before refresh or close where browser support permits. Disclose warning limitations. Do not silently add remote storage.

## Verify live behavior

Use the existing [agent-browser](../../agent-browser/SKILL.md) workflow when available. Check for a sibling skill by name, then the environment's available skills. If unavailable, report the gap and agree on a suitable live browser method before claiming browser verification. This reference remains usable without that skill.

Use real clicks and keyboard actions, not only script evaluation or screenshots. Test applicable controls, phase changes, navigation, diagram editing, lifecycle branches, notes, persistence, and exports. For diagrams, inspect labels, arrow direction and clipping in both themes and narrow layouts; verify that trace controls keep the diagram, explanation and selected state synchronized. Browser checks establish presentation and behavior, not architectural correctness; separately check the diagram against its contracts and scenario traces. Reproduce bugs before fixing them and retest the same interaction after a fix.

Review function and appearance separately. Inspect every visible section, including the top toolbar, expanded secondary content, and failure or empty states. Check:

- Buttons and selects for alignment, consistent heights, readable labels, dropdown behavior, and focus rings.
- Text and controls for readability and contrast in supported themes.
- Desktop and mobile layouts in the actual use context, including narrow widths near layout boundaries. Distinguish accidental page overflow from deliberate local scrolling.
- Sticky headers, focus placement, long notes, diagrams, and collapsed content after resize or theme changes.
- Native paginated PDF output if printing is offered. Inspect actual pages for clipping, overlaps, repeated headers, and readable backgrounds. Dark theme selector specificity and grid pagination can produce dark pages or overlapping content even when the browser print preview looks plausible.

Choose sizes and themes from the intended context rather than copying fixed dimensions from a previous guide. A bounded sweep does not establish that all UI problems are fixed.

## Review and handoff

Give any reviewer the exact approved scope, artifact audience, and permitted actions. Review does not authorize edits. The parent or owner must inspect the actual diff and evidence before acceptance.

Report the tested interactions, layouts, themes, and export paths, with evidence locations and known failures or untested areas. Distinguish live functional tests, visual review, and static inspection. If native PDF or a browser action was unavailable, say so rather than substituting a claim of completion.
