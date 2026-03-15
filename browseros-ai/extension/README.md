# BrowserOS AI Extension

Cross-browser extension scaffold for Chrome/Edge/Brave/Opera/Firefox-compatible builds.

## Load unpacked
1. Run `npm run build-extension`
2. Open browser extension developer mode.
3. Load `extension/dist` as unpacked extension.

## Features
- Popup launcher for BrowserOS AI web dashboard.
- Background service worker for command forwarding events.
- Content-script bridge for page metadata capture (non-invasive).
