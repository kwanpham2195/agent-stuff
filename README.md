# agent-stuff

Personal agent instructions, reusable skills, and a local context management framework.

## Contents

- `AGENTS.md` contains the global operating rules.
- `skills/` contains workflows and reference material loaded when a task needs them.
- `context/templates/` contains empty templates for private local work records.
- `scripts/validate-skills.py` checks skill metadata and local references.

## Day-to-day usage

Describe the task in ordinary language. You do not need to invoke every skill or prescribe their order. With the instructions and skills loaded, the agent uses the task to select relevant guidance. The skill catalog below is a reference for discovering capabilities and requesting a particular method.

Start with [installation](#install) and ensure your agent loads the global instructions and discovers the installed skills. The [Pi setup](#pi-setup) explains the supported installation paths and what each includes. Skills provide instructions; they do not install the tools or credentials a task may require.

```text
Your request
  ├─ outcome: what should change or be explained?
  ├─ constraints: what must remain true?
  └─ stopping point: findings, proposal, implementation, or PR?
        ↓
Agent reads the project and selects relevant skills
        ↓
Work → verification → result, evidence, and remaining questions
```

### Prompts you can reuse

For a small task, one sentence is enough:

> Fix the typo in the settings label and run the relevant check.

For a feature, describe observable behavior:

> Add status filtering to the issues page. Keep the selection in the URL so reload and back navigation preserve it. Implement and verify it; stop before committing.

For a bug, give the symptom and expected result:

> Switching projects resets my filters. Reproduce it, find the cause, fix it, and verify the original scenario. Show me the failure path briefly.

For a refactor, state what must stay the same:

> Simplify notification state management without changing public behavior. Show the current and proposed structure before implementing, then wait for my approval.

For an investigation, state the write boundary:

> Trace how authentication expires and refreshes. Explain the failure cases with a sequence diagram. Keep application files unchanged; save useful findings in this workspace's local context.

For a review, identify the comparison and whether edits are allowed:

> Review this branch against the original request and repository standards. Report actionable findings with file references. Do not edit files.

If the outcome is uncertain, start there:

> I want onboarding to feel shorter. Help me define the outcome and compare options first. Stop before implementation.

### Continue through feedback

You can refine the same task without choosing another skill:

```text
You:   Show the proposed structure before implementing.
Agent: Presents the structure, tradeoffs, and open questions.
You:   Use option A, preserve the public API, then implement and verify.
Agent: Makes the agreed change and reports the checks and limitations.
```

Be explicit about delegation and external actions when they are part of the task: "Subagents are allowed", "Commit the verified changes locally", or "Open a draft PR after checks pass". Permissions still depend on the installed tools and repository rules. Asking for a proposal ends at review; asking a follow-up question is not approval to implement it.

For work that must survive another session:

> Save a checkpoint with the decisions, verification results, blockers, and next step in this workspace's context. I will resume later.

Then resume with:

> Read the checkpoint for the notification refactor, reconcile it with the current branch, and continue the next authorized step.

The agent may ask you to register or select a workspace before saving. Small tasks can stay in chat. "Read-only" requests need separate permission to save notes; see the [context model](#context-model).

### When to name a skill

Name a skill when you want its specific method or deliverable, for example: "Use show-me to explain this flow" or "Use write-exec-plan to plan this migration". Some skills require an explicit request or agreement. Use your agent's skill invocation mechanism when needed; command syntax and available tools depend on the agent. Naming one skill does not require listing every supporting skill it uses.

## Skills

### Planning and collaboration

- [`define-outcome`](skills/define-outcome/SKILL.md) clarifies intent, scope, acceptance criteria, and required evidence before implementation.
- [`research`](skills/workflow/research/SKILL.md) investigates a bounded question and reports source-backed findings.
- [`prototype`](skills/workflow/prototype/SKILL.md) builds a disposable experiment to answer a design or state-model question.
- [`domain-modeling`](skills/workflow/domain-modeling/SKILL.md) defines project terminology and records architectural decisions.
- [`grilling`](skills/workflow/grilling/SKILL.md) runs a structured interview to test a plan, decision, or idea.
- [`grill-me`](skills/workflow/grill-me/SKILL.md) provides a short command for the standard grilling workflow.
- [`grill-with-docs`](skills/workflow/grill-with-docs/SKILL.md) runs the interview and records glossary or decision updates when authorized.
- [`show-me`](skills/show-me/SKILL.md) explains technical work with diagrams, pseudocode, structural diffs, and concrete contracts.
- [`handoff`](skills/handoff/SKILL.md) records enough state for another session or agent to resume the work.
- [`delegated-execution`](skills/delegated-execution/SKILL.md) controls subagent permissions, ownership, model selection, review, and recovery.
- [`retro`](skills/retro/SKILL.md) reviews a coding session and identifies changes worth retaining.

### Implementation and verification

- [`coding-standards`](skills/workflow/coding-standards/SKILL.md) routes TypeScript, Go, Effect, and Cloudflare changes to the applicable coding rules.
- [`write-discoverable-code`](skills/workflow/write-discoverable-code/SKILL.md) keeps names, files, errors, and comments easy to find through search.
- [`diagnosing-bugs`](skills/workflow/diagnosing-bugs/SKILL.md) requires reproduction evidence and verification against the reported scenario.
- [`code-review`](skills/workflow/code-review/SKILL.md) reviews changes against repository standards and the originating specification.
- [`create-verification-skill`](skills/create-verification-skill/SKILL.md) creates a project-specific workflow that tests an application through its user-facing interface.
- [`maintain-verification-skill`](skills/maintain-verification-skill/SKILL.md) updates an existing verification workflow as the application changes.

### Git, issues, and pull requests

- [`commit`](skills/commit/SKILL.md) defines commit scope, message format, staging, and authorization rules.
- [`clean-copy`](skills/clean-copy/SKILL.md) rebuilds branch changes as a clean sequence of reviewable commits.
- [`issue`](skills/issue/SKILL.md) captures work in a local issue or an authorized remote tracker.
- [`write-issue`](skills/write-issue/SKILL.md) defines titles, descriptions, types, and triage standards for issues.
- [`take`](skills/take/SKILL.md) claims an issue, implements it, verifies it, and opens a pull request.
- [`pr`](skills/pr/SKILL.md) creates or updates a pull request for the current branch.
- [`write-pr`](skills/write-pr/SKILL.md) defines pull request titles, descriptions, and the preflight comment sweep.
- [`update-changelog`](skills/update-changelog/SKILL.md) applies the repository's changelog and release-note rules.

### Documentation and agent instructions

- [`technical-writing`](skills/technical-writing/SKILL.md) writes or reviews developer documentation for a specific reader and purpose.
- [`writing-for-agents`](skills/writing-for-agents/SKILL.md) writes executable instructions for an agent with no conversation history.
- [`agents-md`](skills/agents-md/SKILL.md) controls the scope and content of root and nested `AGENTS.md` files.
- [`write-design-doc`](skills/write-design-doc/SKILL.md) records decisions that are expensive to reverse before implementation.
- [`write-exec-plan`](skills/write-exec-plan/SKILL.md) plans complex work across phases or pull requests.
- [`product-description`](skills/product-description/SKILL.md) documents user-visible product behavior from source, tests, and live verification.
- [`write-tbp`](skills/write-tbp/SKILL.md) writes technical blog posts about project features and implementation.
- [`to-questionnaire`](skills/to-questionnaire/SKILL.md) turns an unresolved decision into questions for the person who owns the missing context.

### Local tools

- [`config-manager`](skills/config-manager/SKILL.md) manages dotfiles and global tools through chezmoi.
- [`librarian`](skills/librarian/SKILL.md) maintains local read-only checkouts of upstream repositories for source reference.
- [`orbstack`](skills/orbstack/SKILL.md) checks and starts OrbStack when tests require Docker.
- [`obsidian-vault-config`](skills/obsidian-vault-config/SKILL.md) manages configuration shared by multiple Obsidian vaults.
- [`bro`](skills/bro/SKILL.md) restates the previous response in plain language.

The repository does not contain workspace records, session transcripts, credentials, or authentication data. Keep context created from the templates under `~/.agents/context/` and out of Git unless you intentionally publish a specific artifact.

## Install

Review `AGENTS.md` and the skills before installing them. These files encode personal workflow and permission choices that you may want to change.

Run the installer from a clone:

```bash
./scripts/install
```

The installer copies the global instructions and owned skills into `~/.agents`. It stops when a destination already exists. Move or remove an existing destination only after reviewing it.

Validate the repository with:

```bash
python3 scripts/validate-skills.py
```

## Context model

The framework treats a workspace as the boundary for related repositories, work records, and reusable local knowledge. `skills/references/context-routing.md` defines how an agent selects that workspace. `skills/references/work-lifecycle.md` defines checkpoints, review pauses, acceptance, and resumption.

Copy the empty templates when you need durable local context:

```bash
mkdir -p "$HOME/.agents/context/templates"
cp context/templates/*.md "$HOME/.agents/context/templates/"
```

Small tasks remain in the conversation. Repository documentation, issue trackers, and accepted decision records remain authoritative when they already own the information.

## Pi setup

Pi discovers the shared `skills/` tree directly after the main installer copies it to `~/.agents/skills`. Install the complete local setup, including Pi configuration, with:

```bash
./scripts/install --pi
```

The Pi option creates `~/.pi/agent/AGENTS.md` as a link to the shared global instructions. It installs the reviewed agents, extensions, themes, Pi-specific skills, and modes. It copies settings and MCP configuration under their `.example.json` names without activating them. The installer checks every destination before writing and stops without making changes when a destination exists.

If you want only the Pi package resources, install the repository through Pi:

```bash
pi install git:github.com/kwanpham2195/agent-stuff
```

The Pi package installs extensions, themes, and skills. It does not install `AGENTS.md`, settings, modes, MCP configuration, or subagent definitions.

### Extensions

- `answer.ts` extracts questions from the last assistant response and presents an interactive answer form.
- `brain-index-injector.ts` injects a project-local `brain/index.md` into the system prompt when that file exists.
- `btw.ts` opens a side conversation for a question without adding that thread to the main conversation.
- `dirty-repo-guard.ts` blocks session replacement when the current Git working tree is dirty.
- `files.ts` provides file browsing, opening, editing, and diff actions through `/files`.
- `goal.ts` stores and enforces a long-running objective in the Pi session tree.
- `handoff.ts` summarizes the active conversation into a handoff for a new session.
- `head.ts` shows the beginning of the current conversation branch.
- `no-sleep.ts` uses macOS `caffeinate` while the agent is active.
- `notify.ts` sends an OSC desktop notification when Pi finishes and waits for input.
- `permission-gate.ts` asks before dangerous shell commands such as recursive deletion or `sudo`.
- `pickup.ts` resumes a handoff saved by `handoff.ts`.
- `prompt-editor.ts` adds mode and model controls to the prompt editor.
- `session-breakdown.ts` reports session, message, token, model, and cost activity over time.
- `todos.ts` manages claimable file-based tasks under `.pi/todos` or `PI_TODO_PATH`.
- `unified-edit.ts` replaces the built-in edit tool with row operations and unified patch support.
- `uv.ts` redirects common Python environment and package commands through `uv`.

`herdr-agent-state.ts` and `moshi-hooks.ts` are excluded because their owning applications generate them. Install those integrations through Herdr or moshi-hook instead of copying generated files.

### Themes and Pi skills

The Pi package includes `catppuccin-macchiato`, `dayowl`, `modern-dark`, and `nightowl` themes.

Two Pi-specific skills are included:

- `pi-skill-creator` creates, evaluates, and improves skills for Pi and OpenCode.
- `tldraw-offline` controls an open tldraw Desktop canvas through its local API.

The local `recall` skill is excluded until its upstream provenance and redistribution terms are resolved.

### Settings and optional services

`pi/settings.example.json` records the package list, model selection, subagent model assignments, terminal preferences, and theme used by this setup. Model availability depends on your Pi version and authenticated providers. Review the complete file before activating it. Pi may download and execute every third-party entry in `packages` when it loads the active settings.

`pi/mcp.example.json` configures Linear through `mcp-remote` and a local zvec-grep server. Remove either server if you do not use it. Authentication remains in each service's credential storage and is not included here. See [Set up zvec-grep](docs/zvec-grep.md) for installation, indexing, Pi MCP configuration, privacy, and removal.

Activate either example explicitly after review:

```bash
cp "$HOME/.pi/agent/settings.example.json" "$HOME/.pi/agent/settings.json"
cp "$HOME/.pi/agent/mcp.example.json" "$HOME/.pi/agent/mcp.json"
```

If an active file already exists, merge the settings you want instead of replacing it.

`pi/modes.json` supplies the `default` and `fast` model presets used by `prompt-editor.ts`.

## Install external skills
## Install external skills

The global instructions refer to several skills maintained in other repositories. Install only the ones you use. `npx skills` records their source and supports later updates.

```bash
# Browser automation and visual PR evidence
npx skills add vercel-labs/agent-browser -g --skill agent-browser
npx skills add vercel-labs/before-and-after -g --skill before-and-after

# Document conversion
npx skills add firecrawl/anydoc -g --skill convert-documents-to-markdown

# HTML artifacts
npx skills add plannotator/effective-html -g \
  --skill design-artifact html html-diagram html-plan html-prototype html-wireframe

# Terminal and development-process tools
npx skills add herdrdev/herdr -g --skill herdr
npx skills add mitsuhiko/agent-stuff -g --skill tmux
npx skills add remorses/tuistory -g --skill tuistory

# Writing cleanup
npx skills add cursor/plugins -g --skill unslop
```

The `tuistory` skill expects its CLI:

```bash
npm install --global tuistory
```

The `skill-creator` skill is supplied by Codex as a system skill in this setup, so this repository does not install a separate copy.

Other bundled skills describe workflows for tools such as chezmoi, GitHub CLI, OrbStack, and Obsidian. Install and configure those applications only when you use the corresponding workflow.

## License

MIT. See [LICENSE](LICENSE).
