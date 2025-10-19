"""Utility helpers for replacement chains."""

from __future__ import annotations

from typing import Iterable

from . import data

DEFAULT_CHAIN_NAMES: tuple[str, ...] = ("latin", "cyrillic")

__all__ = ["DEFAULT_CHAIN_NAMES", "load_cycles", "build_reverse_index"]


def load_cycles(chain_names: Iterable[str] = DEFAULT_CHAIN_NAMES) -> dict[str, list[str]]:
    """Return a mapping of base characters to replacement cycles."""
    merged: dict[str, list[str]] = {}
    for name in chain_names:
        definitions = data.load_chain(name)
        for base, variants in definitions.items():
            cycle = [base] + [v for v in variants if v and v != base]
            if base in merged:
                existing = merged[base]
                for variant in cycle[1:]:
                    if variant not in existing:
                        existing.append(variant)
            else:
                merged[base] = cycle
    return merged


def build_reverse_index(cycles: dict[str, list[str]]) -> dict[str, tuple[str, int]]:
    """Create a lookup that maps any variant to its base and index within the cycle."""
    index: dict[str, tuple[str, int]] = {}
    for base, cycle in cycles.items():
        for idx, char in enumerate(cycle):
            index[char] = (base, idx)
    return index
