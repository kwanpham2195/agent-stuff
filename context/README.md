# Local context

Keep local context under `~/.agents/context/`. Do not commit workspace records by default.

Start with:

```text
~/.agents/context/
├── index.md
├── templates/
└── workspaces/
```

The root `index.md` lists registered workspaces and their directory or repository identity hints. Each workspace owns its work records and reusable knowledge. Read `../skills/references/context-routing.md` for placement rules.
