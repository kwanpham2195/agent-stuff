# Skill mechanics

- Use `name` and a concise trigger-based `description` in SKILL.md frontmatter. Shared Claude/Codex skills retain Claude's `disable-model-invocation` boolean alongside Codex invocation policy; do not remove it merely because Codex's validator rejects it.
- Preserve existing invocation policy. Explicit-only skills use `disable-model-invocation: true` in SKILL.md for Claude and `policy.allow_implicit_invocation: false` in `agents/openai.yaml` for Codex. For new skills, change automatic discovery only when the user requests it. Check both controls when changing shared-skill policy; neither establishes Pi behavior.
- An explicit-only skill still needs a description. A router may point the user to it; do not assume routing overrides its invocation policy.
- Shared material belongs in a plain reference linked by its callers. Create another skill only when it needs independent discovery or explicit invocation.
- Retain existing names and paths when consolidating bodies unless renaming or removal is authorized; verify inbound references when changing them.
