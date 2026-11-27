# Third-party material

The `visual-explainer` skill is adapted from
[nicobailon/visual-explainer](https://github.com/nicobailon/visual-explainer). Its MIT
license is preserved in `skills/visual-explainer/LICENSE`.

The visual-explainer kit includes Pele 1.6.0, a diagram renderer from
[obsidianmd/pele](https://github.com/obsidianmd/pele). Its bundled file is
`skills/visual-explainer/kit/vendor/pele.mjs`; its MIT license is preserved in
`skills/visual-explainer/kit/vendor/PELE-LICENSE`. The `mermaid-png` skill
installs Pele from npm at run time instead, with the version pinned in its script.

The `librarian` and `update-changelog` skills are adapted from
[mitsuhiko/agent-stuff](https://github.com/mitsuhiko/agent-stuff) under the Apache
License 2.0; a copy is in each skill's `LICENSE` file. `librarian` was edited for this
repository; `update-changelog` is unchanged.

The `prototype` skill and `skills/references/adr-format.md` are adapted from
[mattpocock/skills](https://github.com/mattpocock/skills) under the MIT License, kept
in `skills/prototype/LICENSE`. The `code-review` skill borrows its two-axis structure
from the same repository.

The `recall` skill (`skills/recall/`) was included from the maintainer's own
setup. It has no recorded upstream source and is distributed under this
repository's license. Its session-finder script, `scripts/find-sessions.py`, is bundled and
installed with it.

The `apple-notes` and `apple-reminders` skills credit "Hermes Agent" as author
in their frontmatter and are marked MIT-licensed there.

External skills listed in the README are installed from their own sources and
are not covered by this repository's license. Review each source and its terms
before installing it.
