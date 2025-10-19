"""Proof-of-concept hotkey cycler for No Switch.

This script listens for a configurable hotkey (default: ``Alt+Shift+Space``)
and replaces the most recently typed character with the next variant from the
bundled replacement chains. Press ``Esc`` to exit.

Utility commands:

* ``--list-chains`` prints the available replacement chain names without
  starting the keyboard listener.
* ``--demo <char>`` previews the full cycle and next variant for a character.

Requires: ``pynput`` (install with ``pip install pynput``).
"""

from __future__ import annotations

import argparse
import sys
import time
from dataclasses import dataclass
from typing import Iterable, Optional, TYPE_CHECKING

from .chains import DEFAULT_CHAIN_NAMES, build_reverse_index, load_cycles
from .data import list_available_chains

try:
    from pynput import keyboard
except ImportError as exc:  # pragma: no cover - allows graceful CLI feedback
    keyboard = None  # type: ignore[assignment]
    _IMPORT_ERROR = exc
else:
    _IMPORT_ERROR = None

if TYPE_CHECKING:  # pragma: no cover - typing helpers only
    from pynput import keyboard as keyboard_mod

HOTKEY_DEFAULT = "<alt>+<shift>+space"
EXIT_KEY = "esc"
CHAR_STALE_TIMEOUT = 2.5  # seconds


def parse_args(argv: Iterable[str]) -> argparse.Namespace:
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
    return parser.parse_args(list(argv))


@dataclass
class ReplacementCycler:
    """Provide next-character lookup for a collection of replacement cycles."""

    cycles: dict[str, list[str]]
    reverse_index: dict[str, tuple[str, int]]

    @classmethod
    def from_chain_names(cls, chain_names: Iterable[str]) -> "ReplacementCycler":
        cycles = load_cycles(chain_names)
        return cls(cycles=cycles, reverse_index=build_reverse_index(cycles))

    def next_variant(self, char: str) -> Optional[str]:
        """Return the next character in the cycle, wrapping to the beginning."""
        entry = self.reverse_index.get(char)
        if not entry:
            return None
        base, idx = entry
        cycle = self.cycles[base]
        return cycle[(idx + 1) % len(cycle)]

    def cycle_sequence(self, char: str) -> Optional[list[str]]:
        """Return the ordered cycle for the base character associated with ``char``."""
        entry = self.reverse_index.get(char)
        if not entry:
            return None
        base, _ = entry
        return list(self.cycles[base])


def describe_cycle(cycler: ReplacementCycler, char: str) -> Optional[str]:
    """Return a human-readable description of the cycle for ``char``."""
    if len(char) != 1:
        raise ValueError("Demo expects a single character.")

    sequence = cycler.cycle_sequence(char)
    if not sequence:
        return None

    next_char = cycler.next_variant(char)
    cycle_str = " -> ".join(sequence + [sequence[0]])
    return (
        f"Cycle for '{sequence[0]}': {cycle_str}\n"
        f"Next after '{char}': {next_char if next_char is not None else sequence[0]}"
    )


class HotkeyApplication:
    """Listen for the hotkey, cycling the last character when activated."""

    def __init__(
        self,
        hotkey: str,
        chains: Iterable[str],
        timeout: float,
        cycler: ReplacementCycler | None = None,
    ) -> None:
        if keyboard is None:
            message = "pynput is required for this demo. Install it with 'pip install pynput'."
            raise SystemExit(f"{message}\n\nImport error: {_IMPORT_ERROR}")

        self._controller = keyboard.Controller()
        self._hotkey = keyboard.HotKey(keyboard.HotKey.parse(hotkey), self._on_activate)
        self._combo_label = hotkey
        self._cycler = cycler or ReplacementCycler.from_chain_names(chains)
        self._timeout = max(0.0, timeout)

        self._last_char: Optional[str] = None
        self._last_timestamp = 0.0

    def run(self) -> None:
        """Begin listening for key events."""
        print("No Switch proof-of-concept running.")
        print(f"Hotkey: {self._combo_label} | Exit: Esc")
        print("Tip: type a supported character (e.g., 'a'), then press the hotkey to cycle variants.\n")

        with keyboard.Listener(on_press=self._on_press, on_release=self._on_release) as listener:
            listener.join()

    def _on_press(self, key: "keyboard.Key | keyboard.KeyCode") -> Optional[bool]:
        """Handle key press events: feed the hotkey and capture characters."""
        self._hotkey.press(key)

        if key == keyboard.Key.esc:
            print("Exiting No Switch prototype.")
            return False

        char = getattr(key, "char", None)
        if char and len(char) == 1 and char.isprintable():
            self._last_char = char
            self._last_timestamp = time.monotonic()
        return None

    def _on_release(self, key: "keyboard.Key | keyboard.KeyCode") -> None:
        """Handle key release events for the hotkey recognizer."""
        self._hotkey.release(key)

    def _on_activate(self) -> None:
        """Replace the most recent character with its next variant."""
        if not self._last_char:
            print("No character ready to cycle.")
            return

        if self._timeout and (time.monotonic() - self._last_timestamp) > self._timeout:
            print("Last character is stale; type a new character before cycling.")
            return

        next_char = self._cycler.next_variant(self._last_char)
        if not next_char:
            print(f"No chain defined for '{self._last_char}'.")
            return

        self._controller.press(keyboard.Key.backspace)
        self._controller.release(keyboard.Key.backspace)
        self._controller.type(next_char)
        self._last_char = next_char
        self._last_timestamp = time.monotonic()


def main(argv: Iterable[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
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

    try:
        app = HotkeyApplication(args.hotkey, args.chains, args.timeout, cycler=cycler)
    except ValueError as exc:
        print(exc)
        return 2
    app.run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
