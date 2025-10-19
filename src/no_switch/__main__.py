"""Entry point for ``python -m no_switch``."""

from __future__ import annotations

from .cli.hotkey import main


if __name__ == "__main__":
    raise SystemExit(main())
