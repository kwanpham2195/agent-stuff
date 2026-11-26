# agent-stuff

Personal agent instructions, reusable skills, and a local context management framework.

## Contents

- `AGENTS.md` contains the global operating rules.
- `skills/` contains the stable workflows and reference material loaded when a task needs them.
- `experimental/skills/` contains skills that depend on T3 Code and the context folders. The installer skips them unless you pass `--experimental`; see [Experimental skills](#experimental-skills).
- `context/templates/` contains empty templates for private local work records.
- `templates/USER.md` is a blank profile the installer copies to `~/.agents/USER.md` when that file is missing.
- `scripts/validate-skills.py` checks skill metadata and local references in `skills/` and `experimental/skills/`.
- `model-policy.yaml` and `scripts/model-policy.py` configure and resolve model choices for supported workflows.

## Day-to-day usage

Describe the task in ordinary language. You do not need to invoke every skill or prescribe their order. With the instructions and skills loaded, the agent uses the task to select relevant guidance. The skill catalog below is a reference for discovering capabilities and requesting a particular method.

Start with [installation](#install) and ensure your agent loads the global instructions and discovers the installed skills. Skills provide instructions; they do not install the tools or credentials a task may require.

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

The package contains the stable skills below. Each skill is loaded when its task matches; you do not need to name every skill in a request.

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

It checks the experimental destinations for collisions like the others and stops before writing when one exists.

## Install

Review `AGENTS.md` and the skills before installing them. These files encode personal workflow and permission choices that you may want to change.

Run the installer from a clone:

```bash
./scripts/install
```

Options: `--claude`, `--codex` and `--cursor` connect those harnesses ([below](#connect-your-harness)), and `--experimental` adds the [experimental skills](#experimental-skills). Run `./scripts/install --help` for usage.

The installer copies the global instructions and stable skills into `~/.agents`. `--experimental` adds the [experimental skills](#experimental-skills). It also copies `templates/USER.md` to `~/.agents/USER.md` unless that file exists; fill it in with your name, languages, time zone and writing preferences. It stops when another destination already exists. Move or remove an existing destination only after reviewing it.

### Connect your harness

The installer writes to `~/.agents`. Each harness needs to find the instructions and skills there. Pass the flags on the first install, because the installer stops when `~/.agents` already has these files.

| Harness | Flag | What it links |
| --- | --- | --- |
| Claude Code | `--claude` | `~/.claude/CLAUDE.md` to `~/.agents/AGENTS.md`, and `~/.claude/skills` to `~/.agents/skills` |
| Codex | `--codex` | `~/.codex/AGENTS.md` to `~/.agents/AGENTS.md`; Codex reads user skills from `~/.agents/skills` itself |
| Cursor | `--cursor` | Writes `~/.cursor/rules/agents.mdc` as an always-apply rule that tells the agent to read `~/.agents/AGENTS.md`. Cursor reads user skills from `~/.agents/skills` itself. Cursor has no global `AGENTS.md` file, and the rule points to the file instead of copying it, so edits to `AGENTS.md` apply without re-running the installer |

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

The context folder is a plain directory of Markdown files, `~/.agents/context/`, kept out of this repository. You may track it in its own private Git repository. Small tasks remain in the conversation. Repository documentation, issue trackers, and accepted decision records remain authoritative when they already own the information.

### Set up your context folder

The installer copies the empty templates to `~/.agents/context/templates/`. Then:

1. Create the root index and the workspaces folder:

   ```bash
   mkdir -p "$HOME/.agents/context/workspaces"
   cp "$HOME/.agents/context/templates/index.md" "$HOME/.agents/context/index.md"
   ```

2. Start an agent session in a repository. On the first task the agent checks the root index for a workspace that owns the directory. If none does, it asks whether to create and register one, associate the directory with an existing workspace, or continue without one. Answer once; it creates `workspaces/<id>/index.md` from the `workspace.md` template and adds a link to the root index.
3. Durable work then lives under `workspaces/<id>/work/<work-id>/`, using the `work.md` template. `project.md` and `research.md` are used for larger efforts and saved findings.

The agent asks before registering or merging workspaces, and it keeps secrets out of context files.

### Optional pieces

- **Overview board.** You can build an Obsidian Base (a Kanban view over the work notes' properties) for a cross-workspace overview. This repository does not ship one. Without it, agents read the work notes directly. The `obsidian-markdown` and `obsidian-bases` skills help build one; install them separately.
- **Commit guardrails.** Checks for metadata, secrets and writing quality on the context repository are your own tooling and are not included.

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
