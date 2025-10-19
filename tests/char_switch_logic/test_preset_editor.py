from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.char_switch_logic import (  # noqa: E402
    Chain,
    ChainPriorityManager,
    Preset,
    PresetEditor,
)


def sample_preset() -> Preset:
    return Preset(
        name="sample",
        description="Sample preset.",
        chains=[
            Chain(trigger="a", symbols=["a", "ą"]),
            Chain(trigger="e", symbols=["e", "ę"]),
        ],
    )


class PresetEditorTests(unittest.TestCase):
    def test_add_chain_at_specific_position(self) -> None:
        preset = sample_preset()
        editor = PresetEditor(preset)

        editor.add_chain(Chain(trigger="o", symbols=["o", "ó"]), position=1)

        self.assertEqual([chain.trigger for chain in preset.chains], ["a", "o", "e"])

    def test_remove_chain_by_trigger(self) -> None:
        preset = sample_preset()
        editor = PresetEditor(preset)

        editor.remove_chain("e")

        self.assertEqual([chain.trigger for chain in preset.chains], ["a"])

    def test_update_chain_symbols_rebuilds_cycle(self) -> None:
        preset = sample_preset()
        editor = PresetEditor(preset)

        editor.update_chain_symbols("a", ["à", "â", "a"])

        chain = next(chain for chain in preset.chains if chain.trigger == "a")
        self.assertEqual(chain.symbols, ["à", "â", "a"])
        self.assertEqual(chain.next_symbol("â"), "a")

    def test_priority_manager_reorders_chains(self) -> None:
        preset = sample_preset()
        manager = ChainPriorityManager(preset)

        manager.move("e", 0)
        self.assertEqual([chain.trigger for chain in preset.chains][:2], ["e", "a"])

        manager.reorder(["a"])
        self.assertEqual([chain.trigger for chain in preset.chains], ["a", "e"])

    def test_add_chain_rejects_duplicate_trigger(self) -> None:
        preset = sample_preset()
        editor = PresetEditor(preset)

        with self.assertRaises(ValueError):
            editor.add_chain(Chain(trigger="a", symbols=["a", "ä"]))


if __name__ == "__main__":
    unittest.main()
