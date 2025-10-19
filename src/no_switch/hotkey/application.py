"""Interactive hotkey application for cycling character variants."""

from __future__ import annotations

import time
from typing import Iterable, Optional, TYPE_CHECKING

from .cycler import ReplacementCycler

try:
    from pynput import keyboard
except ImportError as exc:  # pragma: no cover - allows graceful CLI feedback
    keyboard = None  # type: ignore[assignment]
    _IMPORT_ERROR = exc
else:
    _IMPORT_ERROR = None

if TYPE_CHECKING:  # pragma: no cover - typing helpers only
    from pynput import keyboard as keyboard_mod

__all__ = ["HotkeyApplication", "keyboard", "_IMPORT_ERROR"]


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
        print("No Switch hotkey listener running.")
        print(f"Hotkey: {self._combo_label} | Exit: Esc")
        print("Tip: type a supported character (e.g., 'a'), then press the hotkey to cycle variants.\n")

        with keyboard.Listener(on_press=self._on_press, on_release=self._on_release) as listener:
            listener.join()

    def _on_press(self, key: "keyboard.Key | keyboard.KeyCode") -> Optional[bool]:
        """Handle key press events: feed the hotkey and capture characters."""
        self._hotkey.press(key)

        if key == keyboard.Key.esc:
            print("Exiting No Switch listener.")
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
