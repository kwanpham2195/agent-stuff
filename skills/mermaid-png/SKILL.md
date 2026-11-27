---
name: mermaid-png
description: "Render Mermaid diagrams to PNG images instead of showing Mermaid text. Use whenever a reply, review file, artifact, doc, issue or PR would include a diagram written in Mermaid."
---

# Mermaid to PNG

Never show Mermaid text to a reader. This covers chat, T3 threads, `review/` folders, saved artifacts, repository docs, issues and PR descriptions. A reader sees a picture, not a ` ```mermaid ` block.

## Render

Write the Mermaid source to a `.mmd` file, then run:

```sh
mermaid-png diagram.mmd              # writes and prints diagram.png
mermaid-png diagram.mmd out/flow.png # choose the output path
```

If `mermaid-png` is not on PATH, run `scripts/mermaid-png` from this skill's folder.

The script draws the diagram with [Pele](https://pele.run), a Mermaid renderer that needs no browser, and turns the SVG into a PNG with `rsvg-convert` at 2x on a white background. It supports every diagram type in Mermaid 12.1.0. The first run installs a pinned Pele into `~/.cache/mermaid-png/`, so it needs `npm` and network once.

Open the PNG and look at it before you show it. Fix clipped labels, crossed lines or a cramped layout in the source, then render again.

## Place the image

| Surface | Where the files go | How to show it |
| --- | --- | --- |
| Chat and T3 threads | The work's context folder, or a new `/tmp` folder when there is none | Markdown image with the PNG's absolute path |
| `review/` folders and other saved Markdown | An `assets/` folder beside the document, with the `.mmd` source | Markdown image with a relative path |
| Repository docs | Beside the doc, with the `.mmd` source committed so others can edit it | Markdown image with a relative path |
| PR descriptions and comments | A local file only | Upload it with `gh pr edit --attach` or `gh pr comment --attach`, as the `before-and-after` skill does |

HTML artifacts from `visual-explainer` are exempt. Its kit draws Mermaid as SVG inside the page, so the reader never sees the text.

## When it fails

- **Parse error:** the script exits 1 and prints Pele's message with the line. Fix the source and render again.
- **`rsvg-convert` not found:** run `brew install librsvg`.
- **Black shapes in the PNG:** the script warns when the SVG still uses `var()`, `color-mix()` or `<style>`. `rsvg-convert` ignores these, so a newer Pele feature slipped past `scripts/mermaid-png.mjs`. Extend the resolver there.
- **Still failing:** use a plain-text view from [show-me](../show-me/SKILL.md), such as a call tree, a file tree or a diff, and say that the diagram was not rendered. Never fall back to Mermaid text.

## Update Pele

Change `pele_version` in `scripts/mermaid-png`. Render a few diagram types (flowchart, sequence, state, class, ER, pie, Gantt) and look at each PNG before you commit.
