# Current Project Structure
_Last updated: 2025-10-19_

- Root files (`LICENSE`, `README.md`) - legal notice and contributor-facing overview.
- `ai_instructions/` - governance for automated agents, including operating rules, complaint log, and structure metadata.
- `docs/` - human-facing documentation that explains features, design decisions, and contributor workflows.
- `resources/` - default character replacement chains and runtime assets shipped with the application.
- `src/` - production code for every runtime surface.
  - `char_switch_logic/` - accent/symbol replacement engines and chain orchestration.
  - `gui/` - user-interface layers for configuring chains, profiles, and preferences.
  - `hotkeys/` - global keyboard listener abstractions and OS-specific hooks.
- `tests/` - pytest suite (currently a placeholder) for unit and regression coverage.
