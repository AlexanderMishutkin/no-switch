"""Public entry points for the character switching logic package."""

from .chain_runtime import ChainResolver, HotkeyChainService, ReplacementResult
from .preset_editor import ChainPriorityManager, PresetEditor
from .preset_io import Chain, Preset, PresetExporter, PresetImporter, PresetRepository

__all__ = [
    "Chain",
    "ChainResolver",
    "ChainPriorityManager",
    "HotkeyChainService",
    "Preset",
    "PresetEditor",
    "PresetExporter",
    "PresetImporter",
    "PresetRepository",
    "ReplacementResult",
]
