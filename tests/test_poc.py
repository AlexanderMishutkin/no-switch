import pytest

from no_switch.poc import ReplacementCycler, describe_cycle


def test_describe_cycle_returns_cycle_for_known_character():
    cycler = ReplacementCycler.from_chain_names(["latin"])

    report = describe_cycle(cycler, "a")

    assert report is not None
    assert "Cycle for 'a':" in report
    assert "Next after 'a':" in report


def test_describe_cycle_returns_none_for_missing_character():
    cycler = ReplacementCycler.from_chain_names(["latin"])

    assert describe_cycle(cycler, "x") is None


def test_describe_cycle_rejects_multi_character_input():
    cycler = ReplacementCycler.from_chain_names(["latin"])

    with pytest.raises(ValueError):
        describe_cycle(cycler, "abc")
