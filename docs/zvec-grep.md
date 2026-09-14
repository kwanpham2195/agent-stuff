# Set up zvec-grep

This setup uses [zvec-grep](https://github.com/zvec-ai/zvec-grep) for indexed lexical and semantic search over local workspaces. The `zg` CLI and the `zvec_grep_search` MCP tool use the same local index.

## Install

zvec-grep requires Node.js 22 or newer.

```bash
npm install --global @zvec/zvec-grep
zg --version
```

Add its repository-local state to your Git ignore rules:

```gitignore
.zvec-grep/
```

## Create an index

Indexing writes `.zvec-grep/` under the workspace root and may download a local embedding model. Run it only for a workspace you intend to index:

```bash
cd /path/to/workspace
zg index
zg status
```

The default local embedding model keeps indexed file content on the machine. Remote embedding providers require a separate authorization grant and may receive query text or workspace content. Do not run `zg auth grant` until you have reviewed that provider and approved the workspace.

Use direct search from the shell:

```bash
zg "where theme preferences are restored"
zg --rg -F "loadTheme" src
```

Use `zg` when wording or location is unknown or when evidence spans files. Use `rg`, native grep, or `zg --rg` for exact strings, filenames, paths, and exhaustive matches.

## Connect Pi through MCP

The Pi integration in this repository uses the `pi-mcp-adapter` package and the local HTTP endpoint in `pi/mcp.example.json`. zvec-grep's own guided installer does not currently list Pi as a target.

Start the local server:

```bash
zg --server on
zg --server status --check-ready
```

Install the Pi setup and review the examples:

```bash
./scripts/install --pi
```

If you want both example MCP servers, activate the file:

```bash
cp "$HOME/.pi/agent/mcp.example.json" "$HOME/.pi/agent/mcp.json"
```

If you want only zvec-grep, create `~/.pi/agent/mcp.json` with:

```json
{
  "mcpServers": {
    "zvec-grep": {
      "url": "http://127.0.0.1:7999/mcp",
      "lifecycle": "lazy",
      "toolPrefix": "none",
      "includeTools": ["zvec_grep_search"],
      "directTools": ["zvec_grep_search"]
    }
  }
}
```

Restart Pi or open a new session. Confirm that `zvec_grep_search` is available. Every MCP request must pass the absolute workspace root that the local daemon can read.

## Operate the server

```bash
zg --server status
zg --server off
zg --server on
```

The default server listens only on `127.0.0.1:7999`. It exposes the search tool through the default `agent` toolset. Administrative index tools require the optional `full` toolset and are not needed by this setup.

A result marked `possibly_stale` can still be used when its evidence is sufficient. Use a refresh that waits only when the answer depends on files changed since the last index update:

```bash
zg query --refresh wait "recent configuration change"
```

## Remove

Stop the server and remove the package:

```bash
zg --server off
npm uninstall --global @zvec/zvec-grep
```

Remove the `zvec-grep` entry from `~/.pi/agent/mcp.json`. Indexes remain under each workspace's `.zvec-grep/` directory until you deliberately remove them.
