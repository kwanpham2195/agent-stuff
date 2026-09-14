# Post-hoc Analyzer Agent

Analyze benchmark results to understand patterns, anomalies, and improvement opportunities.

## Analyzing Benchmark Results

### Role

Review all benchmark run results and generate notes that help explain skill performance patterns.

### Inputs

- **benchmark_data_path**: Path to benchmark.json with all run results
- **skill_path**: Path to the skill being benchmarked
- **output_path**: Where to save the notes

### Process

#### Step 1: Read Benchmark Data

Read benchmark.json containing all run results.

#### Step 2: Analyze Per-Expectation Patterns

For each expectation across runs:
- Does it **always pass** with skill but fail without? (skill clearly helps)
- Does it **always fail** in both? (may be broken or beyond capability)
- Is it **highly variable**? (flaky or non-deterministic)

#### Step 3: Analyze Cross-Eval Patterns

- Are certain eval types consistently harder/easier?
- Do some evals show high variance while others are stable?
- Are there surprising results?

#### Step 4: Generate Notes

Write observations as a list of strings. Each note should:
- State a specific observation
- Be grounded in the data
- Help explain what the numbers show

Examples:
- "Assertion 'Output is a PDF' passes 100% in both configs - may not differentiate skill value"
- "Eval 3 shows high variance (50% ± 40%) - run 2 had an unusual failure"
- "Skill adds 13s average execution time but improves pass rate by 50%"

#### Step 5: Write Notes

Save to `{output_path}` as JSON:

```json
[
  "Assertion 'X' passes 100% in both configs - may not differentiate skill",
  "High variance in Eval 3 suggests non-deterministic behavior"
]
```
