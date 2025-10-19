# Structure

This document outlines the current layout of the No Switch repository so that future contributors understand what lives where and why.

## Directory Overview

| Path | Role | Notes |
| --- | --- | --- |
| `src/no_switch` | Python package | All importable code and bundled resources. Uses the modern `src/` layout to avoid accidental imports from the repository root. |
| `src/no_switch/chains.py` | Core module | Builds and loads the character replacement chains that power the prototype and upcoming features. |
| `src/no_switch/resources/` | Package resources | JSON chain definitions shipped alongside the package. Keeping resources under the package namespace guarantees availability when the library is installed via `pip`. |
| `src/no_switch/cli/` | Command-line interfaces | Houses CLI commands, including the hotkey listener entry point (`hotkey.py`). |
| `src/no_switch/hotkey/` | Hotkey runtime | Contains the interactive listener (`application.py`) and replacement cycling utilities (`cycler.py`). |
| `docs/` | Documentation | High-level architecture notes (`STACK.md`) and this structure guide—only implementation context needed by human contributors. |
| `ai_management/` | AI operations | AI-facing policies (`AGENTS.md`), complaint tracker, and other process documents for automated contributors. |
| `README.md` | Project brief | Quick-start information for new users. |

## Python Package (`src/no_switch`)

- **Purpose**: Houses the production code that will evolve into the No Switch library.
- **Why resources live here**: Storing JSON assets inside `src/no_switch/resources/` ensures they are shipped as part of the wheel or sdist once packaging metadata is added. External callers can rely on `importlib.resources` (or similar) to access the bundled files without chasing relative paths on disk.
- **Hotkey tooling**: CLI commands live under `src/no_switch/cli/` with the interactive runtime in `src/no_switch/hotkey/`. This split keeps command parsing, reusable cycler logic, and event handling independent so future UIs can reuse the underlying modules.

## Documentation (`docs/`)

- `ai_management/AGENTS.md` captures current agent personas and responsibilities.
- `STACK.md` records the technical stack and reasoning.
- `STRUCTURE.md` (this file) serves as the canonical source of truth for layout decisions. Expand it as new modules, services, or assets appear.

## Growth Checklist

When the codebase grows, consider the following conventions:

1. Place shared resources that must ship with the package under `src/no_switch/<feature>/` so they travel with releases.
2. Add automated tests under a top-level `tests/` directory mirroring the package layout.
3. Record non-package artifacts (design notes, diagrams, ADRs) under `docs/` and reference them from `README.md`.
4. Promote CLI commands to distribution entry points (`console_scripts`) when packaging metadata is introduced.
