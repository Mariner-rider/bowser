import { cpSync, mkdirSync } from "node:fs";
import { join } from "node:path";

const root = process.cwd();
const src = join(root, "extension");
const dist = join(root, "extension", "dist");

mkdirSync(dist, { recursive: true });
cpSync(join(src, "manifest.json"), join(dist, "manifest.json"));
cpSync(join(src, "src", "background.js"), join(dist, "background.js"));
cpSync(join(src, "src", "content.js"), join(dist, "content.js"));
cpSync(join(src, "src", "popup.html"), join(dist, "popup.html"));
cpSync(join(src, "src", "popup.js"), join(dist, "popup.js"));

console.log("[build-extension] Built extension artifacts at extension/dist.");
