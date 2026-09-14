# agent-stuff

Personal agent instructions, reusable skills, and a local context management framework.

## Contents

- `AGENTS.md` contains the global operating rules.
- `skills/` contains workflows and reference material loaded when a task needs them.
- `context/templates/` contains empty templates for private local work records.
- `scripts/validate-skills.py` checks skill metadata and local references.

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
