# AI Code Complaints Log

Status legend: **Open** = fix pending; **Resolved** = verified fix delivered.

| ID | Complaint | Raised By | Status | Resolution |
| --- | --- | --- | --- | --- |
| C1 | “Why data is placed in SRC!?” | User | Resolved | Documented the packaging rationale in `docs/STRUCTURE.md` explaining why bundled JSON lives under `src/no_switch/data/`. |
| C2 | “What the file structure with poc.py?!??! It's not serious enough.” | User | Resolved | Replaced the monolithic `poc.py` with dedicated modules under `src/no_switch/cli/` and `src/no_switch/hotkey/`, and documented the new layout. |
| C3 | “Make document in DOCS describing project structure and keep it professional.” | User | Resolved | Authored `docs/STRUCTURE.md` with a formal directory overview and growth checklist. |
| C4 | “Why project structure not structure?” | User | Resolved | Renamed the guide to `STRUCTURE.md` and updated the title to `Structure` for concise naming. |
| C5 | “Modify your agents.md stating to be non too verbose and consistent.” | User | Resolved | Added a “Communication Principles” section to `ai_management/AGENTS.md` emphasizing concise, consistent messaging. |
| C6 | “Why the heck some readme files are lowercase and other upper case?” | User | Resolved | Normalized documentation naming by renaming `docs/stack.md` to `docs/STACK.md` and aligning references. |
| C7 | “Again - when I do complain - you fix it.” | User | Resolved | Codified the expectation in `ai_management/AGENTS.md` within the Communication Principles section. |
| C8 | “You don't get it. Mark complains as unfixed and fix them!” | User | Resolved | Documented the open→resolved workflow at the top of this log and followed it while implementing the latest fixes. |
| C9 | “Split ai_management from docs and put complains and other documents meant for you in that folder.” | User | Resolved | Created the `ai_management/` directory, moved AI policies and complaints there, and updated `README.md` plus `docs/STRUCTURE.md` references. |
| C10 | “After splitting docs - go really fixing problems with your POC.” | User | Resolved | Added CLI diagnostics (`--list-chains`, `--demo`), better chain validation, and regression tests in `tests/test_hotkey_cli.py`. |
| C11 | “Why all the code is in single file named awfully poc.py? Fix it instead of explaining.” | User | Resolved | Replaced `src/no_switch/poc.py` with structured modules (`cli`, `hotkey`) and added package entry points. |
