#!/usr/bin/env python3
"""Validate improvement receipts or report changed evidence without writing state."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime
from pathlib import Path


class ReceiptError(ValueError):
    """An incomplete or contradictory receipt cannot support an improvement claim."""


def text(value, field):
    if not isinstance(value, str) or not value.strip() or value != value.strip():
        raise ReceiptError(f"Nonempty text required: {field}")
    return value


def fields(value, required, optional=()):
    if not isinstance(value, dict) or set(value) - set(required) - set(optional) or set(required) - set(value):
        raise ReceiptError(f"Receipt fields must include {', '.join(required)}")


def count(value, field):
    if type(value) is not int or value < 0:
        raise ReceiptError(f"Nonnegative integer required: {field}")


def digest(value):
    if not isinstance(value, str) or not re.fullmatch(r"[0-9a-f]{64}", value):
        raise ReceiptError("SHA-256 digest required")


def timestamp(value, field):
    """Require explicit UTC seconds, never infer a timezone or the current time."""
    if not isinstance(value, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", value):
        raise ReceiptError(f"UTC timestamp required: {field}")
    try:
        return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError as exc:
        raise ReceiptError(f"Invalid UTC timestamp: {field}") from exc


def unique_texts(value, field, nonempty=False):
    if not isinstance(value, list) or (nonempty and not value):
        raise ReceiptError(f"List required: {field}")
    for item in value:
        text(item, field)
    if len(set(value)) != len(value):
        raise ReceiptError(f"Duplicate identity: {field}")


def validate_receipts(data):
    """Return validated receipts; validation never reads evidence links."""
    fields(data, ("version", "candidates"))
    if data["version"] != 1 or not isinstance(data["candidates"], list):
        raise ReceiptError("Unsupported improvement receipt version or candidate list")
    identities = set()
    for candidate in data["candidates"]:
        fields(candidate, ("work", "id", "state", "evidence", "failure_class", "acceptance",
                           "source", "execution", "mechanism", "authority", "trial", "deployment", "follow_up", "measures"))
        identity = (text(candidate["work"], "work"), text(candidate["id"], "id"))
        if identity in identities:
            raise ReceiptError("Duplicate candidate identity")
        identities.add(identity)
        if candidate["state"] not in {"observed", "proposed", "authorized-for-trial", "evaluated", "deployed", "followed-up", "rejected", "inconclusive"}:
            raise ReceiptError("Unknown candidate state")
        if candidate["failure_class"] not in {"none", "task-defect", "instruction", "infrastructure", "new-scope", "unknown"}:
            raise ReceiptError("Unknown failure class")
        unique_texts(candidate["evidence"], "evidence", nonempty=True)
        for key in ("mechanism", "authority"):
            text(candidate[key], key)
        acceptance = candidate["acceptance"]
        fields(acceptance, ("result", "criteria", "evidence", "human"))
        if acceptance["result"] not in {"met", "not-met", "unknown"} or acceptance["human"] not in {"accepted", "pending", "not-required"}:
            raise ReceiptError("Unknown acceptance result")
        text(acceptance["criteria"], "criteria")
        unique_texts(acceptance["evidence"], "acceptance evidence", acceptance["result"] == "met")
        source = candidate["source"]
        fields(source, ("revision", "loaded"))
        text(source["revision"], "revision")
        if not isinstance(source["loaded"], list):
            raise ReceiptError("Loaded sources must be a list")
        loaded_paths = []
        for loaded in source["loaded"]:
            fields(loaded, ("path", "sha256"))
            loaded_paths.append(text(loaded["path"], "loaded path"))
            digest(loaded["sha256"])
        unique_texts(loaded_paths, "loaded paths")
        execution = candidate["execution"]
        fields(execution, ("provider", "model", "options", "tools", "runs"))
        for key in ("provider", "model"):
            text(execution[key], key)
        if not isinstance(execution["options"], dict):
            raise ReceiptError("Model options must be an object")
        unique_texts(execution["tools"], "tools")
        unique_texts(execution["runs"], "runs")
        trial = candidate["trial"]
        if trial is not None:
            fields(trial, ("fixture_sha256", "rubric_sha256", "valid", "verdict", "evidence", "invalid_reason"))
            digest(trial["fixture_sha256"])
            digest(trial["rubric_sha256"])
            if type(trial["valid"]) is not bool or trial["verdict"] not in {"pass", "fail", "inconclusive", "invalid"}:
                raise ReceiptError("Invalid trial classification")
            unique_texts(trial["evidence"], "trial evidence", nonempty=True)
            if not trial["valid"]:
                text(trial["invalid_reason"], "invalid reason")
                if trial["verdict"] != "invalid":
                    raise ReceiptError("Invalid trials cannot receive a quality verdict")
            elif trial["invalid_reason"] is not None or trial["verdict"] == "invalid" or not source["loaded"]:
                raise ReceiptError("Valid trials require loaded-source exposure and no invalid reason")
            if trial["valid"]:
                unique_texts(execution["runs"], "valid trial run IDs", nonempty=True)
        deployment = candidate["deployment"]
        if deployment is not None:
            fields(deployment, ("commit", "previous_revision", "targets", "parity_evidence", "fresh_run_evidence", "rollback"))
            for key in ("commit", "previous_revision", "parity_evidence", "rollback"):
                text(deployment[key], key)
            unique_texts(deployment["targets"], "targets", nonempty=True)
            if deployment["fresh_run_evidence"] is not None:
                text(deployment["fresh_run_evidence"], "fresh run evidence")
        follow_up = candidate["follow_up"]
        fields(follow_up, ("target_tasks", "working_days", "applicable_tasks", "mistake_tasks", "unknown_coverage", "evidence", "started_at", "deadline_at"))
        started, deadline = follow_up["started_at"], follow_up["deadline_at"]
        if started is not None:
            timestamp(started, "started_at")
        if deadline is not None:
            timestamp(deadline, "deadline_at")
            if started is None or timestamp(deadline, "deadline_at") <= timestamp(started, "started_at"):
                raise ReceiptError("Follow-up deadline requires an earlier known start")
        for key in ("target_tasks", "working_days", "unknown_coverage"):
            count(follow_up[key], key)
        if not follow_up["target_tasks"] or not follow_up["working_days"]:
            raise ReceiptError("Follow-up bounds must be positive")
        for key in ("applicable_tasks", "mistake_tasks", "evidence"):
            unique_texts(follow_up[key], key)
        if not set(follow_up["mistake_tasks"]) <= set(follow_up["applicable_tasks"]):
            raise ReceiptError("Mistake numerator exceeds applicable task denominator")
        measures = candidate["measures"]
        fields(measures, ("accepted_tasks", "user_interventions", "repeated_work", "elapsed_seconds", "queue_seconds", "human_wait_seconds", "provider_outage_seconds", "tokens", "cost"))
        unique_texts(measures["accepted_tasks"], "accepted tasks")
        for key in ("user_interventions", "repeated_work", "tokens"):
            if measures[key] is not None:
                count(measures[key], key)
        for key in ("elapsed_seconds", "queue_seconds", "human_wait_seconds", "provider_outage_seconds", "cost"):
            value = measures[key]
            if value is not None and (type(value) not in (int, float) or value < 0 or not value < float("inf")):
                raise ReceiptError(f"Nonnegative finite measurement or null required: {key}")
        state = candidate["state"]
        if state in {"evaluated", "deployed", "followed-up"} and trial is None:
            raise ReceiptError("Evaluated candidates require a trial receipt")
        if state in {"deployed", "followed-up"} and (deployment is None or not trial["valid"] or trial["verdict"] != "pass"):
            raise ReceiptError("Promotion requires a valid passing trial and deployment receipt")
        if state in {"deployed", "followed-up"} and (acceptance["result"] != "met" or acceptance["human"] == "pending"):
            raise ReceiptError("Promotion requires satisfied acceptance and resolved human gates")
        if state in {"deployed", "followed-up"} and not deployment["fresh_run_evidence"]:
            raise ReceiptError("Promotion requires fresh-run exposure evidence")
        if state == "followed-up" and (not deployment["fresh_run_evidence"] or len(follow_up["applicable_tasks"]) < follow_up["target_tasks"] or not follow_up["evidence"]):
            raise ReceiptError("Follow-up requires fresh exposure and applicable observed tasks")
    return data


def review_delta(data, prior, as_of):
    """Deduplicate evidence and deadline transitions at an explicit UTC instant."""
    now = timestamp(as_of, "as_of")
    validate_receipts(data)
    fields(prior, ("version", "watermarks"))
    if prior["version"] != 1 or not isinstance(prior["watermarks"], dict):
        raise ReceiptError("Invalid prior review receipt")
    for key, value in prior["watermarks"].items():
        text(key, "watermark identity")
        digest(value)
    watermarks = dict(prior["watermarks"])
    updates = []
    for candidate in data["candidates"]:
        key = json.dumps([candidate["work"], candidate["id"]], separators=(",", ":"))
        follow_up = candidate["follow_up"]
        overdue = (follow_up["deadline_at"] is not None
                   and now >= timestamp(follow_up["deadline_at"], "deadline_at")
                   and candidate["state"] not in {"followed-up", "rejected"}
                   and (len(follow_up["applicable_tasks"]) < follow_up["target_tasks"] or not follow_up["evidence"]))
        value = hashlib.sha256(json.dumps([candidate, overdue], sort_keys=True, separators=(",", ":")).encode()).hexdigest()
        if watermarks.get(key) != value:
            updates.append({"work": candidate["work"], "id": candidate["id"], "state": candidate["state"], "follow_up_overdue": overdue})
            watermarks[key] = value
    return {"updates": updates, "launches": [], "receipt": {"version": 1, "watermarks": watermarks}}


def compare_trials(baseline, candidate):
    """Check matched trial metadata; an eligible comparison is not a quality win."""
    validate_receipts(baseline)
    validate_receipts(candidate)
    if len(baseline["candidates"]) != 1 or len(candidate["candidates"]) != 1:
        raise ReceiptError("A matched comparison requires one candidate per arm")
    left, right = baseline["candidates"][0], candidate["candidates"][0]
    if set(left["execution"]["runs"]) & set(right["execution"]["runs"]):
        raise ReceiptError("Matched trial arms must have disjoint run IDs")
    for key in ("work", "id"):
        if left[key] != right[key]:
            raise ReceiptError("Matched trial candidate identity differs")
    for item in (left, right):
        if item["trial"] is None or not item["trial"]["valid"] or not item["source"]["loaded"]:
            raise ReceiptError("Matched trials require valid results and recorded exposure")
    for key in ("provider", "model", "options", "tools"):
        if left["execution"][key] != right["execution"][key]:
            raise ReceiptError(f"Matched trial execution differs: {key}")
    for key in ("fixture_sha256", "rubric_sha256"):
        if left["trial"][key] != right["trial"][key]:
            raise ReceiptError(f"Frozen comparison input differs: {key}")
    if left["acceptance"]["criteria"] != right["acceptance"]["criteria"]:
        raise ReceiptError("Matched trial acceptance criteria differ")
    return {"comparable_metadata": True, "quality_verdict": "requires-independent-assessment"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--prior", type=Path, help="Compute a review delta against a delivered receipt")
    mode.add_argument("--baseline", type=Path, help="Check matched trial metadata without assigning a quality score")
    parser.add_argument("--as-of", help="Explicit UTC review time, required with --prior")
    args = parser.parse_args()
    try:
        data = validate_receipts(json.loads(args.input.read_text()))
        if args.prior:
            result = review_delta(data, json.loads(args.prior.read_text()), args.as_of)
        elif args.baseline:
            result = compare_trials(json.loads(args.baseline.read_text()), data)
        else:
            result = {"valid_candidates": len(data["candidates"])}
        print(json.dumps(result, indent=2))
        return 0
    except (OSError, ValueError, TypeError) as exc:
        print(f"Improvement receipt rejected: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
