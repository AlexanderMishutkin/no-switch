from __future__ import annotations

import pytest

from char_switch_logic import Chain, ChainPriorityManager, Preset, PresetEditor


def sample_preset() -> Preset:
    return Preset(
        name="sample",
        description="Sample preset.",
        chains=[
            Chain(trigger="a", symbols=["a", "ą"]),
            Chain(trigger="e", symbols=["e", "ę"]),
        ],
    )


def test_add_chain_at_specific_position() -> None:
    preset = sample_preset()
    editor = PresetEditor(preset)

    editor.add_chain(Chain(trigger="o", symbols=["o", "ó"]), position=1)

    assert [chain.trigger for chain in preset.chains] == ["a", "o", "e"]


def test_remove_chain_by_trigger() -> None:
    preset = sample_preset()
    editor = PresetEditor(preset)

    editor.remove_chain("e")

    assert [chain.trigger for chain in preset.chains] == ["a"]


def test_update_chain_symbols_rebuilds_cycle() -> None:
    preset = sample_preset()
    editor = PresetEditor(preset)

    editor.update_chain_symbols("a", ["à", "â", "a"])

    chain = next(chain for chain in preset.chains if chain.trigger == "a")
    assert chain.symbols == ["à", "â", "a"]
    assert chain.next_symbol("â") == "a"


def test_priority_manager_reorders_chains() -> None:
    preset = sample_preset()
    manager = ChainPriorityManager(preset)

    manager.move("e", 0)
    assert [chain.trigger for chain in preset.chains][:2] == ["e", "a"]

    manager.reorder(["a"])
    assert [chain.trigger for chain in preset.chains] == ["a", "e"]


def test_add_chain_rejects_duplicate_trigger() -> None:
    preset = sample_preset()
    editor = PresetEditor(preset)

    with pytest.raises(ValueError):
        editor.add_chain(Chain(trigger="a", symbols=["a", "ä"]))
