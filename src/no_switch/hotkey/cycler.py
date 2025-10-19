"""Replacement cycle helpers used by the No Switch hotkey tools."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Optional

from ..chains import DEFAULT_CHAIN_NAMES, build_reverse_index, load_cycles

__all__ = ["ReplacementCycler", "describe_cycle"]


@dataclass
class ReplacementCycler:
    """Provide next-character lookup for a collection of replacement cycles."""

    cycles: dict[str, list[str]]
    reverse_index: dict[str, tuple[str, int]]

    @classmethod
    def from_chain_names(cls, chain_names: Iterable[str] = DEFAULT_CHAIN_NAMES) -> "ReplacementCycler":
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
