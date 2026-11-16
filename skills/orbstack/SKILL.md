---
name: orbstack
description: Control OrbStack and Docker readiness on macOS. Use to check or start OrbStack, wait for Docker, inspect OrbStack machines, run commands through orb/orbctl, or debug local test failures that depend on Docker or testcontainers.
---

# OrbStack

Prefer `orbctl`; use `orb` as a fallback. Use `orbctl` for OrbStack and machine state (`status`, `start`, `list`, `info`, `logs`, `restart`) and Docker commands for container state.

Docker is ready when `docker info` succeeds. To make it ready, run this from this skill's directory:

```bash
scripts/ensure-docker-ready.sh
```

The script checks `docker info`, starts OrbStack through `orbctl`, `orb`, or `open -a OrbStack`, waits for Docker, and exits non-zero if Docker is still unavailable. Use it in hooks and repeatable workflows.

## Guardrails

- Do not use `orbctl reset` unless the user explicitly asks. It deletes OrbStack Linux and Docker data.
- Do not stop or restart machines unless the user asked or a local test/dev task is blocked by OrbStack state.
- For pre-push or test gates, require Docker readiness, not compose Mongo/LocalStack/Gotenberg readiness, when the repo integration harness uses testcontainers.
