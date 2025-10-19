from __future__ import annotations

from char_switch_logic import ChainResolver, HotkeyChainService, PresetRepository


def make_service(preset_name: str, tmp_path) -> HotkeyChainService:
    repository = PresetRepository(config_dir=tmp_path)
    preset = repository.get(preset_name)
    assert preset is not None
    resolver = ChainResolver(preset)
    return HotkeyChainService(resolver)


def test_multi_letter_priority_wins_over_single_letter(tmp_path) -> None:
    service = make_service("ru", tmp_path)

    result = service.apply("bl", cursor=2)
    assert result is not None
    assert result.current == "ъ"
    assert result.start == 0 and result.end == 1

    # Cycling again should bring back the transliteration pair.
    second = service.apply(result.text, cursor=1)
    assert second is not None
    assert second.current == "bl"
    assert second.start == 0 and second.end == 2


def test_selection_cycles_through_chain(tmp_path) -> None:
    service = make_service("de", tmp_path)
    text = "Über"

    result = service.apply(text, cursor=0, selection=(0, 1))
    assert result is not None
    assert result.text == "Uber"
    assert result.current == "U"
    assert result.previous == "Ü"

    # Selecting the updated character should cycle back to the umlaut.
    next_result = service.apply(result.text, cursor=0, selection=(0, 1))
    assert next_result is not None
    assert next_result.text == text


def test_longer_chain_symbols_take_precedence(tmp_path) -> None:
    service = make_service("ru", tmp_path)

    result = service.apply("shch", cursor=4)
    assert result is not None
    assert result.current == "щ"

    revert = service.apply(result.text, cursor=len(result.text))
    assert revert is not None
    assert revert.current == "shch"


def test_no_chain_match_returns_none(tmp_path) -> None:
    service = make_service("de", tmp_path)

    assert service.apply("plain", cursor=5) is None

    # Selection with no matching chain should also return None.
    assert service.apply("plain", cursor=0, selection=(0, 2)) is None
