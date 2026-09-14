# Pi Skill Creator

Create, test, and improve Agent Skills for pi and opencode.

This skill helps you draft a skill, run test prompts against it, review the outputs in an HTML viewer, and iteratively improve the skill instructions.

## Setup Instructions

This skill is a self-contained Python project with no external dependencies.

1. Ensure you have Python 3.10+ installed.
2. Clone or copy this skill to your agents directory:

```bash
# For pi
cp -r pi-skill-creator ~/.pi/agent/skills/

# For opencode
cp -r pi-skill-creator ~/.agents/skills/
```

3. Run any script directly with Python:

```bash
python -m scripts.run_eval --skill-path /path/to/skill ...
```

## Usage

To use this skill, ask the agent to create a new skill or improve an existing one. For example:
- "Create a new skill for generating release notes"
- "Improve the triggering description for the doc-coauthoring skill"
- "Run evals for my new skill"
