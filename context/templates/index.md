# Local context

Workspaces are the sole context and work ownership boundary. Routing uses this directory and each
workspace index; paths are hints and repository identities are supporting evidence. Unknown,
overlapping, or uncertain mappings require a question rather than silent registration or merging.
Small work stays inline.

## Registered workspaces

Add one link per registered workspace:

```md
- [workspace-name](workspaces/workspace-id/index.md) - directory hint: `$HOME/path/to/workspace`; repository identity: `github.com/owner/repository`
```
