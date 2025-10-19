"""Argument parsing helpers for No Switch CLI commands."""

from __future__ import annotations

import argparse
from typing import Iterable

from ..chains import DEFAULT_CHAIN_NAMES

HOTKEY_DEFAULT = "<alt>+<shift>+space"
CHAR_STALE_TIMEOUT = 2.5  # seconds

__all__ = ["build_parser", "parse_args", "HOTKEY_DEFAULT", "CHAR_STALE_TIMEOUT"]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Cycle accented characters with a hotkey.")
    parser.add_argument(
        "--hotkey",
        default=HOTKEY_DEFAULT,
        help=f"Hotkey combination in pynput format (default: {HOTKEY_DEFAULT}).",
    )
    parser.add_argument(
        "--chains",
        nargs="+",
        default=list(DEFAULT_CHAIN_NAMES),
        help=f"Replacement chains to load (default: {' '.join(DEFAULT_CHAIN_NAMES)}).",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=CHAR_STALE_TIMEOUT,
        help="Seconds after which the last typed character is considered stale.",
    )
    parser.add_argument(
        "--list-chains",
        action="store_true",
        help="List bundled chain names and exit without starting the listener.",
    )
    parser.add_argument(
        "--demo",
        metavar="CHAR",
        help="Preview the cycle for a single character and exit.",
    )
    return parser


def parse_args(argv: Iterable[str]) -> argparse.Namespace:
    parser = build_parser()
    return parser.parse_args(list(argv))
