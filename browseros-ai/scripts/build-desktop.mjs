import { mkdirSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const root = process.cwd();
const dist = join(root, "desktop", "dist");
mkdirSync(dist, { recursive: true });

writeFileSync(
  join(dist, "build-info.json"),
  JSON.stringify(
    {
      runtime: "electron",
      entry: "desktop/electron/main.js",
      timestamp: new Date().toISOString(),
      note: "Install electron in host environment and run npm run desktop:dev",
    },
    null,
    2,
  ),
  "utf8",
);

console.log("[build-desktop] Prepared desktop distribution metadata at desktop/dist.");
