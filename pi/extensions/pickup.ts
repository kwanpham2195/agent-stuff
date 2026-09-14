/**
 * Pickup extension - resume a saved handoff from ~/.pi/handoffs/
 *
 * Usage:
 *   /pickup          - pick from available handoffs
 *   /pickup <query>  - filter handoffs by name
 */

import { readdir, readFile, unlink } from "node:fs/promises";
import { join } from "node:path";
import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";
import { DynamicBorder } from "@earendil-works/pi-coding-agent";
import { Container, type SelectItem, SelectList, Spacer, Text } from "@earendil-works/pi-tui";

const HANDOFF_DIR = join(process.env.HOME ?? "~", ".pi", "handoffs");

interface HandoffEntry {
  file: string;
  date: string;
  time: string;
  slug: string;
  preview: string;
  content: string;
}

async function loadHandoffs(query?: string): Promise<HandoffEntry[]> {
  let files: string[];
  try {
    files = (await readdir(HANDOFF_DIR))
      .filter((f) => f.endsWith(".md"))
      .sort()
      .reverse(); // newest first
  } catch {
    return [];
  }

  if (query) {
    files = files.filter((f) => f.toLowerCase().includes(query));
  }

  const entries: HandoffEntry[] = [];
  for (const file of files) {
    const content = await readFile(join(HANDOFF_DIR, file), "utf-8");
    const name = file.replace(/\.md$/, "");
    const tsMatch = name.match(/^(\d{4}-\d{2}-\d{2})T(\d{2}-\d{2}-\d{2})-(.+)$/);

    // First non-empty, non-heading line as preview
    const previewLine = content
      .split("\n")
      .map((l) => l.trim())
      .find((l) => l && !l.startsWith("#")) ?? "";

    entries.push({
      file,
      date: tsMatch?.[1] ?? name.slice(0, 10),
      time: tsMatch?.[2]?.replace(/-/g, ":") ?? "",
      slug: tsMatch?.[3]?.replace(/-/g, " ") ?? name,
      preview: previewLine.length > 80 ? previewLine.slice(0, 77) + "..." : previewLine,
      content,
    });
  }
  return entries;
}

export default function (pi: ExtensionAPI) {
  pi.registerCommand("pickup", {
    description: "Pick up a saved handoff",
    handler: async (args, ctx) => {
      if (!ctx.hasUI) {
        ctx.ui.notify("pickup requires interactive mode", "error");
        return;
      }

      const query = args.trim().toLowerCase() || undefined;
      const handoffs = await loadHandoffs(query);

      if (handoffs.length === 0) {
        const msg = query
          ? `No handoffs matching "${args.trim()}"`
          : "No handoffs found. Use /handoff to create one.";
        ctx.ui.notify(msg, "info");
        return;
      }

      // Build SelectList items
      const items: SelectItem[] = handoffs.map((h) => ({
        value: h.file,
        label: `${h.date} ${h.time}  ${h.slug}`,
        description: h.preview,
      }));

      // Show TUI picker
      const selectedFile = await ctx.ui.custom<string | null>((tui, theme, _kb, done) => {
        const container = new Container();

        // Top border
        container.addChild(new DynamicBorder((s: string) => theme.fg("accent", s)));

        // Title + count
        const title = theme.fg("accent", theme.bold("Handoffs"));
        const count = theme.fg("muted", ` (${handoffs.length})`);
        container.addChild(new Text(`${title}${count}`, 1, 0));

        container.addChild(new Spacer(1));

        // SelectList
        const selectList = new SelectList(items, Math.min(items.length, 12), {
          selectedPrefix: (t: string) => theme.fg("accent", t),
          selectedText: (t: string) => theme.fg("accent", t),
          description: (t: string) => theme.fg("muted", t),
          scrollInfo: (t: string) => theme.fg("dim", t),
          noMatch: (t: string) => theme.fg("warning", t),
        });
        selectList.onSelect = (item) => done(item.value);
        selectList.onCancel = () => done(null);
        container.addChild(selectList);

        container.addChild(new Spacer(1));

        // Help text
        container.addChild(
          new Text(theme.fg("dim", "↑↓ navigate • enter select • type to filter • esc cancel"), 1, 0),
        );

        // Bottom border
        container.addChild(new DynamicBorder((s: string) => theme.fg("accent", s)));

        return {
          render: (w: number) => container.render(w),
          invalidate: () => container.invalidate(),
          handleInput: (data: string) => {
            selectList.handleInput(data);
            tui.requestRender();
          },
        };
      });

      if (!selectedFile) {
        ctx.ui.notify("Cancelled", "info");
        return;
      }

      const handoff = handoffs.find((h) => h.file === selectedFile)!;

      // Preview in editor for optional edits
      const editedPrompt = await ctx.ui.editor("Review handoff", handoff.content);

      if (editedPrompt === undefined) {
        ctx.ui.notify("Cancelled", "info");
        return;
      }

      // Action picker — also a proper TUI
      const actionItems: SelectItem[] = [
        { value: "submit", label: "Submit in this session", description: "Load into editor and submit" },
        { value: "new-session", label: "Open in new session", description: "Create a fresh session with this handoff" },
        { value: "clipboard", label: "Copy to clipboard", description: "Copy prompt for use anywhere" },
        { value: "delete", label: "Delete handoff", description: `Remove ${handoff.file}` },
      ];

      const action = await ctx.ui.custom<string | null>((tui, theme, _kb, done) => {
        const container = new Container();

        container.addChild(new DynamicBorder((s: string) => theme.fg("accent", s)));
        container.addChild(new Text(theme.fg("accent", theme.bold("What next?")), 1, 0));
        container.addChild(new Spacer(1));

        const selectList = new SelectList(actionItems, actionItems.length, {
          selectedPrefix: (t: string) => theme.fg("accent", t),
          selectedText: (t: string) => theme.fg("accent", t),
          description: (t: string) => theme.fg("muted", t),
          scrollInfo: (t: string) => theme.fg("dim", t),
          noMatch: (t: string) => theme.fg("warning", t),
        });
        selectList.onSelect = (item) => done(item.value);
        selectList.onCancel = () => done(null);
        container.addChild(selectList);

        container.addChild(new Spacer(1));
        container.addChild(new Text(theme.fg("dim", "↑↓ navigate • enter select • esc cancel"), 1, 0));
        container.addChild(new DynamicBorder((s: string) => theme.fg("accent", s)));

        return {
          render: (w: number) => container.render(w),
          invalidate: () => container.invalidate(),
          handleInput: (data: string) => {
            selectList.handleInput(data);
            tui.requestRender();
          },
        };
      });

      if (!action) {
        ctx.ui.notify("Cancelled", "info");
        return;
      }

      if (action === "delete") {
        const ok = await ctx.ui.confirm("Delete?", `Delete ${handoff.file}?`);
        if (ok) {
          await unlink(join(HANDOFF_DIR, handoff.file));
          ctx.ui.notify(`Deleted ${handoff.file}`, "info");
        }
        return;
      }

      if (action === "clipboard") {
        const { execSync } = await import("node:child_process");
        execSync("pbcopy", { input: editedPrompt });
        ctx.ui.notify("Copied to clipboard", "info");
        return;
      }

      if (action === "submit") {
        ctx.ui.setEditorText(editedPrompt);
        ctx.ui.notify("Handoff loaded into editor. Submit when ready.", "info");
        return;
      }

      if (action === "new-session") {
        const currentSessionFile = ctx.sessionManager.getSessionFile();
        const result = await ctx.newSession({
          parentSession: currentSessionFile,
          withSession: async (replacementCtx) => {
            replacementCtx.ui.setEditorText(editedPrompt);
            replacementCtx.ui.notify("Handoff ready. Submit when ready.", "info");
          },
        });
        if (result.cancelled) {
          ctx.ui.notify("New session cancelled", "info");
        }
      }
    },
  });
}
