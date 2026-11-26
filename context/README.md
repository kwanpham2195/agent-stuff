# Local context

Keep local context in a private directory outside any public repository. Do not commit workspace records to a shared repository.

Layout:

```text
<context root>/
├── index.md          # registered workspaces and their directory or repository hints
├── templates/        # optional workspace, project, work and research templates
├── scripts/          # optional shared validators and pre-commit checks
└── workspaces/
    └── <workspace-id>/
        ├── index.md  # identity, routing hints, approvals and links
        ├── memory/   # optional reusable project knowledge (plain folder)
        ├── projects/ # optional long-lived goals that group work
        └── work/     # one folder per bounded outcome
```

- The root is its own Git repository. It holds the shared tools: `index.md`, templates, hooks, validators and lint settings.
- Each `workspaces/<id>/` is its own private Git repository, ignored by the root repository. Run Git from the repository that owns the file.
- Workspace memory is a plain `memory/` folder committed with that workspace's records, not a separate repository. Keep `memory/MEMORY.md` a short index that links one topic file per subject.
- Add remotes only when you choose to; nothing here requires one.

To register a new workspace, follow the checklist in [Initialize local context history](../skills/references/work-lifecycle.md#initialize-local-context-history). Read [context routing](../skills/references/context-routing.md) for placement, memory and record rules.
