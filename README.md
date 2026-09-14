# agent-stuff

Personal agent instructions, reusable skills, and a local context management framework.

## Contents

- `AGENTS.md` contains the global operating rules.
- `skills/` contains workflows and reference material loaded when a task needs them.
- `context/templates/` contains empty templates for private local work records.
- `scripts/validate-skills.py` checks skill metadata and local references.

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

## Optional tools

Some skills describe workflows for tools such as chezmoi, GitHub CLI, OrbStack, Obsidian, and browser or terminal helpers. Install and configure only the tools you use. Externally managed skills named in `AGENTS.md` are not bundled here.

## License

MIT. See [LICENSE](LICENSE).
