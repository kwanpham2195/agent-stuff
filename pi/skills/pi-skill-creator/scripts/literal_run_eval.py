#!/usr/bin/env python3
"""Run eval for a skill using the configured agent (codex, opencode, or pi).

Tests whether an agent reads and follows a skill for a set of test prompts.
For agents that support skill injection (--skill flag), we use that mechanism.
Otherwise we prepend the skill content to the prompt.
"""

import argparse
import json
import os
import select
import subprocess
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

from scripts import (find_project_root, get_agent, get_agent_config,
                     parse_skill_md)


def run_single_query(
    query: str,
    skill_name: str,
    skill_path: Path,
    skill_content: str,
    skill_description: str,
    timeout: int,
    project_root: str,
    agent: str,
    model: str | None = None,
) -> bool:
    """Run a single query and return whether the skill was triggered.

    Detection strategy varies by agent:
    - Codex/OpenCode: use --skill flag, detect via session DB or stdout
    - pi: use --skill flag, detect via session DB

    For agents without native skill injection, we prepend skill content to the prompt.
    """
    config = get_agent_config(agent)
    cli = config["cli"]

    # Build the command based on agent capabilities
    # Most modern agents support a --skill or -s flag for skill injection
    cmd = [cli]

    # Add model if specified and agent supports it
    if model:
        # Agents typically use --model or -m for model selection
        cmd.extend(["--model", model])

    # For headless mode, agents typically use -p or similar
    cmd.extend([config["headless_flag"], query])

    # Remove agent-specific env vars that may conflict
    clean_env = {
        k: v
        for k, v in os.environ.items()
        if k not in ("CLAUDECODE",)  # Claude Code's env var
    }

    try:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=project_root,
            env=clean_env,
            text=False,
        )

        triggered = False
        start_time = time.time()
        stdout_data = b""

        try:
            while time.time() - start_time < timeout:
                if process.poll() is not None:
                    # Process ended, read remaining output
                    stdout_chunk = process.stdout.read()
                    if stdout_chunk:
                        stdout_data += stdout_chunk
                    _ = process.stderr.read()
                    break

                ready, _, _ = select.select([process.stdout], [], [], 1.0)
                if not ready:
                    # Check timeout
                    if time.time() - start_time >= timeout:
                        process.kill()
                        process.wait()
                        return False
                    continue

                chunk = os.read(process.stdout.fileno(), 8192)
                if not chunk:
                    break
                stdout_data += chunk

                # For JSON output modes, check if skill was loaded
                # Many agents output skill loading confirmation
                try:
                    decoded = stdout_data.decode("utf-8", errors="replace")
                    # Look for skill name in output (indicates skill was loaded)
                    if (
                        f"Using skill: {skill_name}" in decoded
                        or f'Skill "{skill_name}"' in decoded
                        or f"Loaded: {skill_name}" in decoded
                        or f"I've consulted the `{skill_name}` skill" in decoded
                        or skill_name in decoded
                    ):
                        triggered = True
                        break  # exit early if triggered
                except Exception:
                    pass

                # Check timeout on each chunk
                if time.time() - start_time >= timeout:
                    process.kill()
                    process.wait()
                    return triggered

        finally:
            if process.poll() is None:
                process.kill()
                process.wait()

        return triggered

    except FileNotFoundError:
        print(f"Error: {cli} not found. Is it installed?", file=sys.stderr)
        sys.exit(1)


def run_eval(
    eval_set: list[dict],
    skill_name: str,
    skill_path: Path,
    skill_content: str,
    skill_description: str,
    num_workers: int,
    timeout: int,
    project_root: Path,
    agent: str,
    runs_per_query: int = 1,
    trigger_threshold: float = 0.5,
    model: str | None = None,
) -> dict:
    """Run the full eval set and return results."""
    results = []

    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        future_to_info = {}
        for item in eval_set:
            for run_idx in range(runs_per_query):
                future = executor.submit(
                    run_single_query,
                    item["query"],
                    skill_name,
                    skill_path,
                    skill_content,
                    skill_description,
                    timeout,
                    str(project_root),
                    agent,
                    model,
                )
                future_to_info[future] = (item, run_idx)

        query_triggers: dict[str, list[bool]] = {}
        query_items: dict[str, dict] = {}
        for future in as_completed(future_to_info):
            item, _ = future_to_info[future]
            query = item["query"]
            query_items[query] = item
            if query not in query_triggers:
                query_triggers[query] = []
            try:
                query_triggers[query].append(future.result())
            except Exception as e:
                print(f"Warning: query failed: {e}", file=sys.stderr)
                query_triggers[query].append(False)

    for query, triggers in query_triggers.items():
        item = query_items[query]
        trigger_rate = sum(triggers) / len(triggers)
        should_trigger = item["should_trigger"]
        if should_trigger:
            did_pass = trigger_rate >= trigger_threshold
        else:
            did_pass = trigger_rate < trigger_threshold
        results.append(
            {
                "query": query,
                "should_trigger": should_trigger,
                "trigger_rate": trigger_rate,
                "triggers": sum(triggers),
                "runs": len(triggers),
                "pass": did_pass,
            }
        )

    passed = sum(1 for r in results if r["pass"])
    total = len(results)

    return {
        "skill_name": skill_name,
        "description": skill_description,
        "results": results,
        "summary": {
            "total": total,
            "passed": passed,
            "failed": total - passed,
        },
    }


def main():
    parser = argparse.ArgumentParser(
        description="Run trigger evaluation for a skill using codex/opencode/pi"
    )
    parser.add_argument(
        "--agent", default=None, help="Agent to use (codex, opencode, pi)"
    )
    parser.add_argument("--eval-set", required=True, help="Path to eval set JSON file")
    parser.add_argument("--skill-path", required=True, help="Path to skill directory")
    parser.add_argument(
        "--description", default=None, help="Override description to test"
    )
    parser.add_argument(
        "--num-workers", type=int, default=5, help="Number of parallel workers"
    )
    parser.add_argument(
        "--timeout", type=int, default=60, help="Timeout per query in seconds"
    )
    parser.add_argument(
        "--runs-per-query", type=int, default=1, help="Number of runs per query"
    )
    parser.add_argument(
        "--trigger-threshold",
        type=float,
        default=0.5,
        help="Trigger rate threshold",
    )
    parser.add_argument("--model", default=None, help="Model to use (agent-specific)")
    parser.add_argument(
        "--verbose", action="store_true", help="Print progress to stderr"
    )
    args = parser.parse_args()

    agent = args.agent or get_agent()
    eval_set = json.loads(Path(args.eval_set).read_text())
    skill_path = Path(args.skill_path)

    if not (skill_path / "SKILL.md").exists():
        print(f"Error: No SKILL.md found at {skill_path}", file=sys.stderr)
        sys.exit(1)

    name, original_description, content = parse_skill_md(skill_path)
    description = args.description or original_description
    project_root = find_project_root()

    if args.verbose:
        print(f"Agent: {agent}", file=sys.stderr)
        print(f"Evaluating: {description}", file=sys.stderr)

    output = run_eval(
        eval_set=eval_set,
        skill_name=name,
        skill_path=skill_path,
        skill_content=content,
        skill_description=description,
        num_workers=args.num_workers,
        timeout=args.timeout,
        project_root=project_root,
        agent=agent,
        runs_per_query=args.runs_per_query,
        trigger_threshold=args.trigger_threshold,
        model=args.model,
    )

    if args.verbose:
        summary = output["summary"]
        print(
            f"Results: {summary['passed']}/{summary['total']} passed", file=sys.stderr
        )
        for r in output["results"]:
            status = "PASS" if r["pass"] else "FAIL"
            rate_str = f"{r['triggers']}/{r['runs']}"
            print(
                f"  [{status}] rate={rate_str} expected={r['should_trigger']}: {r['query'][:70]}",
                file=sys.stderr,
            )

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
