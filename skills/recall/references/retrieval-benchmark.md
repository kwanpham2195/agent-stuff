# Benchmark record retrieval

The [experimental benchmark](../scripts/benchmark-retrieval.py) uses Python's standard-library SQLite FTS5 and BM25. It does not change the recall route. Its in-memory index exists only during a run. Keep real workspace data and generated results outside the source repository.

## Freeze before ranking

Review an explicit manifest for one authorized workspace. Include only regular Markdown records and selected artifacts. Exclude transcripts, credentials and unrelated workspaces. The tool rejects traversal, absolute source paths, symlink sources and source names containing transcript, session or rollout. These checks support the review; they cannot classify arbitrary Markdown content as safe.

The manifest contains `sources`, `questions` and `baseline`. Each source has a workspace-relative `path`, evidence `date` and `provenance`. Each question has `id`, `question`, predeclared `query` terms, `owner_path`, `linked_paths`, `gold` path/section pairs and optional `stale` path/section pairs. Record whether each question is an actual quotation or a reconstruction from a real request or decision. Define the labels before inspecting rankings. `baseline.initial_paths` contains the workspace index followed by the old route's non-complete records in a declared fixed order.

Run these commands with explicit private paths for the placeholders:

```sh
python3 benchmark-retrieval.py freeze --workspace-root WORKSPACE --manifest MANIFEST --output CORPUS
python3 benchmark-retrieval.py run --corpus CORPUS --output RESULTS
```

The tool preserves exact source bytes, SHA-256 digests, dates and provenance in the corpus. Results retain paths, headings, line ranges and source digests. It refuses to overwrite an output. Runs use the frozen corpus without reading live sources. Keep the script revision and manifest/corpus hashes with the report.

## Interpret the comparison

The existing record route reads the index, promotes the current non-complete owner, reads the other non-complete records, then reads explicitly declared links. Its first five sources are whole documents. The old skill did not specify ordering among other records, so the manifest's ordering is a reproducible replay assumption. It is not a measurement of an agent's choices or transcript search.

The lexical proxy scans sections in path/line order using case-insensitive OR substring matching, similar to an unranked text search. BM25 receives the same query terms as FTS5 tokens and returns five sections. The tokenizer and substring semantics differ. Neither score nor a retrieved proposal establishes authority.

Report correct source and section coverage in the first five results. Report text read in characters, with its meaning for each route: the broad route's full read set, the lexical proxy's corpus scan, and BM25's returned sections. Report returned characters separately. BM25 also reads the entire corpus to build its index; include that cost. These counts are not model tokens, billed input, latency or equal retrieval units.

`stale_candidates_at_5` counts only prelabelled stale proposal sections. `top1_stale_authority_risk` reports whether the first result is one of those sections. Neither measures an agent falsely treating a proposal as accepted. Audit answers against the dated authority separately, recording false acceptance, false rejection and unanswered questions. Disclose label coverage, corpus omissions, reconstructed questions and the lack of a held-out set. A small successful run supports further evaluation, not adoption or a claim that recall triggers consistently.
