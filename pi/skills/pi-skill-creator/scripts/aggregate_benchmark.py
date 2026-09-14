#!/usr/bin/env python3
"""
Aggregate individual run results into benchmark summary statistics.

Usage:
    python aggregate_benchmark.py <benchmark_dir> --agent opencode --skill-name my-skill

Reads grading.json files from run directories and produces:
- run_summary with mean, stddev, min, max for each metric
- delta between with_skill and without_skill configurations
"""

import argparse
import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path


def calculate_stats(values: list[float]) -> dict:
    """Calculate mean, stddev, min, max for a list of values."""
    if not values:
        return {"mean": 0.0, "stddev": 0.0, "min": 0.0, "max": 0.0}

    n = len(values)
    mean = sum(values) / n

    if n > 1:
        variance = sum((x - mean) ** 2 for x in values) / (n - 1)
        stddev = math.sqrt(variance)
    else:
        stddev = 0.0

    return {
        "mean": round(mean, 4),
        "stddev": round(stddev, 4),
        "min": round(min(values), 4),
        "max": round(max(values), 4),
    }


def load_run_results(benchmark_dir: Path) -> dict:
    """Load all run results from a benchmark directory.

    Expected layout:
    <benchmark_dir>/
    └── eval-N/
        ├── with_skill/
        │   ├── run-1/grading.json
        │   └── run-2/grading.json
        └── without_skill/
            ├── run-1/grading.json
            └── run-2/grading.json
    """
    results: dict[str, list] = {}

    if not benchmark_dir.exists():
        print(f"Directory not found: {benchmark_dir}")
        return {}

    # Find eval-* directories
    eval_dirs = sorted(benchmark_dir.glob("eval-*"))
    if not eval_dirs:
        # Try nested runs/ layout
        runs_dir = benchmark_dir / "runs"
        if runs_dir.exists():
            eval_dirs = sorted(runs_dir.glob("eval-*"))

    for eval_dir in eval_dirs:
        # Find config directories (with_skill, without_skill, etc.)
        for config_dir in sorted(eval_dir.iterdir()):
            if not config_dir.is_dir():
                continue
            config = config_dir.name

            # Find run-* directories
            run_dirs = sorted(config_dir.glob("run-*"))
            if not run_dirs:
                continue

            if config not in results:
                results[config] = []

            for run_dir in run_dirs:
                grading_file = run_dir / "grading.json"
                if not grading_file.exists():
                    continue

                try:
                    with open(grading_file) as f:
                        grading = json.load(f)
                except json.JSONDecodeError as e:
                    print(f"Warning: Invalid JSON in {grading_file}: {e}")
                    continue

                # Extract run number from directory name
                run_number = 1
                try:
                    run_number = int(run_dir.name.split("-")[1])
                except (ValueError, IndexError):
                    pass

                result = {
                    "run_number": run_number,
                    "pass_rate": grading.get("summary", {}).get("pass_rate", 0.0),
                    "passed": grading.get("summary", {}).get("passed", 0),
                    "failed": grading.get("summary", {}).get("failed", 0),
                    "total": grading.get("summary", {}).get("total", 0),
                }

                # Extract timing
                timing = grading.get("timing", {})
                result["time_seconds"] = timing.get("total_duration_seconds", 0.0)
                result["tokens"] = timing.get("total_tokens", 0)

                # Extract expectations
                raw_expectations = grading.get("expectations", [])
                result["expectations"] = raw_expectations

                results[config].append(result)

    return results


def aggregate_results(results: dict) -> dict:
    """Aggregate run results into summary statistics."""
    run_summary = {}
    configs = list(results.keys())

    for config in configs:
        runs = results.get(config, [])

        if not runs:
            run_summary[config] = {
                "pass_rate": {"mean": 0.0, "stddev": 0.0, "min": 0.0, "max": 0.0},
                "time_seconds": {"mean": 0.0, "stddev": 0.0, "min": 0.0, "max": 0.0},
                "tokens": {"mean": 0, "stddev": 0, "min": 0, "max": 0},
            }
            continue

        pass_rates = [r["pass_rate"] for r in runs]
        times = [r["time_seconds"] for r in runs]
        tokens = [r.get("tokens", 0) for r in runs]

        run_summary[config] = {
            "pass_rate": calculate_stats(pass_rates),
            "time_seconds": calculate_stats(times),
            "tokens": calculate_stats(tokens),
        }

    # Calculate delta between first two configs
    if len(configs) >= 2:
        primary = run_summary.get(configs[0], {})
        baseline = run_summary.get(configs[1], {})
    else:
        primary = run_summary.get(configs[0], {}) if configs else {}
        baseline = {}

    delta_pass_rate = primary.get("pass_rate", {}).get("mean", 0) - baseline.get(
        "pass_rate", {}
    ).get("mean", 0)
    delta_time = primary.get("time_seconds", {}).get("mean", 0) - baseline.get(
        "time_seconds", {}
    ).get("mean", 0)
    delta_tokens = primary.get("tokens", {}).get("mean", 0) - baseline.get(
        "tokens", {}
    ).get("mean", 0)

    run_summary["delta"] = {
        "pass_rate": f"{delta_pass_rate:+.2f}",
        "time_seconds": f"{delta_time:+.1f}",
        "tokens": f"{delta_tokens:+.0f}",
    }

    return run_summary


def generate_benchmark(
    benchmark_dir: Path, skill_name: str = "", skill_path: str = ""
) -> dict:
    """Generate complete benchmark.json from run results."""
    results = load_run_results(benchmark_dir)
    run_summary = aggregate_results(results)

    # Build runs array
    runs = []
    for config in results:
        for result in results[config]:
            runs.append(
                {
                    "configuration": config,
                    "run_number": result["run_number"],
                    "result": {
                        "pass_rate": result["pass_rate"],
                        "passed": result["passed"],
                        "failed": result["failed"],
                        "total": result["total"],
                        "time_seconds": result["time_seconds"],
                        "tokens": result.get("tokens", 0),
                    },
                    "expectations": result.get("expectations", []),
                }
            )

    benchmark = {
        "metadata": {
            "skill_name": skill_name or "<skill-name>",
            "skill_path": skill_path or "<path/to/skill>",
            "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "runs": runs,
        },
        "run_summary": run_summary,
        "notes": [],
    }

    return benchmark


def generate_markdown(benchmark: dict) -> str:
    """Generate human-readable benchmark.md from benchmark data."""
    run_summary = benchmark["run_summary"]
    configs = [k for k in run_summary if k != "delta"]

    lines = [
        f"# Skill Benchmark: {benchmark['metadata']['skill_name']}",
        "",
        f"**Date**: {benchmark['metadata']['timestamp']}",
        "",
        "## Summary",
        "",
    ]

    if len(configs) >= 2:
        a_name = configs[0].replace("_", " ").title()
        b_name = configs[1].replace("_", " ").title()
        delta = run_summary.get("delta", {})

        a_pr = run_summary.get(configs[0], {}).get("pass_rate", {})
        b_pr = run_summary.get(configs[1], {}).get("pass_rate", {})
        a_time = run_summary.get(configs[0], {}).get("time_seconds", {})
        b_time = run_summary.get(configs[1], {}).get("time_seconds", {})

        lines.extend(
            [
                f"| Metric | {a_name} | {b_name} | Delta |",
                "|--------|------------|---------------|-------|",
                f"| Pass Rate | {a_pr.get('mean', 0) * 100:.0f}% ± {a_pr.get('stddev', 0) * 100:.0f}% | {b_pr.get('mean', 0) * 100:.0f}% ± {b_pr.get('stddev', 0) * 100:.0f}% | {delta.get('pass_rate', '—')} |",
                f"| Time | {a_time.get('mean', 0):.1f}s ± {a_time.get('stddev', 0):.1f}s | {b_time.get('mean', 0):.1f}s ± {b_time.get('stddev', 0):.1f}s | {delta.get('time_seconds', '—')}s |",
            ]
        )
    else:
        for config in configs:
            cfg = run_summary[config]
            name = config.replace("_", " ").title()
            pr = cfg.get("pass_rate", {})
            lines.append(f"**{name}**: {pr.get('mean', 0) * 100:.0f}% pass rate")

    if benchmark.get("notes"):
        lines.extend(["", "## Notes", ""])
        for note in benchmark["notes"]:
            lines.append(f"- {note}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Aggregate benchmark run results into summary statistics"
    )
    parser.add_argument(
        "benchmark_dir", type=Path, help="Path to the benchmark directory"
    )
    parser.add_argument(
        "--agent", default=None, help="Agent used (codex, opencode, pi)"
    )
    parser.add_argument(
        "--skill-name", default="", help="Name of the skill being benchmarked"
    )
    parser.add_argument(
        "--skill-path", default="", help="Path to the skill being benchmarked"
    )
    parser.add_argument(
        "--output", "-o", type=Path, help="Output path for benchmark.json"
    )

    args = parser.parse_args()

    if not args.benchmark_dir.exists():
        print(f"Directory not found: {args.benchmark_dir}")
        sys.exit(1)

    benchmark = generate_benchmark(args.benchmark_dir, args.skill_name, args.skill_path)

    output_json = args.output or (args.benchmark_dir / "benchmark.json")
    output_md = output_json.with_suffix(".md")

    with open(output_json, "w") as f:
        json.dump(benchmark, f, indent=2)
    print(f"Generated: {output_json}")

    markdown = generate_markdown(benchmark)
    with open(output_md, "w") as f:
        f.write(markdown)
    print(f"Generated: {output_md}")

    # Print summary
    run_summary = benchmark["run_summary"]
    configs = [k for k in run_summary if k != "delta"]
    delta = run_summary.get("delta", {})

    print("\nSummary:")
    for config in configs:
        pr = run_summary[config]["pass_rate"]["mean"]
        label = config.replace("_", " ").title()
        print(f"  {label}: {pr * 100:.1f}% pass rate")
    if delta:
        print(f"  Delta: {delta.get('pass_rate', '—')}")


if __name__ == "__main__":
    main()
