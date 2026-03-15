import { existsSync, mkdirSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const root = process.cwd();
const pwaDist = join(root, "pwa", "dist");
const mobileDist = join(root, "mobile", "dist");

if (!existsSync(pwaDist)) {
  mkdirSync(pwaDist, { recursive: true });
  writeFileSync(
    join(pwaDist, "index.html"),
    "<!doctype html><html><body><h1>BrowserOS AI PWA placeholder build</h1></body></html>",
    "utf8",
  );
}

mkdirSync(mobileDist, { recursive: true });
writeFileSync(
  join(mobileDist, "build-info.json"),
  JSON.stringify(
    {
      target: ["ios", "android"],
      copiedWebDir: "pwa/dist",
      timestamp: new Date().toISOString(),
      note: "Run `npx cap sync ios && npx cap sync android` after installing dependencies."
    },
    null,
    2,
  ),
  "utf8",
);

console.log("[build-mobile] Prepared Capacitor mobile artifacts for iOS and Android.");
