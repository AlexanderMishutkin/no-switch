# Structure

This document outlines the current layout of the No Switch repository so that future contributors understand what lives where and why.

## Directory Overview

| Path | Role | Notes |
| --- | --- | --- |
| `src/no_switch` | Python package | All importable code and bundled resources. Uses the modern `src/` layout to avoid accidental imports from the repository root. |
| `src/no_switch/chains.py` | Core module | Builds and loads the character replacement chains that power the prototype and upcoming features. |
| `src/no_switch/data/` | Package resources | JSON chain definitions shipped alongside the package. Keeping data under the package namespace guarantees availability when the library is installed via `pip`. |
| `src/no_switch/poc.py` | Proof of concept | CLI entry point demonstrating how the chain loader and hotkey cycler work together, including diagnostics (`--list-chains`, `--demo`) for offline verification. |
| `docs/` | Documentation | High-level architecture notes (`STACK.md`) and this structure guide—only implementation context needed by human contributors. |
| `ai_management/` | AI operations | AI-facing policies (`AGENTS.md`), complaint tracker, and other process documents for automated contributors. |
| `README.md` | Project brief | Quick-start information for new users. |

## Python Package (`src/no_switch`)

- **Purpose**: Houses the production code that will evolve into the No Switch library.
- **Why data lives here**: Storing JSON assets inside `src/no_switch/data/` ensures they are shipped as part of the wheel or sdist once packaging metadata is added. External callers can rely on `importlib.resources` (or similar) to access the bundled files without chasing relative paths on disk.
- **`poc.py` status**: The file is a proof-of-concept CLI for internal testing, now with non-interactive helpers (`--list-chains`, `--demo`) so contributors can validate the replacement logic without running the hotkey listener. As the project matures, it can graduate into a console script entry point (e.g., via `python -m no_switch.poc` or a `no-switch` command) or move under an `examples/` namespace. For now it remains alongside the package so that it stays in sync with internal APIs.

## Documentation (`docs/`)

- `ai_management/AGENTS.md` captures current agent personas and responsibilities.
- `STACK.md` records the technical stack and reasoning.
- `STRUCTURE.md` (this file) serves as the canonical source of truth for layout decisions. Expand it as new modules, services, or assets appear.

## Growth Checklist

When the codebase grows, consider the following conventions:

1. Place shared resources that must ship with the package under `src/no_switch/<feature>/` so they travel with releases.
2. Add automated tests under a top-level `tests/` directory mirroring the package layout.
3. Record non-package artifacts (design notes, diagrams, ADRs) under `docs/` and reference them from `README.md`.
4. Revisit the placement of `poc.py` once a supported CLI story is defined; promote it to an official entry point or move it to `examples/` or `tools/`.
