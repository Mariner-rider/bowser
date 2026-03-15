# Developer Guide

## Branch workflow

- `main`: stable production
- `develop`: integration branch
- `feature/*`: feature development (`feature/agent-system`, `feature/local-ai`, etc.)

## CI/CD baseline

- Lint code
- Run tests
- Build browser artifacts
- Publish preview/deployable bundle

A starter workflow should be placed in `.github/workflows/ci.yml` in the host repository.

## Security checklist

- Sandbox automation actions before execution
- Enforce capability/permission checks at the kernel boundary
- Avoid storing plaintext API keys
- Isolate wallet identity and signing flows from general agent runtime
