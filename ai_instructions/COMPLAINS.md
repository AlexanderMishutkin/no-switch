| Date | Complaint | Fix |
| --- | --- | --- |
| 2025-10-19 | `ai_instructions/STRUCTURE.md` listed paths without descriptions, reducing usefulness. | Added descriptions for every entry and updated `ai_instructions/AGENTS.md` to require descriptive structure updates. |
| 2025-10-19 | `README.md` directed human contributors to `ai_instructions/AGENTS.md`. | Replaced the reference with pointers to human-facing docs under `docs/`. |
| 2025-10-19 | `ai_instructions/STRUCTURE.md` described individual files instead of directory responsibilities. | Rewrote the document to focus on directory-level functionality and clarified the expectation in `ai_instructions/AGENTS.md`. |
| 2025-10-19 | `ai_instructions/STRUCTURE.md` omitted subdirectory coverage, weakening navigational value. | Expanded the overview to include key subdirectories (e.g., `src/char_switch_logic/`, `src/gui/`, `src/hotkeys/`) and updated `ai_instructions/AGENTS.md` to require it. |
| 2025-10-19 | Missing `requirements.txt` prevented dependency installation and tests were not executed. | Added `requirements.txt` with full dependency list, removed extra manifest, and updated `ai_instructions/AGENTS.md` to forbid excuses—only fixes. |
