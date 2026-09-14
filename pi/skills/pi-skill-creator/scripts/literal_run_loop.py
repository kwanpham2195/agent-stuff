#!/usr/bin/env python3
"""Run the eval + improve loop until all pass or max iterations reached.

Combines run_eval.py and improve_description.py to iteratively optimize
a skill's description for better triggering accuracy.

Usage:
    python -m scripts.run_loop \
        --agent opencode \
        --eval-set trigger_evals.json \
        --skill-path /path/to/skill \
        --model gpt-4o \
        --max-iterations 5
"""

import argparse
import json
import random
import sys
import time
from pathlib import Path

from scripts import get_agent, parse_skill_md
from scripts.improve_description import improve_description
from scripts.run_eval import run_eval


def split_eval_set(
    eval_set: list[dict], holdout: float, seed: int = 42
) -> tuple[list[dict], list[dict]]:
    """Split eval set into train and test sets, stratified by should_trigger."""
    random.seed(seed)

    trigger = [e for e in eval_set if e["should_trigger"]]
    no_trigger = [e for e in eval_set if not e["should_trigger"]]

    random.shuffle(trigger)
    random.shuffle(no_trigger)

    n_trigger_test = max(1, int(len(trigger) * holdout))
    n_no_trigger_test = max(1, int(len(no_trigger) * holdout))

    test_set = trigger[:n_trigger_test] + no_trigger[:n_no_trigger_test]
    train_set = trigger[n_trigger_test:] + no_trigger[n_no_trigger_test:]

    return train_set, test_set


def run_loop(
    eval_set: list[dict],
    skill_path: Path,
    skill_name: str,
    skill_content: str,
    current_description: str,
    agent: str,
    model: str,
    num_workers: int,
    timeout: int,
    max_iterations: int,
    holdout: float,
    verbose: bool,
    results_dir: Path | None = None,
) -> dict:
    """Run the eval + improvement loop."""
    from scripts import find_project_root

    project_root = find_project_root()

    # Split into train/test if holdout > 0
    if holdout > 0:
        train_set, test_set = split_eval_set(eval_set, holdout)
        if verbose:
            print(
                f"Split: {len(train_set)} train, {len(test_set)} test (holdout={holdout})",
                file=sys.stderr,
            )
    else:
        train_set = eval_set
        test_set = []

    history = []
    current_desc = current_description

    for iteration in range(1, max_iterations + 1):
        if verbose:
            print(f"\n{'=' * 60}", file=sys.stderr)
            print(f"Iteration {iteration}/{max_iterations}", file=sys.stderr)
            print(f"Description: {current_desc[:80]}...", file=sys.stderr)
            print(f"{'=' * 60}", file=sys.stderr)

        # Evaluate train + test together
        all_queries = train_set + test_set
        t0 = time.time()
        all_results = run_eval(
            eval_set=all_queries,
            skill_name=skill_name,
            skill_path=skill_path,
            skill_content=skill_content,
            skill_description=current_desc,
            num_workers=num_workers,
            timeout=timeout,
            project_root=project_root,
            agent=agent,
            runs_per_query=1,
            trigger_threshold=0.5,
            model=model,
        )
        eval_elapsed = time.time() - t0

        # Split results back into train/test
        train_queries_set = {q["query"] for q in train_set}
        train_results = [
            r for r in all_results["results"] if r["query"] in train_queries_set
        ]
        test_results = [
            r for r in all_results["results"] if r["query"] not in train_queries_set
        ]

        train_passed = sum(1 for r in train_results if r["pass"])
        train_total = len(train_results)
        train_summary = {
            "passed": train_passed,
            "failed": train_total - train_passed,
            "total": train_total,
        }

        if test_set:
            test_passed = sum(1 for r in test_results if r["pass"])
            test_total = len(test_results)
            test_summary = {
                "passed": test_passed,
                "failed": test_total - test_passed,
                "total": test_total,
            }
        else:
            test_summary = None

        history.append(
            {
                "iteration": iteration,
                "description": current_desc,
                "train_passed": train_passed,
                "train_failed": train_total - train_passed,
                "train_total": train_total,
                "train_results": train_results,
                "test_passed": test_summary["passed"] if test_summary else None,
                "test_total": test_summary["total"] if test_summary else None,
                "test_results": test_results if test_set else None,
                "passed": train_passed,
                "failed": train_total - train_passed,
                "total": train_total,
                "results": train_results,
            }
        )

        if verbose:

            def print_stats(label, results, elapsed):
                total = len(results)
                correct = sum(1 for r in results if r["pass"])
                print(
                    f"{label}: {correct}/{total} correct ({elapsed:.1f}s)",
                    file=sys.stderr,
                )
                for r in results:
                    status = "PASS" if r["pass"] else "FAIL"
                    print(f"  [{status}] {r['query'][:60]}", file=sys.stderr)

            print_stats("Train", train_results, eval_elapsed)
            if test_summary:
                print_stats("Test ", test_results, 0)

        # Check exit condition
        if train_total > 0 and train_passed == train_total:
            if verbose:
                print(
                    f"\nAll train queries passed on iteration {iteration}!",
                    file=sys.stderr,
                )
            break

        if iteration == max_iterations:
            if verbose:
                print(f"\nMax iterations reached ({max_iterations}).", file=sys.stderr)
            break

        # Improve description
        if verbose:
            print("\nImproving description...", file=sys.stderr)

        t0 = time.time()
        # Blind the improvement to test results
        blinded_history = [
            {k: v for k, v in h.items() if not k.startswith("test_")} for h in history
        ]
        new_desc = improve_description(
            skill_name=skill_name,
            skill_content=skill_content,
            current_description=current_desc,
            eval_results={"results": train_results, "summary": train_summary},
            history=blinded_history,
            agent=agent,
            model=model,
            iteration=iteration,
        )
        improve_elapsed = time.time() - t0

        if verbose:
            print(
                f"Proposed ({improve_elapsed:.1f}s): {new_desc[:80]}...",
                file=sys.stderr,
            )

        current_desc = new_desc

    # Find best by test score (or train if no test)
    if test_set:
        best = max(history, key=lambda h: h.get("test_passed") or 0)
        best_score = f"{best['test_passed']}/{best['test_total']}"
    else:
        best = max(history, key=lambda h: h["train_passed"])
        best_score = f"{best['train_passed']}/{best['train_total']}"

    return {
        "original_description": current_description,
        "best_description": best["description"],
        "best_score": best_score,
        "final_description": current_desc,
        "iterations_run": len(history),
        "train_size": len(train_set),
        "test_size": len(test_set) if test_set else 0,
        "history": history,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Run eval + improve loop for description optimization"
    )
    parser.add_argument("--agent", default=None, help="Agent (codex, opencode, pi)")
    parser.add_argument("--eval-set", required=True, help="Path to eval set JSON file")
    parser.add_argument("--skill-path", required=True, help="Path to skill directory")
    parser.add_argument(
        "--description", default=None, help="Override starting description"
    )
    parser.add_argument(
        "--num-workers", type=int, default=5, help="Number of parallel workers"
    )
    parser.add_argument(
        "--timeout", type=int, default=60, help="Timeout per query in seconds"
    )
    parser.add_argument(
        "--max-iterations", type=int, default=5, help="Max improvement iterations"
    )
    parser.add_argument(
        "--holdout",
        type=float,
        default=0.4,
        help="Fraction to hold out for test (0 to disable)",
    )
    parser.add_argument("--model", required=True, help="Model to use for improvement")
    parser.add_argument("--verbose", action="store_true", help="Print progress")
    parser.add_argument(
        "--results-dir",
        default=None,
        help="Save all outputs to a timestamped subdirectory",
    )
    args = parser.parse_args()

    eval_set = json.loads(Path(args.eval_set).read_text())
    skill_path = Path(args.skill_path)

    if not (skill_path / "SKILL.md").exists():
        print(f"Error: No SKILL.md found at {skill_path}", file=sys.stderr)
        sys.exit(1)

    skill_name, original_description, skill_content = parse_skill_md(skill_path)
    agent = args.agent or get_agent()
    current_desc = args.description or original_description

    results_dir = None
    if args.results_dir:
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        results_dir = Path(args.results_dir) / timestamp
        results_dir.mkdir(parents=True, exist_ok=True)

    output = run_loop(
        eval_set=eval_set,
        skill_path=skill_path,
        skill_name=skill_name,
        skill_content=skill_content,
        current_description=current_desc,
        agent=agent,
        model=args.model,
        num_workers=args.num_workers,
        timeout=args.timeout,
        max_iterations=args.max_iterations,
        holdout=args.holdout,
        verbose=args.verbose,
        results_dir=results_dir,
    )

    print(json.dumps(output, indent=2))

    if results_dir:
        (results_dir / "results.json").write_text(json.dumps(output, indent=2))
        print(f"Results saved to: {results_dir}", file=sys.stderr)


if __name__ == "__main__":
    main()
