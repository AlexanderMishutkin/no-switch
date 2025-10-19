"""
Preset loading, saving, import, and export utilities.

This module defines the data structures shared across the character switching
logic and provides repository helpers that work with both bundled resources and
user-defined presets. Paths are resolved with `pathlib` to remain cross-platform.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Iterable, List, Optional
import json
import os
import importlib.resources as pkg_resources

DEFAULT_RESOURCE_PACKAGE = "resources.presets"
ENV_CONFIG_DIR = "NO_SWITCH_CONFIG_DIR"
DEFAULT_APP_DIR = "NoSwitch"
CUSTOM_PRESET_DIR = "presets"


def _expand_config_dir() -> Path:
    """Determine the base configuration directory for custom presets."""
    override = os.getenv(ENV_CONFIG_DIR)
    if override:
        return Path(override).expanduser().resolve()

    home = Path.home()
    if os.name == "nt":
        roaming = Path(os.getenv("APPDATA", home / "AppData" / "Roaming"))
        return roaming / DEFAULT_APP_DIR
    if sys_plist := os.getenv("XDG_CONFIG_HOME"):
        return Path(sys_plist).expanduser() / DEFAULT_APP_DIR.lower()
    return home / ".noswitch"


@dataclass
class Chain:
    """
    Ordered sequence of symbols that the switching logic cycles through.

    The first symbol may represent the trigger typed by the user. When `sticky`
    is true, the trigger is guaranteed to remain in the cycle so the original
    text can always be restored.
    """

    trigger: str
    symbols: List[str]
    description: Optional[str] = None
    sticky: bool = True

    def __post_init__(self) -> None:
        if not self.trigger:
            raise ValueError("Chain trigger must be a non-empty string.")
        if not self.symbols:
            raise ValueError("Chain symbols cannot be empty.")
        if self.sticky and self.trigger not in self.symbols:
            self.symbols.insert(0, self.trigger)
        # Ensure no duplicates while preserving order.
        deduped: List[str] = []
        for symbol in self.symbols:
            if symbol not in deduped:
                deduped.append(symbol)
        self.symbols = deduped

    def to_dict(self) -> Dict[str, object]:
        data: Dict[str, object] = {
            "trigger": self.trigger,
            "symbols": self.symbols,
        }
        if self.description:
            data["description"] = self.description
        if not self.sticky:
            data["sticky"] = False
        return data

    def next_symbol(self, current: str) -> str:
        """
        Calculate the next symbol in the chain for the given current value.

        When the current symbol is unknown, we default to the trigger so the
        user sees a consistent result.
        """
        if current not in self.symbols:
            return self.symbols[0]
        index = self.symbols.index(current)
        return self.symbols[(index + 1) % len(self.symbols)]

    def contains(self, candidate: str) -> bool:
        return candidate in self.symbols

    def iter_symbols_by_length(self) -> Iterable[str]:
        """Iterate over symbols sorted by length (descending) for priority matching."""
        return sorted(self.symbols, key=len, reverse=True)


@dataclass
class Preset:
    """Named collection of chains."""

    name: str
    description: str
    chains: List[Chain] = field(default_factory=list)

    def to_dict(self) -> Dict[str, object]:
        return {
            "name": self.name,
            "description": self.description,
            "chains": [chain.to_dict() for chain in self.chains],
        }

    @classmethod
    def from_dict(cls, data: Dict[str, object]) -> "Preset":
        chains_data = data.get("chains", [])
        chains = [Chain(**chain_dict) for chain_dict in chains_data]  # type: ignore[arg-type]
        return cls(
            name=str(data["name"]),
            description=str(data.get("description", "")),
            chains=chains,
        )

    @property
    def max_symbol_length(self) -> int:
        return max((len(symbol) for chain in self.chains for symbol in chain.symbols), default=0)


class PresetRepository:
    """
    Manage access to presets from bundled resources and user storage.

    Custom presets live in `<config_dir>/presets`. Default presets are read-only.
    """

    def __init__(
        self,
        resource_package: str = DEFAULT_RESOURCE_PACKAGE,
        config_dir: Optional[Path] = None,
    ) -> None:
        self._resource_package = resource_package
        self._config_dir = config_dir or _expand_config_dir()
        self._custom_dir = self._config_dir / CUSTOM_PRESET_DIR
        self._custom_dir.mkdir(parents=True, exist_ok=True)
        self._default_cache: Dict[str, Preset] = {}
        self._custom_cache: Dict[str, Preset] = {}
        self._load_defaults()
        self._load_customs()

    def _load_defaults(self) -> None:
        package_files = pkg_resources.files(self._resource_package)
        for resource in package_files.iterdir():
            if resource.suffix.lower() != ".json":
                continue
            with resource.open("r", encoding="utf-8") as handle:
                data = json.load(handle)
            preset = Preset.from_dict(data)
            self._default_cache[preset.name] = preset

    def _load_customs(self) -> None:
        if not self._custom_dir.exists():
            return
        for json_file in self._custom_dir.glob("*.json"):
            with json_file.open("r", encoding="utf-8") as handle:
                data = json.load(handle)
            preset = Preset.from_dict(data)
            self._custom_cache[preset.name] = preset

    def list_presets(self, include_custom: bool = True) -> Dict[str, Preset]:
        presets = dict(self._default_cache)
        if include_custom:
            presets.update(self._custom_cache)
        return presets

    def get(self, name: str) -> Optional[Preset]:
        return self._custom_cache.get(name) or self._default_cache.get(name)

    def save_custom(self, preset: Preset) -> Path:
        path = self._custom_dir / f"{preset.name}.json"
        with path.open("w", encoding="utf-8") as handle:
            json.dump(preset.to_dict(), handle, ensure_ascii=False, indent=2)
        self._custom_cache[preset.name] = preset
        return path

    def export(self, preset: Preset, destination: Path) -> Path:
        destination = destination.expanduser()
        destination.parent.mkdir(parents=True, exist_ok=True)
        with destination.open("w", encoding="utf-8") as handle:
            json.dump(preset.to_dict(), handle, ensure_ascii=False, indent=2)
        return destination

    def import_from(self, source: Path, overwrite: bool = False) -> Preset:
        source = source.expanduser()
        with source.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
        preset = Preset.from_dict(data)
        if not overwrite and self.get(preset.name):
            raise ValueError(f"Preset '{preset.name}' already exists. Pass overwrite=True to replace.")
        self.save_custom(preset)
        return preset


class PresetExporter:
    """Simple façade for exporting presets."""

    def __init__(self, repository: PresetRepository) -> None:
        self._repository = repository

    def export(self, preset_name: str, destination: Path) -> Path:
        preset = self._repository.get(preset_name)
        if not preset:
            raise LookupError(f"Preset '{preset_name}' not found.")
        return self._repository.export(preset, destination)


class PresetImporter:
    """Import presets from disk into the repository."""

    def __init__(self, repository: PresetRepository) -> None:
        self._repository = repository

    def import_file(self, source: Path, overwrite: bool = False) -> Preset:
        return self._repository.import_from(source, overwrite=overwrite)
