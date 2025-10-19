# No Switch

No Switch turns quick key combos into multilingual magic. Swap plain characters for accented or symbolic versions without leaving the keyboard.

## Quick Example
1. Type `U` in any application.
2. Tap your personal "Accent" hotkey (for example `Alt+Shift+U`).
3. No Switch immediately replaces the last character with `Ü`. Keep tapping to cycle `Ü → Ù → Ū → U`, or stop when the variant you need appears.

The same hotkey works on a single highlighted character, so you can fix typos without retyping.

## Why You’ll Love It
- Hotkey-triggered character replacement for the last typed glyph or a one-character selection.
- Custom replacement chains that cycle through your go-to accents or symbols.
- Optional smart fallbacks that loop back to the original character.
- Lightweight background listener that wakes only when a configured hotkey fires.
- Profiles for different languages or workflows, plus an easy-to-sync settings file.

## Getting Started
- **Activate the environment:** `source /home/ubuntu/.virtualenvs/no-switch/bin/activate` (WSL shared venv).
- **Install project deps:** `python -m pip install -r requirements.txt` (currently minimal).
- **Run tests:** `python -m unittest discover -s tests`.
- **Try the UI:** Launch the app entry point under `src/` (coming soon) to manage hotkeys, replacement chains, and profile toggles.

## Build Targets
We aim to ship native packages for every major desktop platform while keeping a "clone and run" option for contributors.

- **Windows:** PyInstaller/Briefcase build for `.exe` + optional installer.
- **macOS:** Hardened runtime `.app` bundle with notarization support.
- **Linux:** AppImage plus a simple executable for package managers.

Detailed build scripts will live in `docs/` as they solidify.

## Development Docs
- Feature walkthroughs and design notes: see files under `docs/`.
- Character replacement flow: [`docs/CHAR_SWITCH_LOGIC.md`](docs/CHAR_SWITCH_LOGIC.md)
- Packaging and contributor guides will land in `docs/` as they mature.

## Project Layout
```
src/           Application source code
tests/         Unittest-based unit and regression suites
docs/          Additional documentation
```

## Roadmap
- [ ] Define core event hook abstraction for keyboard listeners per operating system.
- [ ] Establish configuration schema and validation.
- [ ] Build proof-of-concept UI with a single hotkey and replacement chain.
- [ ] Integrate packaging scripts for Windows/macOS/Linux.
- [ ] Add regression tests for replacement logic and configuration persistence.

## Star History
[![Star History Chart](https://api.star-history.com/svg?repos=pyth/no-switch&type=Date)](https://star-history.com/#pyth/no-switch&Date)

## Contributing
- Branch from `main` using `feat/<short-name>` or `bug/<short-name>`.
- Keep commits in present-tense imperative voice.
- Run `ruff format`, `ruff check`, and `python -m unittest discover -s tests` before opening a PR.
- Document UI changes with screenshots or GIFs.

## License
Released under the [MIT License](LICENSE).
