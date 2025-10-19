# Repository Guidelines

## Project Structure & Module Organization
This repository targets Python 3.13 (see `.venv/`). Place production modules under `src/` and ensure each subpackage exposes a clear `__all__`. Tests belong in `tests/`. Docs belogs to `docs/`.

## Build, Test, and Development Commands
Create a virtual environment with `python -m venv .venv` if not already present, then activate it and install dependencies via `pip install -r requirements.txt` once those manifests exist. Use `python -m pytest` to run the full test suite, and `pytest tests/test_parser.py -k scenario` for targeted checks. Run `python -m build` before publishing to verify packaging metadata.

## Coding Style & Naming Conventions
Follow PEP 8 with 4-space indents and 120-character lines; format code with `ruff format` and lint using `ruff check`. Module names should be lowercase with underscores, classes in PascalCase. Use typehints wherever it is possible and docstrings only when they are really needed for understanding.

## Testing Guidelines
Rely on `pytest` with plain asserts and fixtures in `tests/conftest.py`. New features require unit coverage plus regression cases if fixing bugs. Name tests `test_<unit>_<behavior>` and guard external integrations behind marks such as `@pytest.mark.integration`. Track coverage with `pytest --cov=src --cov-report=term-missing`.

## Commit & Pull Request Guidelines
Commits use present-tense imperatives like “Add parser validation,” mirroring the existing history. Keep changes scoped and include context in the body when touching multiple areas. Pull requests must describe motivation, summarize the solution, link related issues, and provide screenshots or logs when behavior changes. Confirm lint and test commands pass before requesting review.

Each feature or enhancement must be done in a separate branch. Branch naming `feat/feature-description-short` or `bug/bug-description`
