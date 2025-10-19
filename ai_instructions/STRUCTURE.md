# Current Project Structure
_Last updated: 2025-10-19_

- `LICENSE` - repository license information.
- `README.md` - overview and quickstart notes.
- `ai_instructions/` - agent-facing guidelines and logs.
  - `AGENTS.md` - operational rules for agents.
  - `COMPLAINS.md` - complaint log with fixes.
  - `STRUCTURE.md` - this structure reference document.
- `docs/`
  - `CHAR_SWITCH_LOGIC.md` - overview of character switching flow.
- `resources/` - auxiliary assets and reference materials.
- `src/` - production Python packages and entrypoints.
  - `main.py` - primary application bootstrap.
  - `char_switch_logic/`
    - `__init__.py` - exports character switch utilities.
  - `gui/`
    - `__init__.py` - GUI module exports.
  - `hotkeys/`
    - `__init__.py` - hotkey bindings package exports.
- `tests/` - pytest test suite placeholder.
