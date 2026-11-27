# Lint rules and enforcement

Open this file when a task touches linter settings, a home-grown rule, or a bulk code-fix tool. The code-level expectations themselves live in the [parsing guide](parsing-and-schemas.md), the [safety guide](typescript-safety.md), and the [module guide](modules-services-and-adapters.md#reducing-complexity-without-losing-cohesion). This page is only about what a lint setup can honestly demonstrate.

## What to report

For a cleanup, state whether it removed work, merely re-typed existing parsing, or narrowed an API, and attach the relevant [regression evidence](testing.md#regression-evidence-for-parsing-and-recovery) and [inference checks](testing.md#compile-time-behavior). Passing lint, a reduced warning count, and a green fixture each show something different, so do not substitute one for another. Name the blind spots that remain. In docs, keep rules that are live apart from rules that are merely suggested, and do not trade away a safety property or public contract to make a rule easier.

## Start from what actually executes

Inspect the top-level config, whichever scripts or tasks invoke the linter, the installed plugin versions, and the ignore lists. Only after that can you claim a rule applies somewhere. Something mentioned in a design note but absent from config is an idea, not a safeguard. Numbers and rule lists belong in config, never duplicated in documents.

## What a rule cannot see

A rule working from syntax and local scope has no access to compiler types, regardless of whether the project type-checks in other tasks. It is fine for patterns confined to one file. Anything flowing in through imports, derived from schemas, or passed between functions needs type-aware linting or a reviewer. Whenever you propose a rule, spell out both what it detects and what it misses.

## Pairing problems with checks

- Widened or re-asserted types: a syntactic rule for the obvious shapes, type-aware rules for anything deeper.
- Dead conditions: the compiler-backed unnecessary-condition rule, with its options set so that real runtime validation and deliberate infinite loops are left alone.
- Parsers or helpers that leak internals through their exports: a narrow rule that follows re-exports, plus a stated exception for intentional low-level APIs.
- Unused exports: a workspace audit that includes public entrypoints, dynamic loading, and type-only imports.
- Duplicate validation or lenient legacy parsing: trace the data's origin and write regression tests, since identical-looking calls may do different jobs.
- Complexity: the configured ceiling, and a review that any split keeps related logic together. A lower score is not the same as easier code.

These are menu items. Switching a new rule on is a separate decision, and an autofix that would have to judge data origin or public API shape should not be offered.

## Verifying a rule

- Exercise it with the linter's built-in rule tester, then again against the project's real top-level config.
- Fixtures should include renamed imports, re-exports, acceptable code, look-alike APIs from other packages, and near misses.
- A numeric limit needs one case exactly at the limit and one beyond it.
- Code that regular lint skips, such as bundled plugin sources, needs its own check.
