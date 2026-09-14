#!/usr/bin/env python3
"""Improve a skill description based on eval results.

Calls the agent CLI (codex/opencode/pi) as a subprocess to generate
an improved description based on what failed in the eval results.
"""

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

from scripts import get_agent, parse_skill_md


def _call_agent(prompt: str, agent: str, model: str | None, timeout: int = 300) -> str:
    """Run the agent CLI with the prompt and return the text response."""
    from scripts import get_agent_config

    config = get_agent_config(agent)
    cli = config["cli"]

    cmd = [cli]
    if model:
        cmd.extend(["--model", model])
    cmd.extend([config["headless_flag"], prompt])

    # Remove conflicting env vars
    clean_env = {k: v for k, v in os.environ.items() if k not in ("CLAUDECODE",)}

    result = subprocess.run(
        cmd,
        input=prompt,
        capture_output=True,
        text=True,
        env=clean_env,
        timeout=timeout,
    )
    if result.returncode != 0:
        raise RuntimeError(f"{cli} exited {result.returncode}\nstderr: {result.stderr}")
    return result.stdout


def improve_description(
    skill_name: str,
    skill_content: str,
    current_description: str,
    eval_results: dict,
    history: list[dict],
    agent: str,
    model: str | None = None,
    iteration: int | None = None,
    log_dir: Path | None = None,
) -> str:
    """Call the agent to improve the description based on eval results."""
    failed_triggers = [
        r
        for r in eval_results.get("results", [])
        if r.get("should_trigger") and not r.get("pass")
    ]
    false_triggers = [
        r
        for r in eval_results.get("results", [])
        if not r.get("should_trigger") and not r.get("pass")
    ]

    train_score = "{}/{}".format(
        eval_results.get("summary", {}).get("passed", 0),
        eval_results.get("summary", {}).get("total", 0),
    )

    prompt = f"""You are optimizing a skill description for a {agent} coding agent skill called "{skill_name}".

A "skill" is a reusable prompt template with progressive disclosure — there's a title and description that determines when the agent uses the skill, and if it does, it reads the full .md instructions which include details, examples, and references to helper scripts.

The description appears in the agent's available_skills list. When a user sends a query, the agent decides whether to use the skill based on the description. Your goal: write a description that triggers for relevant queries, and does NOT trigger for irrelevant ones.

Current description:
"{current_description}"

Current score: {train_score}
"""

    if failed_triggers:
        prompt += "\nFAILED TO TRIGGER (should have triggered but didn't):\n"
        for r in failed_triggers:
            prompt += f'  - "{r["query"]}" (triggered {r.get("triggers", 0)}/{r.get("runs", 0)} times)\n'
        prompt += "\n"

    if false_triggers:
        prompt += "FALSE TRIGGERS (triggered but shouldn't have):\n"
        for r in false_triggers:
            prompt += f'  - "{r["query"]}" (triggered {r.get("triggers", 0)}/{r.get("runs", 0)} times)\n'
        prompt += "\n"

    if history:
        prompt += "PREVIOUS ATTEMPTS (do NOT repeat these — try something structurally different):\n\n"
        for h in history:
            prev_score = "{}/{}".format(
                h.get("passed", h.get("train_passed", 0)),
                h.get("total", h.get("train_total", 0)),
            )
            prompt += f"<attempt train={prev_score}>\n"
            prompt += f'Description: "{h["description"]}"\n'
            if "results" in h:
                prompt += "Results:\n"
                for r in h["results"]:
                    status = "PASS" if r.get("pass") else "FAIL"
                    prompt += f'  [{status}] "{r["query"][:80]}" ({r.get("triggers", 0)}/{r.get("runs", 0)})\n'
            prompt += "</attempt>\n\n"

    prompt += f"""Skill content (for context on what the skill does):
<skill_content>
{skill_content[:2000]}
</skill_content>

Based on the failures, write a new and improved description. Generalize from specific failures to broader categories of user intent — don't just list the failing queries. Keep the description under 200 words / 1024 characters.

Tips:
- Use imperative: "Use this skill for..." not "This skill does..."
- Focus on user intent, not implementation details
- Make it distinctive — the description competes with other skills for attention
- If previous attempts failed, try a different sentence structure or wording

Respond with only the new description in <new_description> tags, nothing else."""

    text = _call_agent(prompt, agent, model)

    match = re.search(r"<new_description>(.*?)</new_description>", text, re.DOTALL)
    description = (
        match.group(1).strip().strip('"').strip("'")
        if match
        else text.strip().strip('"').strip("'")
    )

    # Safety: truncate if over 1024 chars
    if len(description) > 1024:
        description = description[:1021] + "..."

    transcript = {
        "iteration": iteration,
        "prompt": prompt,
        "response": text,
        "parsed_description": description,
        "char_count": len(description),
        "final_description": description,
    }

    if log_dir:
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = log_dir / f"improve_iter_{iteration or 'unknown'}.json"
        log_file.write_text(json.dumps(transcript, indent=2))

    return description


def main():
    parser = argparse.ArgumentParser(
        description="Improve a skill description based on eval results"
    )
    parser.add_argument("--agent", default=None, help="Agent (codex, opencode, pi)")
    parser.add_argument(
        "--eval-results", required=True, help="Path to eval results JSON"
    )
    parser.add_argument("--skill-path", required=True, help="Path to skill directory")
    parser.add_argument("--history", default=None, help="Path to history JSON")
    parser.add_argument("--model", default=None, help="Model to use")
    parser.add_argument("--verbose", action="store_true", help="Print progress")
    args = parser.parse_args()

    agent = args.agent or get_agent()
    skill_path = Path(args.skill_path)

    if not (skill_path / "SKILL.md").exists():
        print(f"Error: No SKILL.md found at {skill_path}", file=sys.stderr)
        sys.exit(1)

    eval_results = json.loads(Path(args.eval_results).read_text())
    history = []
    if args.history:
        history = json.loads(Path(args.history).read_text())

    name, _, content = parse_skill_md(skill_path)
    current_description = eval_results.get("description", "")

    if args.verbose:
        print(f"Agent: {agent}", file=sys.stderr)
        print(f"Current: {current_description[:100]}...", file=sys.stderr)
        print(
            f"Score: {eval_results['summary']['passed']}/{eval_results['summary']['total']}",
            file=sys.stderr,
        )

    new_description = improve_description(
        skill_name=name,
        skill_content=content,
        current_description=current_description,
        eval_results=eval_results,
        history=history,
        agent=agent,
        model=args.model,
    )

    if args.verbose:
        print(f"Improved: {new_description[:100]}...", file=sys.stderr)

    print(
        json.dumps(
            {
                "description": new_description,
                "history": history
                + [
                    {
                        "description": current_description,
                        "passed": eval_results["summary"]["passed"],
                        "failed": eval_results["summary"]["failed"],
                        "total": eval_results["summary"]["total"],
                        "results": eval_results.get("results", []),
                    }
                ],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
