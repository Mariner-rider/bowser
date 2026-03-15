# Installation

## Requirements

- Python 3.11+
- Node.js 20+

## Setup

```bash
npm install
```

## Build artifacts

```bash
npm run build-pwa
npm run build-mobile
```

## Optional quick Python validation

```bash
python -m compileall agents automation learning llm memory interface local_ai core
```

## End-to-end local run

```bash
python scripts/run-e2e.py
```

This runs the clean-room local runtime and does not require cloning any external BrowserOS repository.
