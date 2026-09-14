# JSON Schemas for Agent Skill Creator

## evals.json

```json
{
  "skill_name": "my-skill",
  "evals": [
    {
      "id": 1,
      "prompt": "Realistic user query or task description",
      "expected_output": "Description of what the skill should produce",
      "files": ["optional list of input files"],
      "assertions": [
        {
          "text": "The output file exists",
          "type": "file_exists"
        },
        {
          "text": "The output contains 'Hello World'",
          "type": "contains",
          "value": "Hello World"
        }
      ]
    }
  ]
}
```

## grading.json

```json
{
  "expectations": [
    {
      "text": "The output file exists",
      "passed": true,
      "evidence": "File found at /tmp/output.pdf"
    },
    {
      "text": "The PDF contains the name field",
      "passed": false,
      "evidence": "No name field found in the form data"
    }
  ],
  "summary": {
    "passed": 1,
    "failed": 1,
    "total": 2,
    "pass_rate": 0.5
  },
  "execution_metrics": {
    "total_tool_calls": 15,
    "total_steps": 6,
    "errors_encountered": 0,
    "output_chars": 12450
  },
  "timing": {
    "total_duration_seconds": 165.0
  }
}
```

## timing.json

```json
{
  "total_tokens": 84852,
  "duration_ms": 23332,
  "total_duration_seconds": 23.3
}
```

## benchmark.json

```json
{
  "metadata": {
    "skill_name": "my-skill",
    "skill_path": "/path/to/skill",
    "timestamp": "2026-05-06T00:00:00Z",
    "runs": ["eval-1", "eval-2"]
  },
  "runs": [
    {
      "configuration": "with_skill",
      "run_number": 1,
      "result": {
        "pass_rate": 1.0,
        "passed": 3,
        "failed": 0,
        "total": 3,
        "time_seconds": 45.2,
        "tokens": 12000
      },
      "expectations": []
    }
  ],
  "run_summary": {
    "with_skill": {
      "pass_rate": { "mean": 1.0, "stddev": 0.0, "min": 1.0, "max": 1.0 },
      "time_seconds": { "mean": 45.2, "stddev": 3.1, "min": 42.1, "max": 48.3 },
      "tokens": { "mean": 12000, "stddev": 500, "min": 11500, "max": 12500 }
    },
    "delta": {
      "pass_rate": "+0.25",
      "time_seconds": "+12.3",
      "tokens": "+3500"
    }
  },
  "notes": []
}
```

## trigger_evals.json (for description optimization)

```json
[
  {
    "query": "specific realistic user prompt that should trigger this skill",
    "should_trigger": true
  },
  {
    "query": "a prompt that is adjacent but should NOT trigger this skill",
    "should_trigger": false
  }
]
```
