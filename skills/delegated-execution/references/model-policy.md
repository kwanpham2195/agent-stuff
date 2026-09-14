# Delegation model policy

Use these defaults for delegated work. The harness column identifies the child's execution harness, including when the parent uses another harness. Explicit user choices for the assignment take precedence.

| Harness | Exploration | Implementation | Review | Advisor |
|---|---|---|---|---|
| Claude Code | Sonnet / medium | Opus / medium | Opus / high | Fable / high |
| Pi | Luna / medium | Terra / medium | Sol / high | Sol / high |
| Codex | Luna / medium | Terra / medium | Sol / high | Sol / high |

## Resolve models and roles

- Pi model IDs: Luna = `openai-codex/gpt-5.6-luna`; Terra = `openai-codex/gpt-5.6-terra`; Sol = `openai-codex/gpt-5.6-sol`.
- Codex model IDs: Luna = `gpt-5.6-luna`; Terra = `gpt-5.6-terra`; Sol = `gpt-5.6-sol`. Verify availability through the active harness before dispatch.
- Claude Code aliases: `sonnet`, `opus`, `fable`. Verify the installed version supports the selected alias and effort control.
- Pi role mapping: exploration = `scout`; implementation = `worker`; review = `reviewer`; advisor = `oracle`.
- Classify other agents by their assigned task. For roles outside this table, retain configured defaults; do not infer a new assignment.

## Apply before dispatch

1. Read the selected harness's configuration and discover its supported models and thinking/effort controls. Follow its required launch protocol.
2. Resolve the table entry or explicit user override into native launch settings. Set both model and thinking/effort explicitly where supported; a prompt asking the child to use a model does not configure it.
3. If the model or requested level is unavailable, unsupported, or cannot be selected through the permitted launch path, stop that dispatch and ask before substituting. Do not switch execution modes to work around the limitation.
4. Report the role, selected model, and thinking/effort at launch. Check resolved runtime metadata when exposed; report any mismatch and follow the harness recovery protocol. Do not claim a selection was verified when only the requested configuration is known.
5. On resume, check the stored run contract. If it differs from the intended selection and cannot be changed, ask before starting a replacement run.

This document records the desired policy; native configuration and runtime evidence establish whether it is applied. Updating this table does not itself update harness settings. Keep native configuration changes within the user's authorized scope.
