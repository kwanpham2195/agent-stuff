# agent-stuff

Personal agent instructions, reusable skills, and a local context management framework.

## Contents

- `AGENTS.md` contains the global operating rules.
- `skills/` contains the stable workflows and reference material loaded when a task needs them.
- `experimental/skills/` contains skills that depend on T3 Code and the context folders. The installer skips them unless you pass `--experimental`; see [Experimental skills](#experimental-skills).
- `context/templates/` contains empty templates for private local work records.
- `templates/USER.md` is a blank profile the installer copies to `~/.agents/USER.md` when that file is missing.
- `scripts/validate-skills.py` checks skill metadata and local references in `skills/`, `experimental/skills/` and `pi/skills/`.
- `pi/` contains the Pi agents, extensions, themes, skills, modes and example settings.
- `model-policy.yaml` and `scripts/model-policy.py` configure and resolve model choices for supported workflows.

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

Name a skill when you want its specific method or deliverable, for example: "Use show-me to explain this flow" or "Use code-review to review this branch". Some skills require an explicit request or agreement. Use your agent's skill invocation mechanism when needed; command syntax and available tools depend on the agent. Naming one skill does not require listing every supporting skill it uses.

## Skills

The package contains the stable skills below, plus the Pi-specific skills listed under [Pi setup](#themes-and-pi-skills). Each skill is loaded when its task matches; you do not need to name every skill in a request.

### Planning, collaboration, and review

[`define-outcome`](skills/define-outcome/SKILL.md), [`delegated-execution`](skills/delegated-execution/SKILL.md), [`docs-review`](skills/docs-review/SKILL.md), [`in-your-own-words`](skills/in-your-own-words/SKILL.md), [`ketchup`](skills/ketchup/SKILL.md), [`matthew-mode`](skills/matthew-mode/SKILL.md), [`prototype`](skills/prototype/SKILL.md), [`recall`](skills/recall/SKILL.md), [`retro`](skills/retro/SKILL.md), [`sharpen`](skills/sharpen/SKILL.md), [`show-me`](skills/show-me/SKILL.md), [`triage-work`](skills/triage-work/SKILL.md), and [`walkthrough`](skills/walkthrough/SKILL.md).

### Implementation and verification

[`code-review`](skills/code-review/SKILL.md), [`coding-standards`](skills/coding-standards/SKILL.md), [`correct`](skills/correct/SKILL.md), [`create-verification-skill`](skills/create-verification-skill/SKILL.md), [`go-coding-standards`](skills/go-coding-standards/SKILL.md), [`maintain-verification-skill`](skills/maintain-verification-skill/SKILL.md), [`typescript-coding-standards`](skills/typescript-coding-standards/SKILL.md), and [`write-discoverable-code`](skills/write-discoverable-code/SKILL.md).

### Git, issues, and delivery

[`commit`](skills/commit/SKILL.md), [`issue`](skills/issue/SKILL.md), [`librarian`](skills/librarian/SKILL.md), [`pr`](skills/pr/SKILL.md), [`take`](skills/take/SKILL.md), [`update-changelog`](skills/update-changelog/SKILL.md), [`write-issue`](skills/write-issue/SKILL.md), and [`write-pr`](skills/write-pr/SKILL.md).

### Documentation and writing

[`mermaid-png`](skills/mermaid-png/SKILL.md), [`product-description`](skills/product-description/SKILL.md), [`technical-writing`](skills/technical-writing/SKILL.md), [`unslop`](skills/unslop/SKILL.md), [`visual-explainer`](skills/visual-explainer/SKILL.md), [`write-design-doc`](skills/write-design-doc/SKILL.md), [`write-tbp`](skills/write-tbp/SKILL.md), and [`writing-for-agents`](skills/writing-for-agents/SKILL.md).

### Local tools and setup

[`apple-notes`](skills/apple-notes/SKILL.md), [`apple-reminders`](skills/apple-reminders/SKILL.md), [`optimize-metric`](skills/optimize-metric/SKILL.md), [`orbstack`](skills/orbstack/SKILL.md), [`prepare-system-design-interview`](skills/prepare-system-design-interview/SKILL.md), and [`bro`](skills/bro/SKILL.md).

The repository does not contain workspace records, session transcripts, credentials, or authentication data. Keep context created from the templates under `~/.agents/context/` and out of Git unless you intentionally publish a specific artifact.

## Experimental skills

[`experimental/skills/`](experimental/skills) holds skills that are still changing and that only work in one environment. They are not part of the stable catalog and the installer skips them by default.

- [`desk`](experimental/skills/desk/SKILL.md) runs a T3 Code thread as a desk that starts work, answers what needs attention, triages and changes rules.
- [`agent-pickup`](experimental/skills/agent-pickup/SKILL.md) runs planned tasks unattended in T3 Code through packets, a dispatcher thread and lane threads in worktrees.
- [`scrum-master`](experimental/skills/scrum-master/SKILL.md) runs an assigned T3 Code check of workflow progress and nudges task owners.

They need T3 Code for threads and scheduling, and the context folders from [`context/templates/`](context/templates) for work records (see the [context model](#context-model)). They also rely on the stable skills: once installed they sit beside them in `~/.agents/skills`, so their relative links resolve there, not in the repository tree. Stable skills mention them only as optional.

Install them with the stable set:

```bash
./scripts/install --experimental
```

The flag can be combined with `--pi`. It checks the experimental destinations for collisions like the others and stops before writing when one exists.

## Install

Review `AGENTS.md` and the skills before installing them. These files encode personal workflow and permission choices that you may want to change.

Run the installer from a clone:

```bash
./scripts/install
```

Options: `--pi` adds the [Pi setup](#pi-setup), `--claude`, `--codex` and `--cursor` connect those harnesses ([below](#connect-your-harness)), and `--experimental` adds the [experimental skills](#experimental-skills). Run `./scripts/install --help` for usage.

The installer copies the global instructions and stable skills into `~/.agents`. `--experimental` adds the [experimental skills](#experimental-skills). It also copies `templates/USER.md` to `~/.agents/USER.md` unless that file exists; fill it in with your name, languages, time zone and writing preferences. It stops when another destination already exists. Move or remove an existing destination only after reviewing it.

### Connect your harness

The installer writes to `~/.agents`. Each harness needs to find the instructions and skills there. Pass the flags on the first install, because the installer stops when `~/.agents` already has these files.

| Harness | Flag | What it links |
| --- | --- | --- |
| Claude Code | `--claude` | `~/.claude/CLAUDE.md` to `~/.agents/AGENTS.md`, and `~/.claude/skills` to `~/.agents/skills` |
| Codex | `--codex` | `~/.codex/AGENTS.md` to `~/.agents/AGENTS.md`; Codex reads user skills from `~/.agents/skills` itself |
| Cursor | `--cursor` | Writes `~/.cursor/rules/agents.mdc` as an always-apply rule containing a copy of `AGENTS.md`. Cursor reads user skills from `~/.agents/skills` itself. Cursor does not read a global `AGENTS.md` file, so re-run or re-copy after you edit the instructions |
| Pi | `--pi` | See the [Pi setup](#pi-setup) |

Set `CLAUDE_HOME`, `CODEX_HOME` or `CURSOR_HOME` to use other locations. The installer stops instead of replacing an existing `CLAUDE.md`, `AGENTS.md`, `agents.mdc` or `skills` path there. To connect a harness after installing, create the same links by hand once you have reviewed the existing files, for example `ln -s ~/.agents/AGENTS.md ~/.codex/AGENTS.md`.

T3 Code runs the Codex and Claude Code harnesses, so it needs no separate flag: connect the harness you select in T3 Code. The [experimental skills](#experimental-skills) also need the T3 Code tools and the context folders, and a registered workspace.

The model-policy resolver requires Python 3 and PyYAML. Review the model choices in `model-policy.yaml` for your providers and available models before using delegation.

Validate the repository with:

```bash
python3 scripts/validate-skills.py
```

## Skill requirements

Skills provide instructions; the tools they drive must be installed separately.

- The [experimental skills](#experimental-skills) (`desk`, `agent-pickup`, `scrum-master`) need T3 Code and the context folders. Create the folders from [`context/templates/`](context/templates) (see the [context model](#context-model)); they read and write work records there and use T3 Code threads and scheduling. `triage-work` also reads those work records.
- `apple-notes` and `apple-reminders` need macOS, with the [`memo`](https://github.com/antoniorodr/memo) and [`remindctl`](https://github.com/steipete/remindctl) command-line tools.
- `orbstack` needs macOS with [OrbStack](https://orbstack.dev).
- `mermaid-png` needs Node.js.

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
- `btw.ts` opens a side conversation for a question without adding that thread to the main conversation.
- `files.ts` provides file browsing, opening, editing, and diff actions through `/files`.
- `goal.ts` stores and enforces a long-running objective in the Pi session tree.
- `head.ts` shows the beginning of the current conversation branch.
- `no-sleep.ts` uses macOS `caffeinate` while the agent is active.
- `notify.ts` sends an OSC desktop notification when Pi finishes and waits for input.
- `permission-gate.ts` asks before dangerous shell commands such as recursive deletion or `sudo`.
- `prompt-editor.ts` adds mode and model controls to the prompt editor.
- `session-breakdown.ts` reports session, message, token, model, and cost activity over time.
- `todos.ts` manages claimable file-based tasks under `.pi/todos` or `PI_TODO_PATH`.
- `uv.ts` redirects common Python environment and package commands through `uv`.

### Themes and Pi skills

The Pi package includes `catppuccin-macchiato`, `dayowl`, `modern-dark`, and `nightowl` themes.

Two Pi-specific skills are included:

- `pi-skill-creator` creates, evaluates, and improves skills for Pi and OpenCode.
- `tldraw-offline` controls an open tldraw Desktop canvas through its local API.

### Settings and optional services

`pi/settings.example.json` records the package list, model selection, subagent model assignments, terminal preferences, and theme used by this setup. Model availability depends on your Pi version and authenticated providers. Review the complete file before activating it. Pi may download and execute every third-party entry in `packages` when it loads the active settings.

`pi/mcp.example.json` configures Linear through `mcp-remote`. Remove it if you do not use Linear. Authentication remains in each service's credential storage and is not included here.

Activate either example explicitly after review:

```bash
cp "$HOME/.pi/agent/settings.example.json" "$HOME/.pi/agent/settings.json"
cp "$HOME/.pi/agent/mcp.example.json" "$HOME/.pi/agent/mcp.json"
```

If an active file already exists, merge the settings you want instead of replacing it.

`pi/modes.json` supplies the `default` and `fast` model presets used by `prompt-editor.ts`.

## Install external skills

The global instructions use `rpi` for substantial work and `agent-memory-repo` for global memory. Install these separately before using those workflows. Other external skills are optional. Review third-party skills before installing them; `npx skills` records their source and supports later updates.

```bash
# Research, implementation workflow, and global memory
npx skills add humanlayer/skills -g --skill rpi
npx skills add AgentMemoryRepo/agentmemoryrepo -g --skill agent-memory-repo

# Browser automation and visual PR evidence
npx skills add vercel-labs/agent-browser -g --skill agent-browser
npx skills add vercel-labs/agent-desktop -g --skill agent-desktop
npx skills add vercel-labs/before-and-after -g --skill before-and-after

# Document conversion
npx skills add firecrawl/anydoc -g --skill convert-documents-to-markdown

# Terminal automation: drives and verifies TUIs and interactive CLIs in a real PTY
npx skills add anomalyco/terminal-control -g --skill terminal-control
cargo install terminal-control
```

The instructions also name `rex` for servers, watchers, logs and background terminal work. The Rex app installs that skill itself (`rex skill setup`); it is not available through `npx skills`.

The `skill-creator` skill is supplied by Codex as a system skill in this setup, so this repository does not install a separate copy.

`agents-md`, which guides writing `AGENTS.md` files, is mentioned by the bundled instructions but is not bundled. This repository has no public upstream source to cite for it. Use your own guidance, or a skill from a source you trust, when you write `AGENTS.md`.

Install and configure the applications a skill drives only when you use that workflow.

## License

MIT. See [LICENSE](LICENSE) and [third-party material](THIRD-PARTY.md).
