#!/usr/bin/env python3
"""Freeze explicitly reviewed Markdown records, then compare recall retrieval.

Experimental only. No transcript discovery, network, service or persistent index.
Private manifests, corpus snapshots and results belong outside the source repo.
"""

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import sqlite3


def digest(data):
    return hashlib.sha256(data).hexdigest()


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def sections(text):
    """Keep heading, line range and exact text; ignore headings inside fences."""
    start, heading, fenced = 1, "preamble", False
    lines = text.splitlines(keepends=True)
    for number, line in enumerate(lines, 1):
        if line.startswith(("```", "~~~")):
            fenced = not fenced
        match = re.match(r"^#{1,6} (.+?)\s*$", line) if not fenced else None
        if match:
            if number > start:
                yield heading, start, number - 1, "".join(lines[start - 1:number - 1])
            start, heading = number, match[1]
    if lines:
        yield heading, start, len(lines), "".join(lines[start - 1:])


def freeze(root, manifest):
    """Read only explicit regular .md files inside one authorized workspace."""
    root = root.resolve(strict=True)
    documents = []
    for source in manifest["sources"]:
        relative = Path(source["path"])
        if relative.is_absolute() or ".." in relative.parts or relative.suffix != ".md":
            raise ValueError("Invalid workspace Markdown path")
        if any(re.search(r"transcript|rollout|session", part, re.I) for part in relative.parts):
            raise ValueError("Transcript and session sources are excluded")
        path = root
        for part in relative.parts:
            path = path / part
            if path.is_symlink():
                raise ValueError("Symlink sources are excluded")
        if not path.is_file() or not path.resolve().is_relative_to(root):
            raise ValueError("Source must be a regular workspace file")
        raw = path.read_bytes()
        documents.append(dict(source, sha256=digest(raw), text=raw.decode("utf-8")))
    paths = [d["path"] for d in documents]
    if len(set(paths)) != len(paths):
        raise ValueError("Duplicate source path")
    return {"frozen_at": datetime.now(timezone.utc).isoformat(),
            "workspace_root": str(root), "documents": documents,
            "questions": manifest["questions"], "baseline": manifest["baseline"]}


def query_terms(question):
    # Both lexical and BM25 routes receive the same predeclared terms.
    return list(dict.fromkeys(re.findall(r"\w+", question["query"].lower())))


def benchmark(corpus):
    chunks = []
    documents = {d["path"]: d for d in corpus["documents"]}
    for document in corpus["documents"]:
        if digest(document["text"].encode("utf-8")) != document["sha256"]:
            raise ValueError("Frozen source digest mismatch")
        for heading, first, last, text in sections(document["text"]):
            chunks.append({"path": document["path"], "section": heading,
                           "first_line": first, "last_line": last, "text": text,
                           "date": document["date"], "sha256": document["sha256"],
                           "provenance": document["provenance"]})
    connection = sqlite3.connect(":memory:")
    try:
        connection.execute("CREATE VIRTUAL TABLE search USING fts5(text)")
        connection.executemany("INSERT INTO search(rowid, text) VALUES (?, ?)",
                               ((i + 1, c["text"]) for i, c in enumerate(chunks)))
        results = []
        for question in corpus["questions"]:
            for label in question["gold"] + question.get("stale", []):
                if not any(c["path"] == label["path"] and c["section"] == label["section"]
                           for c in chunks):
                    raise ValueError("Question label does not identify a frozen section")
            terms = query_terms(question)
            if not terms:
                raise ValueError("Empty benchmark query")
            match = " OR ".join('"' + term + '"' for term in terms)
            bm25 = [chunks[row[0] - 1] for row in connection.execute(
                "SELECT rowid FROM search WHERE search MATCH ? ORDER BY bm25(search), rowid LIMIT 5",
                (match,))]
            pattern = re.compile("|".join(re.escape(t) for t in terms), re.I)
            lexical = [c for c in sorted(chunks, key=lambda c: (c["path"], c["first_line"]))
                       if pattern.search(c["text"])][:5]
            # Old skill: index, current non-complete owner, then every other
            # non-complete record. Explicit frozen links are read afterwards.
            route = list(corpus["baseline"]["initial_paths"])
            owner = question["owner_path"]
            if owner in route:
                route.remove(owner)
                route.insert(1, owner)
            route += [p for p in question["linked_paths"] if p not in route]
            if any(p not in documents for p in route):
                raise ValueError("Baseline references an unfrozen source")
            route_chunks = [c for p in route for c in chunks if c["path"] == p]
            # Top five sources in the broad route are whole documents, so
            # section coverage is their entire text, unlike ranked chunks.
            broad = [dict(documents[p], section="whole document") for p in route[:5]]
            methods = {}
            for name, hits, read_chars in (
                ("existing_record_route", broad, sum(len(c["text"]) for c in route_chunks)),
                ("lexical_proxy", lexical, sum(len(c["text"]) for c in chunks)),
                ("fts5_bm25", bm25, sum(len(c["text"]) for c in bm25)),
            ):
                gold = question["gold"]
                correct = any(h["path"] == g["path"] for h in hits for g in gold)
                section_correct = any(h["path"] == g["path"] and
                                      (h["section"] == g["section"] or name == "existing_record_route")
                                      for h in hits for g in gold)
                stale = question.get("stale", [])
                stale_hits = [h for h in hits if any(
                    h["path"] == s["path"] and
                    (h["section"] == s["section"] or name == "existing_record_route") for s in stale)]
                top1_stale = bool(hits and any(hits[0] is h for h in stale_hits))
                methods[name] = {
                    "correct_source_at_5": correct, "correct_section_at_5": section_correct,
                    "text_read_chars": read_chars,
                    "returned_text_chars": sum(len(h["text"]) for h in hits),
                    "stale_candidates_at_5": len(stale_hits),
                    "top1_stale_authority_risk": top1_stale,
                    "hits": [{k: v for k, v in h.items() if k != "text"} for h in hits],
                }
            results.append({"id": question["id"], "question": question["question"], "methods": methods})
        summary = {}
        for name in results[0]["methods"]:
            rows = [r["methods"][name] for r in results]
            summary[name] = {key: sum(r[key] for r in rows) for key in (
                "correct_source_at_5", "correct_section_at_5", "text_read_chars",
                "returned_text_chars", "stale_candidates_at_5", "top1_stale_authority_risk")}
        return {"sqlite_version": sqlite3.sqlite_version, "questions": len(results),
                "documents": len(documents), "sections": len(chunks),
                "index_input_chars": sum(len(c["text"]) for c in chunks),
                "summary": summary, "results": results}
    finally:
        connection.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    snapshot = commands.add_parser("freeze")
    snapshot.add_argument("--workspace-root", type=Path, required=True)
    snapshot.add_argument("--manifest", type=Path, required=True)
    snapshot.add_argument("--output", type=Path, required=True)
    run = commands.add_parser("run")
    run.add_argument("--corpus", type=Path, required=True)
    run.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        # Reject output inside this script's owning repository when present.
        for parent in Path(__file__).resolve().parents:
            if (parent / ".git").exists() and args.output.resolve().is_relative_to(parent):
                raise ValueError("Private benchmark output must be outside the source repository")
        if args.output.exists():
            raise ValueError("Output already exists; preserve frozen evidence")
        if args.command == "freeze":
            result = freeze(args.workspace_root, read_json(args.manifest))
        else:
            raw = args.corpus.read_bytes()
            result = benchmark(json.loads(raw))
            result["corpus_sha256"] = digest(raw)
        with args.output.open("x", encoding="utf-8") as stream:
            json.dump(result, stream, indent=2)
            stream.write("\n")
    except (OSError, ValueError, KeyError, sqlite3.Error) as error:
        parser.exit(2, f"Recall benchmark failed: {error}\n")


if __name__ == "__main__":
    main()
