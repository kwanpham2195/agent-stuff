---
name: pi-skill-creator
description: Create, test, and improve Agent Skills for pi and opencode. Use when users want to create a new skill from scratch, edit or improve an existing skill, run evals to test a skill, or optimize a skill's description for better triggering accuracy. Triggers for any skill creation or evaluation task targeting pi, opencode, or codex.
---

# Pi Skill Creator

Create and iteratively improve skills for coding agent harnesses like **pi**, **opencode**, and **codex**.

The core loop: draft a skill → run test prompts → review outputs → improve → repeat.

## Workflow Overview

1. **Capture intent** — what should the skill do, when should it trigger
2. **Write SKILL.md** — name, description, instructions, examples
3. **Create test prompts** — 2-3 realistic user queries per skill
4. **Run evals** — spawn subagents with/without skill, compare outputs
5. **Review** — HTML viewer shows outputs + quantitative benchmark
6. **Improve** — rewrite based on feedback, repeat until satisfied
7. **Package** — bundle as `.skill` file for distribution

---

## Creating a Skill

### Step 1: Capture Intent

Ask the user:
1. What should this skill enable the agent to do?
2. When should it trigger? (what phrases/contexts)
3. Expected output format?
4. Test cases needed? (skills with verifiable outputs benefit most)

### Step 2: Write SKILL.md

```
skill-name/
├── SKILL.md          ← required
├── scripts/          ← optional helper scripts
├── references/       ← optional docs loaded on demand
└── assets/           ← optional templates, icons
```

**SKILL.md anatomy:**

```yaml
---
name: skill-name
description: When to trigger + what it does. Be "pushy" — overtrigger rather than undertrigger.
---

# Skill Name

## What this skill does

## When to use it

## How to use it

## Examples
```

**Description writing tips:**
- Use imperative: "Use this skill for..." not "This skill does..."
- Focus on user intent, not implementation
- Be distinctive — the description competes with other skills for the agent's attention
- Keep under 200 words / 1024 chars

### Step 3: Create Test Prompts

Save to `evals/evals.json`:

```json
{
  "skill_name": "my-skill",
  "evals": [
    {
      "id": 1,
      "prompt": "Realistic user query",
      "expected_output": "What the skill should produce",
      "files": []
    }
  ]
}
```

## Running and Evaluating

### Run all evals

```bash
python -m scripts.run_eval \
  --agent pi \
  --skill-path /path/to/skill \
  --workspace /tmp/skill-workspace \
  --evals evals/evals.json
```

This spawns subagents for each eval in parallel — one **with skill**, one **without** (baseline).

### Spawn subagents directly

Use `delegate_task` (if using the `pi-subagents` skill) or the pi CLI in each subagent:

**With-skill:**
```bash
cd /project && pi -p "task..." --skill my-skill
```

**Baseline (no skill):**
```bash
cd /project && pi -p "task..."
```

### Grading

```bash
python -m scripts.aggregate_benchmark /workspace/iteration-1 \
  --agent pi \
  --skill-name my-skill
```

### Review in browser

```bash
python eval-viewer/generate_review.py /workspace/iteration-1 \
  --skill-name my-skill \
  --benchmark /workspace/iteration-1/benchmark.json
```

---

## Directory Structure

```
<skill-workspace>/
└── iteration-1/
    ├── eval-1/
    │   ├── with_skill/
    │   │   ├── outputs/        ← what the agent produced
    │   │   ├── transcript.md   ← execution log
    │   │   ├── grading.json    ← pass/fail per assertion
    │   │   └── timing.json     ← duration + tokens
    │   └── without_skill/
    │       └── ...
    ├── skill-snapshot/          ← copy of skill at this iteration
    ├── benchmark.json           ← aggregate stats
    ├── benchmark.md             ← human-readable summary
    └── feedback.json            ← user review comments
```

---

## Improving Skills

After reviewing feedback:

1. Edit the skill based on what didn't work
2. Re-run evals into a new `iteration-2/` directory
3. Re-launch the reviewer with `--previous-workspace iteration-1`
4. Repeat until satisfied

**Generalization principle:** Don't overfit to specific test prompts. If feedback says "the output was wrong for case X", ask *why* — then fix the underlying instruction, not just the specific case.

---

## Description Optimization

Optimize the `description` field in SKILL.md frontmatter for better triggering accuracy.

### Step 1: Generate eval set

Create 20 queries — mix of should-trigger and should-not-trigger:

```json
[
  {"query": "specific realistic user prompt", "should_trigger": true},
  {"query": "adjacent but different task", "should_trigger": false}
]
```

**Good should-trigger queries:** Concrete, with file paths, context, personal details.
**Good should-not-trigger queries:** Near-misses sharing keywords but needing something different.

### Step 2: Run optimization loop

```bash
python -m scripts.run_loop \
  --agent pi \ # or opencode
  --eval-set trigger_evals.json \
  --skill-path /path/to/skill \
  --model gpt-4o \
  --max-iterations 5
```

Writes HTML report showing which description version scored best.

### Step 3: Apply result

Update `description` in SKILL.md with the best-scoring version.

---

## Packaging

```bash
python -m scripts.package_skill /path/to/skill [--output-dir ./dist]
```

Creates `skill-name.skill` — a zip bundle ready for distribution.

---

## Agent-Specific Notes

### pi
- Project root: `AGENTS.md` or `.pi/` directory
- Skills: Pass `--skill /path/to/skill` to inject a skill, or add it to `~/.pi/agent/skills/` or `~/.agents/skills/`
- Sessions: Managed via interactive mode or the `pi-interactive-shell` skill
- Subagents: Managed via the `pi-subagents` skill (use `/skill:pi-subagents delegate`)

---

## Reference Files

- `agents/grader.md` — evaluate assertions against outputs
- `agents/comparator.md` — blind A/B comparison between two outputs
- `agents/analyzer.md` — analyze benchmark results for patterns
- `references/schemas.md` — JSON schemas for evals.json, grading.json, etc.
