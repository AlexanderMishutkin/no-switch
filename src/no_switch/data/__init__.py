"""Utilities for loading bundled replacement chains."""

from __future__ import annotations

import json
from importlib import resources
from importlib.resources.abc import Traversable
from typing import cast

__all__ = ["load_chain", "list_available_chains"]


def _chains_dir() -> Traversable:
    """Return the path to the chains directory."""
    return resources.files(__name__).joinpath("chains")


def list_available_chains() -> list[str]:
    """Return each available chain file stem."""
    return sorted(
        path.stem for path in _chains_dir().iterdir() if path.is_file() and path.suffix == ".json"
    )


def load_chain(name: str) -> dict[str, list[str]]:
    """Load a named replacement chain from JSON."""
    target = _chains_dir().joinpath(f"{name}.json")
    if not target.is_file():
        available = ", ".join(list_available_chains())
        raise ValueError(f"Unknown chain '{name}'. Available: {available}")
    return cast(dict[str, list[str]], json.loads(target.read_text(encoding="utf-8")))
