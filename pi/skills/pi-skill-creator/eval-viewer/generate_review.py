#!/usr/bin/env python3
"""Generate an HTML report from benchmark results.

Usage:
    python generate_review.py /workspace/iteration-1 --skill-name my-skill
    python generate_review.py /workspace/iteration-1 --static /tmp/report.html
"""

import argparse
import html
import json
import sys
from pathlib import Path


def generate_html(benchmark_data: dict, skill_name: str = "") -> str:
    """Generate HTML report from benchmark data."""
    runs = benchmark_data.get("runs", [])
    run_summary = benchmark_data.get("run_summary", {})

    title_prefix = html.escape(skill_name + " — ") if skill_name else ""

    # Group runs by configuration
    configs = {}
    for run in runs:
        cfg = run.get("configuration", "unknown")
        if cfg not in configs:
            configs[cfg] = []
        configs[cfg].append(run)

    # Build HTML
    html_parts = [
        """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>"""
        + title_prefix
        + """Skill Eval Review</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: #fafafa;
            color: #1a1a1a;
        }
        h1 { color: #1a1a1a; border-bottom: 2px solid #1a1a1a; padding-bottom: 8px; }
        .summary {
            background: white;
            padding: 16px;
            border-radius: 8px;
            margin-bottom: 20px;
            border: 1px solid #e0e0e0;
        }
        .summary h2 { margin-top: 0; }
        .metric { display: flex; gap: 24px; margin: 8px 0; }
        .metric-label { font-weight: 600; min-width: 120px; }
        .metric-value { color: #555; }
        table {
            width: 100%;
            border-collapse: collapse;
            background: white;
            border-radius: 8px;
            overflow: hidden;
            border: 1px solid #e0e0e0;
        }
        th {
            background: #1a1a1a;
            color: white;
            padding: 12px 16px;
            text-align: left;
            font-weight: 500;
        }
        td {
            padding: 10px 16px;
            border-bottom: 1px solid #f0f0f0;
        }
        tr:last-child td { border-bottom: none; }
        tr:hover { background: #fafafa; }
        .pass { color: #22c55e; font-weight: 600; }
        .fail { color: #ef4444; font-weight: 600; }
        .config-header {
            background: #f5f5f5;
            font-weight: 600;
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .feedback-section {
            margin-top: 24px;
            background: white;
            padding: 16px;
            border-radius: 8px;
            border: 1px solid #e0e0e0;
        }
        .feedback-section h2 { margin-top: 0; }
        textarea {
            width: 100%;
            min-height: 80px;
            padding: 8px;
            border: 1px solid #e0e0e0;
            border-radius: 4px;
            font-family: inherit;
            font-size: 14px;
        }
        .run-id { font-family: monospace; font-size: 12px; color: #888; }
        .delta { color: #666; font-size: 13px; }
        .delta-positive { color: #22c55e; }
        .delta-negative { color: #ef4444; }
    </style>
</head>
<body>
    <h1>"""
        + title_prefix
        + """Skill Eval Review</h1>
    <div class="summary">
        <h2>Summary</h2>
"""
    ]

    # Summary metrics
    for cfg_name, cfg_data in run_summary.items():
        if cfg_name == "delta":
            delta = cfg_data
            delta_pr = delta.get("pass_rate", "—")
            delta_time = delta.get("time_seconds", "—")
            delta_class_pr = (
                "delta-positive"
                if str(delta_pr).startswith("+")
                else "delta-negative" if str(delta_pr).startswith("-") else ""
            )
            delta_class_time = (
                "delta-positive"
                if str(delta_time).startswith("+")
                else "delta-negative" if str(delta_time).startswith("-") else ""
            )
            html_parts.append(f"""
        <div class="metric">
            <span class="metric-label">Delta (with - without):</span>
            <span class="metric-value">
                Pass Rate: <span class="{delta_class_pr}">{delta_pr}</span> |
                Time: <span class="{delta_class_time}">{delta_time}s</span>
            </span>
        </div>
""")
        else:
            pr = cfg_data.get("pass_rate", {})
            time_s = cfg_data.get("time_seconds", {})
            pr_mean = pr.get("mean", 0) * 100
            pr_std = pr.get("stddev", 0) * 100
            time_mean = time_s.get("mean", 0)
            time_std = time_s.get("stddev", 0)
            html_parts.append(f"""
        <div class="metric">
            <span class="metric-label">{cfg_name.replace("_", " ").title()}:</span>
            <span class="metric-value">
                Pass Rate: {pr_mean:.0f}% ± {pr_std:.0f}% |
                Time: {time_mean:.1f}s ± {time_std:.1f}s
            </span>
        </div>
""")

    html_parts.append("""
    </div>
""")

    # Run details table
    html_parts.append("""
    <table>
        <thead>
            <tr>
                <th>Configuration</th>
                <th>Run</th>
                <th>Pass Rate</th>
                <th>Passed</th>
                <th>Failed</th>
                <th>Time (s)</th>
                <th>Tokens</th>
            </tr>
        </thead>
        <tbody>
""")

    for cfg_name in sorted(configs.keys()):
        cfg_runs = configs[cfg_name]
        for run in sorted(cfg_runs, key=lambda r: r.get("run_number", 0)):
            result = run.get("result", {})
            pass_rate = result.get("pass_rate", 0) * 100
            passed = result.get("passed", 0)
            failed = result.get("failed", 0)
            time_s = result.get("time_seconds", 0)
            tokens = result.get("tokens", 0)
            run_num = run.get("run_number", "?")
            pr_class = "pass" if pass_rate >= 80 else "fail" if pass_rate < 50 else ""
            html_parts.append(f"""
            <tr>
                <td>{html.escape(str(cfg_name))}</td>
                <td class="run-id">run-{run_num}</td>
                <td class="{pr_class}">{pass_rate:.0f}%</td>
                <td class="pass">{passed}</td>
                <td class="fail">{failed}</td>
                <td>{time_s:.1f}</td>
                <td>{tokens}</td>
            </tr>
""")

    html_parts.append("""
        </tbody>
    </table>
""")

    # Individual expectation details
    if runs and runs[0].get("expectations"):
        html_parts.append("""
    <div class="feedback-section">
        <h2>Expectation Details</h2>
""")
        # Show expectations across all runs
        expectations_seen = {}
        for run in runs:
            for exp in run.get("expectations", []):
                exp_text = exp.get("text", "?")
                if exp_text not in expectations_seen:
                    expectations_seen[exp_text] = []
                expectations_seen[exp_text].append(exp.get("passed", False))

        for exp_text, results in expectations_seen.items():
            passed_count = sum(1 for p in results if p)
            total = len(results)
            pass_class = (
                "pass" if passed_count == total else "fail" if passed_count == 0 else ""
            )
            html_parts.append(f"""
        <div style="margin-bottom: 12px; padding: 8px; background: #f9f9f9; border-radius: 4px;">
            <span class="{pass_class}">{passed_count}/{total} passed</span>
            — {html.escape(exp_text[:100])}
        </div>
""")

        html_parts.append("""
    </div>
""")

    html_parts.append("""
</body>
</html>
""")

    return "".join(html_parts)


def main():
    parser = argparse.ArgumentParser(
        description="Generate HTML eval review from benchmark data"
    )
    parser.add_argument("workspace", help="Path to the workspace/iteration directory")
    parser.add_argument("--skill-name", default="", help="Skill name for the title")
    parser.add_argument(
        "--benchmark",
        help="Path to benchmark.json (default: <workspace>/benchmark.json)",
    )
    parser.add_argument(
        "--static", dest="static_file", help="Write to file instead of starting server"
    )
    args = parser.parse_args()

    workspace = Path(args.workspace)
    benchmark_path = (
        Path(args.benchmark) if args.benchmark else (workspace / "benchmark.json")
    )

    if not benchmark_path.exists():
        print(f"Error: benchmark.json not found at {benchmark_path}", file=sys.stderr)
        sys.exit(1)

    with open(benchmark_path) as f:
        benchmark_data = json.load(f)

    html = generate_html(benchmark_data, skill_name=args.skill_name)

    if args.static_file:
        Path(args.static_file).write_text(html)
        print(f"Report written to {args.static_file}")
    else:
        print(html)


if __name__ == "__main__":
    main()
