"""
Preset editing utilities.

The editor deals purely with in-memory data structures and delegates persistence
to `PresetRepository` or the importer/exporter helpers.
"""

from __future__ import annotations

from dataclasses import replace
from typing import List, Optional

from .preset_io import Chain, Preset


class PresetEditor:
    """High-level API that mutates a preset definition."""

    def __init__(self, preset: Preset) -> None:
        self._preset = preset

    @property
    def preset(self) -> Preset:
        return self._preset

    def add_chain(self, chain: Chain, position: Optional[int] = None) -> None:
        if any(existing.trigger == chain.trigger for existing in self._preset.chains):
            raise ValueError(f"Chain with trigger '{chain.trigger}' already exists.")
        if position is None or position >= len(self._preset.chains):
            self._preset.chains.append(chain)
        else:
            self._preset.chains.insert(max(position, 0), chain)

    def remove_chain(self, trigger: str) -> None:
        self._preset.chains = [chain for chain in self._preset.chains if chain.trigger != trigger]

    def update_chain_symbols(self, trigger: str, symbols: List[str]) -> None:
        chain = self._find_chain(trigger)
        updated = Chain(trigger=chain.trigger, symbols=symbols, description=chain.description, sticky=chain.sticky)
        index = self._preset.chains.index(chain)
        self._preset.chains[index] = updated

    def update_chain_description(self, trigger: str, description: Optional[str]) -> None:
        chain = self._find_chain(trigger)
        updated = replace(chain, description=description)
        index = self._preset.chains.index(chain)
        self._preset.chains[index] = updated

    def set_sticky(self, trigger: str, sticky: bool) -> None:
        chain = self._find_chain(trigger)
        updated = Chain(trigger=chain.trigger, symbols=chain.symbols, description=chain.description, sticky=sticky)
        index = self._preset.chains.index(chain)
        self._preset.chains[index] = updated

    def _find_chain(self, trigger: str) -> Chain:
        for chain in self._preset.chains:
            if chain.trigger == trigger:
                return chain
        raise LookupError(f"Chain with trigger '{trigger}' not found.")


class ChainPriorityManager:
    """
    Helper class that maintains chain ordering (priority).

    Higher priority chains should appear earlier in the preset's chain list.
    """

    def __init__(self, preset: Preset) -> None:
        self._preset = preset

    def move(self, trigger: str, new_index: int) -> None:
        chain = self._extract(trigger)
        clamped_index = max(0, min(new_index, len(self._preset.chains)))
        self._preset.chains.insert(clamped_index, chain)

    def reorder(self, ordered_triggers: List[str]) -> None:
        mapping = {chain.trigger: chain for chain in self._preset.chains}
        new_order: List[Chain] = []
        for trigger in ordered_triggers:
            if trigger in mapping:
                new_order.append(mapping.pop(trigger))
        # Append remaining chains that were not explicitly ordered.
        new_order.extend(mapping.values())
        self._preset.chains = new_order

    def _extract(self, trigger: str) -> Chain:
        for index, chain in enumerate(self._preset.chains):
            if chain.trigger == trigger:
                return self._preset.chains.pop(index)
        raise LookupError(f"Chain with trigger '{trigger}' not found.")
