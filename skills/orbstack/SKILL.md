---
name: orbstack
description: Control OrbStack and Docker readiness on macOS. Use when Codex needs to check whether OrbStack is running, start OrbStack, wait for Docker to become available, inspect OrbStack machines, run commands through orb/orbctl, or debug local test failures that depend on Docker, containers, or testcontainers.
---

# OrbStack

## Quick Start

Prefer `orbctl` when installed. Use `orb` as a fallback. Use Docker commands only for container state.

Check status:

```bash
orbctl status
docker info
```

Make Docker ready:

```bash
"$HOME/.codex/skills/orbstack/scripts/ensure-docker-ready.sh"
```

## Workflow

1. Check command availability:

```bash
command -v orbctl || command -v orb || true
```

2. Check OrbStack:

```bash
orbctl status
```

3. If OrbStack is stopped, start it:

```bash
orbctl start
```

4. Wait for Docker, because testcontainers and `docker compose` need Docker:

```bash
docker info
```

5. For machine-level work, use OrbStack commands:

```bash
orbctl list
orbctl info <machine>
orbctl logs <machine>
orbctl restart <machine>
```

6. For container-level work, use Docker commands:

```bash
docker ps
docker logs <container>
docker compose ps
```

## Guardrails

- Do not use `orbctl reset` unless the user explicitly asks. It deletes OrbStack Linux and Docker data.
- Do not stop or restart machines unless the user asked or a local test/dev task is blocked by OrbStack state.
- For pre-push or test gates, require Docker readiness, not compose Mongo/LocalStack/Gotenberg readiness, when the repo integration harness uses testcontainers.
- If `orbctl` and `orb` are missing, fall back to `open -a OrbStack`, then wait for `docker info`.

## Script

Use `scripts/ensure-docker-ready.sh` in hooks and repeatable workflows. It:

- checks `docker info`;
- starts OrbStack through `orbctl`, `orb`, or the app;
- waits until Docker is available;
- exits non-zero if Docker is still unavailable.
