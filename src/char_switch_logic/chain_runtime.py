"""
Runtime helpers for applying character switching presets.

These classes focus on selecting the correct chain based on the surrounding text
and producing the replacement when a hotkey event fires.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Optional, Tuple

from .preset_io import Chain, Preset


@dataclass(frozen=True)
class ChainMatch:
    """Represents a selected chain and the substring it matched."""

    chain: Chain
    matched: str
    start: int
    end: int

    @property
    def length(self) -> int:
        return self.end - self.start


@dataclass(frozen=True)
class ReplacementResult:
    """Outcome returned by the hotkey service after performing a replacement."""

    text: str
    start: int
    end: int
    previous: str
    current: str
    chain: Chain


class ChainResolver:
    """Lookup and prioritise chains within a preset."""

    def __init__(self, preset: Preset) -> None:
        self._preset = preset
        self._chains = list(preset.chains)
        self._order = {chain.trigger: index for index, chain in enumerate(self._chains)}
        self._symbol_cache = self._build_symbol_cache()
        self._max_symbol_length = max((len(symbol) for (_, symbol) in self._symbol_cache), default=0)

    @property
    def max_symbol_length(self) -> int:
        return self._max_symbol_length

    def _build_symbol_cache(self) -> Iterable[Tuple[Chain, str]]:
        combinations = []
        for chain in self._chains:
            priority = self._order[chain.trigger]
            for symbol in chain.iter_symbols_by_length():
                combinations.append((priority, -len(symbol), chain, symbol))
        combinations.sort()
        # Since we sorted by priority and negative length, construct tuples.
        return [(chain, symbol) for _, _, chain, symbol in combinations]

    def find_for_token(self, token: str) -> Optional[Chain]:
        """Locate a chain that contains the provided token."""
        for chain in self._chains:
            if chain.contains(token):
                return chain
        return None

    def match_at(self, text: str, cursor: int) -> Optional[ChainMatch]:
        """Match the best chain ending at the cursor position."""
        if not text or cursor <= 0:
            return None
        window_start = max(0, cursor - self._max_symbol_length)
        context = text[window_start:cursor]
        if not context:
            return None

        for chain, symbol in self._symbol_cache:
            if context.endswith(symbol):
                start = cursor - len(symbol)
                return ChainMatch(chain=chain, matched=symbol, start=start, end=cursor)
        return None


class HotkeyChainService:
    """Apply preset chains to text fragments triggered by hotkeys."""

    def __init__(self, resolver: ChainResolver) -> None:
        self._resolver = resolver

    def apply(
        self,
        text: str,
        cursor: int,
        selection: Optional[Tuple[int, int]] = None,
    ) -> Optional[ReplacementResult]:
        """
        Trigger a replacement at the current cursor position or selection.

        Returns a `ReplacementResult` when a chain fires, otherwise `None`.
        """
        if not text:
            return None

        if selection:
            start, end = selection
            if start < 0 or end > len(text) or start > end:
                raise ValueError("Invalid selection bounds.")
            if start == end:
                # Treat empty selection as cursor mode.
                return self.apply(text, cursor=start, selection=None)

            token = text[start:end]
            chain = self._resolver.find_for_token(token)
            if not chain:
                # Attempt to match by trigger if token equals trigger casing.
                match = self._resolver.match_at(token, len(token))
                chain = match.chain if match else None
            if not chain:
                return None
            replacement = chain.next_symbol(token)
            new_text = text[:start] + replacement + text[end:]
            return ReplacementResult(
                text=new_text,
                start=start,
                end=start + len(replacement),
                previous=token,
                current=replacement,
                chain=chain,
            )

        match = self._resolver.match_at(text, cursor)
        if not match:
            return None

        replacement = match.chain.next_symbol(match.matched)
        new_text = text[:match.start] + replacement + text[match.end:]
        return ReplacementResult(
            text=new_text,
            start=match.start,
            end=match.start + len(replacement),
            previous=match.matched,
            current=replacement,
            chain=match.chain,
        )
