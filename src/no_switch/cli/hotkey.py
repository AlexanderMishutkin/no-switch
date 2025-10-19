"""Command-line entry point for the No Switch hotkey listener."""

from __future__ import annotations

import sys
from typing import Iterable

from ..data import list_available_chains
from ..hotkey import HotkeyApplication, ReplacementCycler, describe_cycle, _IMPORT_ERROR, keyboard
from .arguments import parse_args

__all__ = ["main"]


def _require_keyboard() -> None:
    if keyboard is None:
        message = "pynput is required for this command. Install it with 'pip install pynput'."
        raise SystemExit(f"{message}\n\nImport error: {_IMPORT_ERROR}")


def run_command(argv: Iterable[str]) -> int:
    args = parse_args(argv)
    if args.list_chains:
        for name in list_available_chains():
            print(name)
        return 0

    try:
        cycler = ReplacementCycler.from_chain_names(args.chains)
    except ValueError as exc:
        print(exc)
        return 2

    if args.demo is not None:
        try:
            report = describe_cycle(cycler, args.demo)
        except ValueError as exc:
            print(exc)
            return 2

        if not report:
            print(f"No chain defined for '{args.demo}'.")
            return 1
        print(report)
        return 0

    _require_keyboard()
    app = HotkeyApplication(args.hotkey, args.chains, args.timeout, cycler=cycler)
    app.run()
    return 0


def main(argv: Iterable[str] | None = None) -> int:
    return run_command(argv or sys.argv[1:])


if __name__ == "__main__":
    raise SystemExit(main())
