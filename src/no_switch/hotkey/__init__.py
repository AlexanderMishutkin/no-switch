"""Hotkey tooling for the No Switch package."""

from .application import HotkeyApplication, keyboard, _IMPORT_ERROR
from .cycler import ReplacementCycler, describe_cycle

__all__ = [
    "HotkeyApplication",
    "ReplacementCycler",
    "describe_cycle",
    "keyboard",
    "_IMPORT_ERROR",
]
