# Writing release notes

Rules for writing release notes for a versioned software project: what to cover, how to sort changes, and how to lay the notes out.

**Prerequisite**: Read [Writing reviewable artifacts](writing.md) first. It sets the shared writing standards. This guide adds what is specific to release notes.

## Editorial choices

### What to cover

Write for someone deciding whether to upgrade. Include a change when it affects that decision or their code:

- Breaking changes that need action from the user.
- New features that remove a common pain point.
- New public APIs that make something possible that was not before.
- Changes to how people integrate or deploy the product.
- Fixes for bugs that users reported.

### What to leave out

- Performance work that nobody can observe.
- Fixes for bugs that were introduced and fixed within the same release cycle.
- Internal details that do not touch the public API.
- Cleanups that change code quality but not behavior.

### When a change gets its own featured section

Give a change a subsection under "What's new" when any of these is true:

- It breaks existing code and needs a migration guide.
- It adds a major capability.
- It is a notable feature, even if several pull requests built it.
- Readers need detailed guidance, such as upgrade steps or a compatibility table.

A featured section should contain:

- What changed and why a reader should care.
- Code samples where they help.
- For breaking changes, a migration guide inside a collapsible `<details>` block.
- Links to the relevant documentation.

## Sorting pull requests

| Category     | Typical labels                  | Signals                                      |
| ------------ | ------------------------------- | -------------------------------------------- |
| API changes  | `api`, `feature`, `major`       | Adds, removes, or alters something public    |
| Improvements | `improvement`, `enhancement`    | Makes an existing capability better          |
| Bug fixes    | `bugfix`, `bug`                 | Corrects wrong behavior                      |

Check each change description for a release-note section or an API-change section. Search for "breaking" to find breaking changes and for "deprecat" to find deprecations. If the project has its own markers for either, use them.

### Changes to skip

Skip any change carrying a label that the project treats as non-release work. Typical cases:

- Internal maintenance
- Docs-only changes
- Test-only changes
- Changes marked to be left out of release notes

Also skip:

- Reverts, unless the revert fixes something users can see.
- Fixes for bugs from the same release cycle, unless users can see the fix and it deserves a mention.

If a change is reverted and its entry is still in the unreleased notes, delete that entry.

Credit outside contributors like this:

```markdown
Thanks to [@username](https://github.com/username) for the contribution.
```

## Ground rules

- Never mention AI authorship.
- Write in the past tense, as if the release has shipped.
- Drop any section that has no entries.
- Keep the release index or changelog listing in step with the project's release process.

---

## Layout

### Section order

Use these sections, in this order, and leave out the empty ones:

1. **Intro paragraph.** One or two sentences on the highlights.
2. **What's new** (`## What's new`). One H3 per headline feature or breaking change.
3. **API changes** (`## API changes`). New or changed methods, properties, and options, plus deprecations and breaking changes.
4. **Improvements** (`## Improvements`). Upgrades to existing behavior.
5. **Bug fixes** (`## Bug fixes`). Corrected problems.
6. **Patch releases** (`## Patch releases`). Follows a `---` rule. One bulleted list per patch version.

### Intro paragraph

Summarize the release in one or two sentences. Name the user-facing features first, then mention infrastructure and performance work.

```markdown
This release adds a plugin system for custom exporters, a new SQLite option for the job queue, and a rewritten config loader. It also includes smaller API improvements, speedups, and bug fixes.
```

### Entry format

Begin each entry with a verb such as "Add", "Fix", "Improve", or "Remove". Be brief, but say enough that a reader knows what changed. End with the pull request link.

```markdown
- Add `client.retry()` to resend a failed request. ([#123](https://github.com/example/app/pull/123))
```

If several pull requests contributed:

```markdown
- Speed up config loading. ([#131](https://github.com/example/app/pull/131), [#135](https://github.com/example/app/pull/135))
```

If a sample helps:

````markdown
- Add `persistedValue()` for values that survive a restart. ([#140](https://github.com/example/app/pull/140))

  ```ts
  const theme = persistedValue('theme', 'light')
  ```
````

### Breaking changes and deprecations

Prefix a breaking change with 💥. Prefix a deprecation with 🔜. A deprecated API still works but will go away later. In "API changes", list breaking changes first, then deprecations, then everything else:

```markdown
## API changes

- 💥 **`Plugin.load()`** now takes an options object instead of a path. ([#150](https://github.com/example/app/pull/150))
- 💥 **`oldName`** is now `newName`. ([#152](https://github.com/example/app/pull/152))
- 🔜 **`client.send()`** is deprecated. Use `client.request()` instead. ([#155](https://github.com/example/app/pull/155))
- Add `client.request()` for sending typed requests. ([#120](https://github.com/example/app/pull/120))
```

### The What's new section

Each H3 under `## What's new` covers a headline feature or a major breaking change.

Simple form:

```markdown
## What's new

### Feature name ([#160](https://github.com/example/app/pull/160))

One short paragraph on what the feature does and why it matters.
```

With several pull requests:

```markdown
### Pluggable job queue ([#160](https://github.com/example/app/pull/160), [#162](https://github.com/example/app/pull/162))
```

A deprecation gets 🔜 in its heading:

```markdown
### 🔜 Old config format is deprecated ([#170](https://github.com/example/app/pull/170))

What is deprecated and what to use instead.
```

A breaking change gets 💥 in its heading plus a migration guide:

````markdown
### 💥 Feature name ([#180](https://github.com/example/app/pull/180))

What the change does and why it matters.

<details>
<summary>How to migrate</summary>

Before:

```ts
// old code
```

After:

```ts
// new code
```

</details>
````

Use a collapsible block for background that not every reader needs:

```markdown
<details>
<summary>Why use a database file?</summary>

- **Durable by default**: jobs survive a restart.
- **Smaller footprint**: the queue does not have to sit in memory.

</details>
```

Use one for compatibility tables:

```markdown
<details>
<summary>Supported platforms</summary>

| Platform | Adapter         | Package          |
| -------- | --------------- | ---------------- |
| Node.js  | `NodeAdapter`   | `better-sqlite3` |
| Bun      | `BunAdapter`    | built in         |

</details>
```

### Release link

Close each release section with a link to the project's release page or changelog.

- For a grouped release, put it after the last content section and before the next `---`.
- For a patch release, put it after that patch's bullet list.

```markdown
[View release on GitHub](https://github.com/example/app/releases/tag/v2.4.0)
```

### Patch releases

Put patch releases at the bottom of the grouped release file, under a horizontal rule, oldest first:

```markdown
---

## Patch releases

### v2.3.1

- Fix a crash when the config file is empty. ([#190](https://github.com/example/app/pull/190))

[View release on GitHub](https://github.com/example/app/releases/tag/v2.3.1)

### v2.3.2

- Fix retries ignoring the timeout setting. ([#195](https://github.com/example/app/pull/195))

[View release on GitHub](https://github.com/example/app/releases/tag/v2.3.2)
```

### Horizontal rules

The only place for `---` is directly before `## Patch releases`.

### Headings

Use sentence case: "API changes", not "API Changes".

### Frontmatter

```yaml
---
title: 'v2.4.0'
created_at: 03/14/2025
updated_at: 03/14/2025
keywords:
  - changelog
  - release
  - v2.4
  - v2.4.0
  - v2.4.1
  - topic-keyword
---
```

- Write dates as MM/DD/YYYY.
- Always list `changelog` and `release` as keywords.
- Add the minor version without a patch number (`v2.4`), the `.0` release, and every patch version.
- Then add two to five keywords about the content, in lowercase with hyphens between words.
