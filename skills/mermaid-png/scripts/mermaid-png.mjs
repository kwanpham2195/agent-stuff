// Draw a Mermaid file as an SVG that rsvg-convert can rasterize.
// Usage: node mermaid-png.mjs <pele.js> <input.mmd> <output.svg>
//
// Pele colors every shape with CSS custom properties (var(--pele-*)), which rsvg-convert ignores,
// so shapes come out black. Replace each var() with its value before writing the SVG.
import { readFileSync, writeFileSync } from "node:fs";
import { pathToFileURL } from "node:url";

const [pelePath, input, output] = process.argv.slice(2);
const { render, PeleError } = await import(pathToFileURL(pelePath).href);

// Pele's defaults reject large charts; these are sized for large diagrams.
const options = { fontSize: 16, limit: 1_000_000, outputLimit: 8_000_000, maxEdges: 10_000 };
const theme = { "--pele-font": "Helvetica, Arial, sans-serif", "--pele-font-mono": "Menlo, monospace" };

let svg;
try {
  ({ svg } = render(readFileSync(input, "utf8"), options));
} catch (e) {
  if (!(e instanceof PeleError)) throw e;
  console.error(`mermaid-png: ${input}: ${e.message}`);
  process.exit(1);
}

// A value may hold one level of nested parentheses, such as var(--pele-bg,#fff).
const value = String.raw`(?:[^;"()]|\([^()]*(?:\([^()]*\))?[^()]*\))+`;
const props = { ...theme };
for (const [, name, v] of svg.matchAll(new RegExp(String.raw`(--[\w-]+)\s*:\s*(${value})`, "g"))) {
  if (!(name in props)) props[name] = v.trim();
}
const varCall = /var\(\s*(--[\w-]+)\s*(?:,\s*([^()]*(?:\([^()]*\))?[^()]*))?\)/g;
const resolve = (s) => {
  for (let prev; prev !== s; ) {
    prev = s;
    s = s.replace(varCall, (_, name, fallback) => props[name] ?? (fallback ?? "").trim());
  }
  return s;
};
for (const name of Object.keys(props)) props[name] = resolve(props[name]);
svg = resolve(svg);

const left = svg.match(/var\(|color-mix\(|<style/);
if (left) console.error(`mermaid-png: ${input}: SVG still uses ${left[0]}; check the PNG for black shapes`);
writeFileSync(output, svg);
