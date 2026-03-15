const { contextBridge } = require("electron");

contextBridge.exposeInMainWorld("browserosDesktop", {
  platform: process.platform,
  version: process.versions.electron,
});
