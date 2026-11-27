# Model policy resolver

[model-policy.yaml](../../../model-policy.yaml) owns preferences. [Model policy](model-policy.md) retains authorization, limits, classification and fallback rules. The Python CLI uses PyYAML, already used by the skill validator. It never launches, changes runs, reads credentials or discovers unrelated workspaces.

## Configuration

Schema version 1 has `t3.roles` and `direct.<harness>.roles`. Supported direct harnesses are `codex`, `claude`, `pi`, and `opencode`. Each global context contains all six roles: `task-research`, `task-implementation`, `exploration`, `implementation`, `review`, `advisor`.

Global `t3.difficulties`, when present, contains exactly `low`, `medium`, `high`, `hardest`, each a complete T3 selection. The managed policy enables it. General T3 task roles require `--difficulty` or a complete overriding task/workspace/project selection. This field is global only; workspace role overrides retain their existing schema. Direct contexts and helper/specialist roles reject `--difficulty` to preserve their separate selections. Without a difficulty table, existing policies retain role-only resolution.

A T3 selection has exactly `provider`, `model`, `options`; a direct selection has exactly `model`, `options`. `options` is an explicit mapping of native string/boolean settings. `{}` requests native defaults and clears T3 inheritance. Unknown fields, partial/null selections, unsupported schema versions, duplicate keys, tags, anchors, aliases and merge keys fail. No includes or executable expansion exist.

An optional private workspace override is the sibling `model-policy.yaml` of the explicitly routed registered workspace index. Register it with the exact Markdown link `[Model policy](model-policy.yaml)` in that index. Pass the index path as `--workspace` and its registered `id` as `--workspace-id`. The resolver verifies the index's `type: workspace` and matching ID. It reads only this index and sibling; it does not establish workspace routing authority itself. An absent override file or omitted role inherits global/project choices. A present invalid or unlinked file blocks, including when a task choice exists. Workspace contexts/roles may be sparse, but each present selection is complete and replaces the entire prior selection. No workspace preferences are created by this migration.

T3 provider aliases bind through machine-local `model-provider-bindings.yaml` beside the deployed policy, or the explicit `--bindings` path. This file is excluded from managed source. Its shape is:

```yaml
version: 1
providers:
  codex-default:
    providerInstanceId: explicitly-approved-instance
    driverKind: codex
```

Use only an explicitly approved account and live instance/driver evidence. No first-match guessing or cross-account substitution occurs. A stale or missing binding blocks. Bind other aliases only when their account choice is approved; aliases themselves grant no access.

## Commands

Invoke `python3` with the deployed `scripts/model-policy.py` path. Its default policy is beside the script directory. For source checks:

```sh
python3 scripts/model-policy.py validate
python3 scripts/model-policy.py explain --context t3 --role exploration
python3 scripts/model-policy.py resolve --context t3 --role review --capabilities capabilities.json --bindings bindings.yaml
python3 scripts/model-policy.py resolve --context t3 --role task-implementation --difficulty medium --operation t3_thread_launch --capabilities capabilities.json --bindings bindings.yaml
python3 scripts/model-policy.py compare --resolution resolution.json --observed returned.json
```

`validate` checks configuration offline. `explain` resolves precedence and reports the winning source/key, requested settings and SHA-256 hashes without launch arguments or availability claims. `resolve` requires current capability evidence and emits native launch arguments only after validation. Save its full JSON result for comparison and accounting. Every command rereads its inputs; no cache or watcher exists. Missing optional workspace files are recorded with a null hash so creation invalidates the prior resolution.

T3 capability input is the structured `orchestrator_capabilities` result. If a model is absent, the resolver returns `catalog_lookup_required`; query the live catalog with the model as `search`, then rerun with that targeted response. It never treats a short catalog as proof of unavailability. Check freshness and caller binding at dispatch, retain exact evidence hashes, and re-resolve if any source changes before launch.

For direct use, the caller supplies native evidence with `context`, `available: true`, `operation`, `clearsInheritedOptions: true`, and `models` using native `{id, options: [{id, values, default?}]}` descriptors. These statements must come from verified native discovery and tool contracts, not assumptions. Adapters emit Codex `spawn_agent` model/reasoning_effort, Claude `Agent` model/effort, Pi `subagent` model/thinking, and OpenCode `task` model/variant. Stop when the actual tool cannot accept those settings or clear inheritance. Verify each adapter against the current harness before relying on its emitted arguments. No harness switch repairs missing capability.

Nonempty T3 options can merge with inherited options for the same instance/model. The resolver explicitly replaces omitted inherited settings with advertised defaults. If a default is unclear it blocks. `{}` is passed literally to clear inheritance. Emitted arguments include only model selection; the caller supplies authorized task, title, scope, modes, runtime limits and workspace arguments separately. `--operation t3_thread_launch` emits `modelSelection` with native `instanceId`/`provider`; child dispatch emits `target` for `delegate_task`.

## Task and project inputs

`--task` accepts a YAML/JSON file containing one complete selection. Construct it from human instructions after resolving any partial model request against current native defaults. `--project` accepts:

```yaml
unresolved: []
default:
  provider: codex-default
  model: chosen-model
  options: {}
requirements:
  model: [chosen-model]
  options:
    reasoningEffort: [high]
```

`default` and `requirements` are optional; `unresolved` is required and must be empty. Requirements list allowed values for provider/model and each option. Direct inputs forbid provider. Read and classify applicable project instructions before constructing this input. Complete partial project declarations against the next applicable selection with live model defaults, and ask about ambiguity. Unresolved declarations block. Requirements constrain explicit task, workspace, project and global choices. Native defaults satisfy option constraints only when advertised. Repository-specific override files are deferred; arbitrary project prose is never parsed as configuration.

Precedence is task, workspace, approved project default, global. A missing role/file inherits; a present selection replaces the whole role. Existing recurring-job profiles retain their stored contracts. For future nonrecurring dispatch, classify existing profile choices as approved project defaults or requirements and pass them explicitly; do not migrate or inspect other workspaces automatically.

For a general T3 task with `--difficulty`, its global difficulty entry replaces only the global role default. Complete task, workspace role and approved project default selections still win; project requirements always constrain the final choice. The result includes this item's `difficulty` and the actual winning `source`/`key`, such as `t3.difficulties.medium` or `task`. Partial human model/account/effort instructions are completed into `--task` using the selected candidate and native option descriptors, retaining explicit values. No field merge or parent-option carryover occurs. Invalid difficulty mappings block validation even when another role is selected.

The CLI is stateless. Invoke it separately for each item; never reuse a previous item's difficulty or authorization. It emits actual native launch arguments for supported operations but never changes the parent runtime. For inline work on an existing parent, label the emitted selection as a candidate and record the actual parent model separately. Helpers resolve their roles independently, without the task's `--difficulty`. Difficulty changes neither launch/spend authority nor the pending quota-fallback decision.

## Runtime comparison and recovery

`compare` accepts returned T3 `{providerInstanceId, model, options}` metadata, where options may be a mapping or native ID/value array. Top-level T3 `modelSelection` responses are normalized automatically, including their provider driver. Child responses that omit the driver retain the catalog's driver validation; comparison checks runtime driver metadata whenever exposed. Direct callers normalize native metadata to `{model, options}`. Requested, resolved and observed settings remain separate. Missing model/instance/options metadata, or missing driver metadata on top-level responses, returns `unverified`; differing metadata returns `mismatch` and exit 2. Native option scalar types must match. Follow the existing recovery protocol and reconcile the original task before any replacement. No automatic duplicate launch occurs.

Expected rejections return categorized JSON on stderr and exit 2, with source/key and repair or supported values. They emit no launch arguments. Configuration or capability errors do not authorize fallback. For explicit Opus requests, follow [Claude Code selection](model-policy.md#t3-code-defaults), construct a complete T3 task choice with an approved Claude binding, then resolve independently. Carry no prior model options.

The included policy is an example of this setup's choices. Validate it against your own providers and available models before dispatch. Changes to the policy do not rewrite existing conversations, children, or scheduled runs.
