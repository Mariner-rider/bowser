import { mkdirSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const root = process.cwd();
const dist = join(root, "pwa", "dist");

mkdirSync(dist, { recursive: true });

writeFileSync(
  join(dist, "index.html"),
  `<!doctype html>
<html>
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>BrowserOS AI PWA</title>
  </head>
  <body>
    <div id="app">BrowserOS AI PWA build ready.</div>
  </body>
</html>`,
  "utf8",
);

writeFileSync(
  join(dist, "manifest.webmanifest"),
  JSON.stringify(
    {
      name: "BrowserOS AI",
      short_name: "BrowserOSAI",
      start_url: "/",
      display: "standalone",
      background_color: "#0b0f1a",
      theme_color: "#111827",
      icons: []
    },
    null,
    2,
  ),
  "utf8",
);

console.log("[build-pwa] Built PWA artifacts at pwa/dist.");
