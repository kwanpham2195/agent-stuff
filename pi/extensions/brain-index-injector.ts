/**
 * brain-index-injector — if ./brain/index.md exists in cwd, auto-load and
 * inject it into the system prompt on the first turn of every session,
 * and re-inject after compaction.
 *
 * Project-local. Place at .pi/extensions/brain-index-injector.ts.
 */

import { readFileSync, statSync } from "node:fs";
import { join, relative } from "node:path";
import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";

const MAX_CHARS = 20_000;

type Cached = { indexPath: string; body: string };

function loadBrain(cwd: string): Cached | null {
	const indexPath = join(cwd, "brain", "index.md");
	try {
		if (!statSync(indexPath).isFile()) return null;
		let body = readFileSync(indexPath, "utf8");
		if (body.length > MAX_CHARS) {
			body = body.slice(0, MAX_CHARS) + `\n\n…[truncated; full file at ${indexPath}]`;
		}
		return { indexPath, body };
	} catch {
		return null;
	}
}

function buildInjection(body: string): string {
	return (
		`\n\n## Project Memory (brain/index.md)\n\n` +
		`Auto-loaded at session start and after compaction. The brain vault lives at \`./brain/\`. ` +
		`Use the read tool to follow [[wikilinks]] when relevant. ` +
		`Do not re-read this index — it is already in context.\n\n` +
		`${body}\n`
	);
}

export default function (pi: ExtensionAPI) {
	let cached: Cached | null = null;
	let injected = false;

	pi.on("session_start", async (_event, ctx) => {
		cached = loadBrain(ctx.cwd);
		injected = false;
		if (cached) {
			ctx.ui.notify(
				`brain: loaded ${relative(ctx.cwd, cached.indexPath)} (${cached.body.length} chars)`,
				"info",
			);
		}
	});

	pi.on("session_compact", async () => {
		// Compaction rebuilds the system prompt from the base, so our prior
		// injection is gone. Re-arm so the next turn adds it back.
		injected = false;
	});

	pi.on("before_agent_start", async (event) => {
		if (!cached || injected) return;
		injected = true;
		return {
			systemPrompt: event.systemPrompt + buildInjection(cached.body),
		};
	});
}
