#!/usr/bin/env python3
"""Resolve model preferences without launching or changing any run.

Expected rejections emit a categorized JSON diagnostic to stderr and exit 2.
Only resolve emits launch arguments, after supplied live evidence validates them.
"""

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

import yaml


ROLES = frozenset(("task-research", "task-implementation", "exploration",
                   "implementation", "review", "advisor"))
HARNESSES = frozenset(("codex", "claude", "pi", "opencode"))
DIFFICULTIES = frozenset(("low", "medium", "high", "hardest"))
TASK_ROLES = frozenset(("task-research", "task-implementation"))
DEFAULT_POLICY = Path(__file__).resolve().parents[1] / "model-policy.yaml"
MAX_BYTES = 1024 * 1024
ABSENT = object()


class PolicyError(Exception):
    """A configuration, capability, or runtime rejection with a stable code."""

    def __init__(self, code, key, repair):
        self.code, self.key, self.repair = code, key, repair
        super().__init__(f"Model policy {code}: {key}: {repair}")


def require(condition, code, key, repair):
    if not condition:
        raise PolicyError(code, key, repair)


class StrictLoader(yaml.SafeLoader):
    """Reject YAML indirection and duplicate keys before constructing values."""

    def compose_node(self, parent, index):
        event = self.peek_event()
        require(not isinstance(event, yaml.AliasEvent) and
                not getattr(event, "anchor", None) and not getattr(event, "tag", None),
                "yaml_indirection", "YAML", "Remove tags, anchors and aliases")
        return super().compose_node(parent, index)

    def construct_mapping(self, node, deep=False):
        result = {}
        for key_node, value_node in node.value:
            require(key_node.tag == "tag:yaml.org,2002:str", "invalid_key", "YAML",
                    "Use string keys; merge keys are forbidden")
            key = self.construct_object(key_node, deep=deep)
            require(key not in result, "duplicate_key", key, "Keep exactly one key")
            result[key] = self.construct_object(value_node, deep=deep)
        return result


def load(path, hashes):
    """Read one explicit source and retain the digest of its exact bytes."""
    path = Path(path)
    data = path.read_bytes()
    require(len(data) <= MAX_BYTES, "input_limit", str(path), "Use at most 1 MiB")
    hashes[str(path)] = hashlib.sha256(data).hexdigest()
    return parse_yaml(data, str(path))


def parse_yaml(data, source):
    """Attach source evidence to YAML rejections, including workspace metadata."""
    try:
        return yaml.load(data.decode("utf-8"), Loader=StrictLoader)
    except PolicyError as error:
        raise PolicyError(error.code, source + ":" + error.key, error.repair) from error
    except (yaml.YAMLError, UnicodeError, RecursionError) as error:
        raise PolicyError("invalid_yaml", source, "Use valid plain YAML or JSON") from error


def fields(value, allowed, required, key):
    require(type(value) is dict, "invalid_mapping", key, "Supply a mapping")
    require(not (set(value) - set(allowed)), "unknown_field", key,
            f"Supported fields: {', '.join(sorted(allowed))}")
    require(set(required) <= set(value), "missing_field", key,
            f"Required fields: {', '.join(sorted(required))}")


def name(value, key):
    require(type(value) is str and bool(value.strip()) and value == value.strip() and
            not any(ord(c) < 32 for c in value), "invalid_string", key,
            "Supply a nonempty string without surrounding whitespace or controls")
    return value


def selection(value, context, key):
    keys = {"model", "options"} | ({"provider"} if context == "t3" else set())
    fields(value, keys, keys, key)
    for field in keys - {"options"}:
        name(value[field], f"{key}.{field}")
    require(type(value["options"]) is dict, "invalid_options", key + ".options",
            "Supply an explicit mapping; {} selects native defaults")
    for option, setting in value["options"].items():
        name(option, key + ".options")
        require(type(setting) in (str, bool), "invalid_option_type", key + ".options." + option,
                "Use a native string or boolean option")
    return value


def policy(value, key, sparse=False):
    fields(value, {"version", "t3", "direct"}, {"version"} if sparse else
           {"version", "t3", "direct"}, key)
    require(type(value["version"]) is int and value["version"] == 1,
            "schema_version", key + ".version", "Supported version: 1")
    contexts = {}
    if "t3" in value:
        contexts["t3"] = value["t3"]
    if "direct" in value:
        fields(value["direct"], HARNESSES, () if sparse else HARNESSES, key + ".direct")
        contexts.update({"direct." + harness: roles for harness, roles in value["direct"].items()})
    for context, section in contexts.items():
        allowed = {"roles", "difficulties"} if context == "t3" and not sparse else {"roles"}
        fields(section, allowed, {"roles"}, key + "." + context)
        if "difficulties" in section:
            fields(section["difficulties"], DIFFICULTIES, DIFFICULTIES, key + ".t3.difficulties")
            for difficulty, choice in section["difficulties"].items():
                selection(choice, context, key + ".t3.difficulties." + difficulty)
        fields(section["roles"], ROLES, () if sparse else ROLES, key + "." + context + ".roles")
        for role, choice in section["roles"].items():
            selection(choice, context, key + "." + context + ".roles." + role)
    return contexts


def workspace_policy(index, identity, hashes):
    """Use only the caller-routed index and its explicitly linked sibling file."""
    index = Path(index)
    require(not index.is_symlink() and index.is_file(), "workspace_identity", str(index),
            "Use a regular registered workspace index")
    data = index.read_bytes()
    require(len(data) <= MAX_BYTES, "input_limit", str(index), "Use at most 1 MiB")
    hashes[str(index)] = hashlib.sha256(data).hexdigest()
    text = data.decode("utf-8")
    match = re.match(r"\A---\n(.*?)\n---(?:\n|$)", text, re.S)
    require(match is not None, "workspace_identity", str(index), "Supply a registered workspace index")
    metadata = parse_yaml(match[1].encode(), str(index))
    require(type(metadata) is dict and metadata.get("type") == "workspace" and
            metadata.get("id") == identity, "workspace_identity", str(index),
            "Match --workspace-id to the routed workspace index")
    target = index.parent / "model-policy.yaml"
    require(not target.is_symlink(), "workspace_source", str(target), "Use a regular sibling policy file")
    linked = "[Model policy](model-policy.yaml)" in text
    require(not target.exists() or linked, "workspace_unlinked", str(target),
            "Register [Model policy](model-policy.yaml) in this workspace index")
    if not target.exists():
        hashes[str(target)] = None
        return {}
    return policy(load(target, hashes), str(target), sparse=True)


def project_policy(value, context, key):
    fields(value, {"default", "requirements", "unresolved"}, {"unresolved"}, key)
    require(type(value["unresolved"]) is list and not value["unresolved"],
            "project_unresolved", key, "Classify conflicting project declarations first")
    if "default" in value:
        selection(value["default"], context, key + ".default")
    requirements = value.get("requirements", {})
    fields(requirements, {"model", "options"} | ({"provider"} if context == "t3" else set()), (), key)
    for field, allowed in requirements.items():
        if field == "options":
            require(type(allowed) is dict, "invalid_constraint", key + ".requirements.options",
                    "Supply option names mapped to allowed-value lists")
        entries = allowed.items() if field == "options" and type(allowed) is dict else [(field, allowed)]
        for option, values in entries:
            name(option, key + ".requirements")
            require(type(values) is list and bool(values) and
                    all(type(v) in ((str, bool) if field == "options" else (str,)) for v in values), "invalid_constraint",
                    key + ".requirements." + option, "Supply nonempty allowed-value lists")
    return value


def check_requirements(choice, requirements, key):
    for field, allowed in requirements.items():
        if field == "options":
            for option, values in allowed.items():
                require(choice["options"].get(option) in values, "project_conflict", key + ".options." + option,
                        f"Requested value must satisfy project allowed values {values}")
        else:
            require(choice[field] in allowed, "project_conflict", key + "." + field,
                    f"Requested {choice[field]}; project allows {allowed}")


def validate_model(choice, models, key):
    require(type(models) is list and all(type(m) is dict for m in models),
            "invalid_capabilities", key, "Supply native model descriptors")
    matches = [m for m in models if m.get("id") == choice["model"]]
    require(len(matches) == 1, "catalog_lookup_required", key + ".model",
            f"Requested {choice['model']}; perform targeted native catalog lookup, then supply its evidence")
    descriptors = matches[0].get("options")
    if descriptors is None:
        descriptors = []
    require(type(descriptors) is list and all(type(d) is dict and type(d.get("id")) is str and
            type(d.get("values")) is list and bool(d["values"]) and
            all(type(v) in (str, bool) for v in d["values"]) for d in descriptors),
            "invalid_capabilities", key, "Supply option IDs and supported values")
    options = {d["id"]: d for d in descriptors}
    require(len(options) == len(descriptors), "ambiguous_catalog", key, "Refresh option descriptors")
    for option, descriptor in options.items():
        require(descriptor.get("default") is None or any(type(descriptor["default"]) is type(v) and
                descriptor["default"] == v for v in descriptor["values"]),
                "invalid_capabilities", key + ".options." + option, "Advertised default must be a supported native value")
    for option, setting in choice["options"].items():
        require(option in options, "unsupported_option", key + ".options." + option,
                f"Requested {setting}; supported options: {sorted(options)}")
        require(any(type(setting) is type(v) and setting == v for v in options[option].get("values", [])),
                "unsupported_value", key + ".options." + option,
                f"Requested {setting}; supported values: {options[option].get('values', [])}")
    return options


def effective_options(choice, descriptors):
    """Advertised defaults satisfy constraints without becoming preferences."""
    return {**{k: v["default"] for k, v in descriptors.items() if v.get("default") is not None},
            **choice["options"]}


def native_launch(choice, context, evidence, bindings, key, operation=None):
    """Translate validated choices into the selected native tool's arguments."""
    require(type(evidence) is dict, "capability_evidence", key, "Supply current native capability evidence")
    if context == "t3":
        operation = operation or "delegate_task"
        require(operation in ("delegate_task", "t3_thread_launch"), "operation_unavailable", key,
                "Supported T3 operations: delegate_task, t3_thread_launch")
        fields(bindings, {"version", "providers"}, {"version", "providers"}, "bindings")
        require(type(bindings["version"]) is int and bindings["version"] == 1,
                "schema_version", "bindings.version", "Supported version: 1")
        require(type(bindings["providers"]) is dict, "invalid_mapping", "bindings.providers", "Supply explicit aliases")
        for alias, binding in bindings["providers"].items():
            name(alias, "bindings.providers")
            fields(binding, {"providerInstanceId", "driverKind"}, {"providerInstanceId", "driverKind"}, "bindings." + alias)
            name(binding["providerInstanceId"], "bindings." + alias)
            name(binding["driverKind"], "bindings." + alias)
        require(choice["provider"] in bindings["providers"], "binding_missing", key + ".provider",
                f"Explicitly bind alias {choice['provider']} on this machine; never guess an account")
        binding = bindings["providers"][choice["provider"]]
        catalog = evidence.get("providers")
        require(type(catalog) is list and all(type(p) is dict for p in catalog),
                "invalid_capabilities", key, "Supply the native providers catalog")
        providers = [p for p in catalog if p.get("providerInstanceId") == binding["providerInstanceId"]]
        require(len(providers) == 1 and providers[0].get("driverKind") == binding["driverKind"],
                "binding_stale", key + ".provider", "Refresh the explicit instance/driver binding; do not substitute accounts")
        provider = providers[0]
        require(not provider.get("constraints"), "operation_unavailable", key,
                "Resolve the selected provider's advertised constraints before launch")
        features = evidence.get("features", {})
        require(type(features) is dict, "invalid_capabilities", key + ".features", "Supply native feature descriptors")
        require((operation == "t3_thread_launch" and features.get("threadManagement") is True) or
                (operation == "delegate_task" and provider.get("canRunChildTask") is True and
                (evidence.get("inheritedProviderInstanceId") == binding["providerInstanceId"] or
                 provider.get("canRunCrossProviderChildTask") is True)),
                "operation_unavailable", key, "Selected provider must support this delegation operation")
        descriptors = validate_model(choice, provider.get("models", []), key)
        options = dict(choice["options"])
        # {} clears T3 inheritance. A nonempty map merges, so overwrite every
        # inherited setting when targeting the same provider and model.
        if options and evidence.get("inheritedProviderInstanceId") == binding["providerInstanceId"] and evidence.get("inheritedModel") == choice["model"]:
            inherited_options = evidence.get("inheritedOptions")
            if inherited_options is None:
                inherited_options = []
            require(type(inherited_options) is list and all(type(i) is dict and
                    type(i.get("id")) is str for i in inherited_options),
                    "invalid_capabilities", key, "Supply native inherited option records")
            for inherited in inherited_options:
                option = inherited["id"]
                if option not in options:
                    descriptor = descriptors.get(option, {})
                    require(descriptor.get("default") is not None, "inherited_option_unclear", key + ".options." + option,
                            "Native default is not advertised; supply an explicit complete choice")
                    options[option] = descriptor["default"]
        validate_model({**choice, "options": options}, provider.get("models", []), key)
        args = {"providerInstanceId": binding["providerInstanceId"], "model": choice["model"], "options": options}
        resolved = {**args, "driverKind": binding["driverKind"]}
        if operation == "t3_thread_launch":
            return {"tool": operation, "arguments": {"modelSelection": {
                "instanceId": binding["providerInstanceId"], "provider": binding["driverKind"],
                "model": choice["model"], "options": options}}}, resolved, effective_options(choice, descriptors)
        return {"tool": "delegate_task", "arguments": {"target": args}}, resolved, effective_options(choice, descriptors)
    require(evidence.get("context") == context and evidence.get("available") is True,
            "operation_unavailable", key, "Supply current evidence from this direct harness; do not switch harness")
    descriptors = validate_model(choice, evidence.get("models", []), key)
    adapters = {"direct.codex": ("spawn_agent", {"reasoningEffort": "reasoning_effort"}),
                "direct.claude": ("Agent", {"effort": "effort"}),
                "direct.pi": ("subagent", {"thinking": "thinking"}),
                "direct.opencode": ("task", {"variant": "variant"})}
    tool, names = adapters[context]
    require(operation in (None, tool), "operation_unavailable", key, f"Use native {tool} operation")
    require(evidence.get("operation") == tool, "operation_unavailable", key, f"Verify native {tool} operation")
    require(set(choice["options"]) <= set(names), "adapter_option", key, f"Adapter supports {sorted(names)}")
    require(evidence.get("clearsInheritedOptions") is True, "inheritance_unverified", key,
            "Verify native launch starts with defaults instead of inherited options")
    args = {"model": choice["model"], **{names[k]: v for k, v in choice["options"].items()}}
    return {"tool": tool, "arguments": args}, {"model": choice["model"], "options": choice["options"]}, effective_options(choice, descriptors)


def resolve(policy_path, context, role, hashes, workspace=None, workspace_id=None, task=ABSENT,
            project=ABSENT, evidence=None, bindings=None, live=False, operation=None, difficulty=None):
    """Resolve whole selections by precedence and optionally validate live settings."""
    contexts = policy(load(policy_path, hashes), str(policy_path))
    require(context in contexts, "unknown_context", context, f"Supported contexts: {sorted(contexts)}")
    require(role in ROLES, "unknown_role", role, f"Supported roles: {sorted(ROLES)}")
    key = context + ".roles." + role
    choice, source = contexts[context]["roles"][role], str(policy_path)
    difficulties = contexts[context].get("difficulties", {})
    if difficulty is not None:
        require(context == "t3" and role in TASK_ROLES, "difficulty_scope", key,
                "Task difficulty applies only to T3 task-research/task-implementation; resolve helpers and specialists by role")
        require(type(difficulty) is str and difficulty in DIFFICULTIES, "unknown_difficulty", key,
                f"Supported task difficulties: {sorted(DIFFICULTIES)}")
        require(difficulty in difficulties, "difficulty_unconfigured", str(policy_path),
                "Configure the complete global T3 difficulty mapping before selecting it")
        choice, key = difficulties[difficulty], "t3.difficulties." + difficulty
    overridden = False
    project = project_policy(project, context, "project") if project is not ABSENT else {"unresolved": []}
    if "default" in project:
        choice, source, key = project["default"], "project.default", "project.default"
        overridden = True
    if workspace:
        require(bool(workspace_id), "workspace_identity", str(workspace), "Supply --workspace-id")
        override = workspace_policy(workspace, workspace_id, hashes)
        if role in override.get(context, {}).get("roles", {}):
            choice, source, key = override[context]["roles"][role], str(Path(workspace).parent / "model-policy.yaml"), context + ".roles." + role
            overridden = True
    if task is not ABSENT:
        choice, source, key = selection(task, context, "task"), "task", "task"
        overridden = True
    require(not (context == "t3" and role in TASK_ROLES and difficulties and
                 difficulty is None and not overridden), "difficulty_required", context + ".roles." + role,
            "Classify this work item with --difficulty low|medium|high|hardest, or supply an explicit task/workspace/project selection")
    result = {"context": context, "role": role, "source": source, "key": key,
              "hashes": hashes, "requested": choice, "availability": "not_checked"}
    if difficulty is not None:
        result["difficulty"] = difficulty
    if live:
        launch, resolved, effective = native_launch(choice, context, evidence, bindings, key, operation)
        check_requirements({**choice, "options": effective}, project.get("requirements", {}), key)
        result.update(availability="validated_against_supplied_evidence", resolved=resolved,
                      effectiveOptions=effective, launch=launch)
    else:
        # Check explicit conflicts offline, but defaults need live descriptors.
        constraints = project.get("requirements", {})
        explicit = {k: v for k, v in constraints.items() if k != "options"}
        explicit["options"] = {k: v for k, v in constraints.get("options", {}).items() if k in choice["options"]}
        check_requirements(choice, explicit, key)
    return result


def compare_runtime(resolution, observed):
    """Compare normalized returned metadata; absent fields remain unverified."""
    require(type(resolution) is dict and type(resolution.get("resolved")) is dict and
            "requested" in resolution and type(observed) is dict,
            "invalid_runtime_metadata", "compare", "Supply a resolver result and returned native metadata mapping")
    expected = resolution["resolved"]
    fields(expected, {"providerInstanceId", "driverKind", "model", "options"}, {"model", "options"}, "resolution.resolved")
    selection({"model": expected["model"], "options": expected["options"]}, "direct.codex", "resolution.resolved")
    if "providerInstanceId" in expected:
        name(expected["providerInstanceId"], "resolution.resolved.providerInstanceId")
    if "driverKind" in expected:
        name(expected["driverKind"], "resolution.resolved.driverKind")
    launch = resolution.get("launch", {})
    require(type(launch) is dict, "invalid_runtime_metadata", "resolution.launch",
            "Supply the saved resolver launch result")
    if type(observed.get("modelSelection")) is dict:
        native = observed["modelSelection"]
        observed = {"providerInstanceId": native.get("instanceId"),
                    "driverKind": native.get("provider"), "model": native.get("model"), "options": native.get("options")}
    differences, missing = [], []
    keys = ["providerInstanceId", "model", "options"]
    if "driverKind" in observed or launch.get("tool") == "t3_thread_launch":
        keys.append("driverKind")
    for key in keys:
        if key not in expected:
            continue
        if key not in observed or observed[key] is None:
            missing.append(key)
        elif key == "options":
            actual = observed[key]
            if type(actual) is list:
                require(all(type(item) is dict and type(item.get("id")) is str and
                        "value" in item for item in actual), "invalid_runtime_metadata",
                        "observed.options", "Supply native option ID/value records")
                require(len({item["id"] for item in actual}) == len(actual),
                        "invalid_runtime_metadata", "observed.options", "Remove ambiguous duplicate options")
                actual = {item["id"]: item["value"] for item in actual}
            require(type(actual) is dict and all(type(k) is str and type(v) in (str, bool)
                    for k, v in actual.items()), "invalid_runtime_metadata", "observed.options",
                    "Native option values must be strings or booleans")
            if set(actual) != set(expected[key]) or any(type(actual[k]) is not type(v) or actual[k] != v
                                                      for k, v in expected[key].items() if k in actual):
                differences.append(key)
        elif observed[key] != expected[key]:
            differences.append(key)
    return {"status": "mismatch" if differences else "unverified" if missing else "verified",
            "differences": differences, "missing": missing,
            "requested": resolution["requested"], "resolved": expected, "observed": observed}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("validate", "explain", "resolve", "compare"))
    parser.add_argument("--policy", type=Path, default=DEFAULT_POLICY)
    parser.add_argument("--context", choices=["t3"] + ["direct." + h for h in sorted(HARNESSES)])
    parser.add_argument("--role", choices=sorted(ROLES))
    parser.add_argument("--workspace", type=Path, help="Explicit registered workspace index")
    parser.add_argument("--workspace-id")
    parser.add_argument("--operation", help="Native operation; defaults to delegate_task in T3")
    parser.add_argument("--difficulty", help="This work item's task difficulty: low, medium, high, hardest")
    for flag in ("task", "project", "capabilities", "bindings", "resolution", "observed"):
        parser.add_argument("--" + flag, type=Path)
    args = parser.parse_args()
    hashes = {}
    try:
        if args.command == "compare":
            require(args.resolution and args.observed, "missing_input", "compare", "Supply --resolution and --observed")
            result = compare_runtime(load(args.resolution, hashes), load(args.observed, hashes))
        elif args.command == "validate":
            policy(load(args.policy, hashes), str(args.policy))
            if args.workspace:
                require(bool(args.workspace_id), "workspace_identity", str(args.workspace), "Supply --workspace-id")
                workspace_policy(args.workspace, args.workspace_id, hashes)
            result = {"status": "valid", "availability": "not_checked", "hashes": hashes}
        else:
            require(args.context and args.role, "missing_input", args.command, "Supply --context and --role")
            live = args.command == "resolve"
            require(not live or args.capabilities, "capability_evidence", "resolve", "Supply current --capabilities")
            bindings = args.bindings
            if live and args.context == "t3" and bindings is None:
                bindings = args.policy.parent / "model-provider-bindings.yaml"
            result = resolve(args.policy, args.context, args.role, hashes, args.workspace, args.workspace_id,
                             load(args.task, hashes) if args.task else ABSENT,
                             load(args.project, hashes) if args.project else ABSENT,
                             load(args.capabilities, hashes) if args.capabilities else None,
                             load(bindings, hashes) if bindings else None, live, args.operation, args.difficulty)
            if not live:
                result["status"] = "offline_explanation"
        print(json.dumps(result, sort_keys=True))
        return 2 if result.get("status") == "mismatch" else 0
    except PolicyError as error:
        print(json.dumps({"error": error.code, "key": error.key, "repair": error.repair}), file=sys.stderr)
        return 2
    except (OSError, UnicodeError) as error:
        print(json.dumps({"error": "source_unavailable", "key": str(error.filename) if isinstance(error, OSError) else "encoding",
                          "repair": "Check explicit source paths, permissions and UTF-8 encoding"}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
