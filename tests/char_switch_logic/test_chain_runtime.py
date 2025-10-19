from __future__ import annotations

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from src.char_switch_logic.chain_runtime import ChainResolver, HotkeyChainService
from src.char_switch_logic.preset_io import PresetRepository


class ChainRuntimeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.tmp_path = Path(self.temp_dir.name)

    def make_service(self, preset_name: str) -> HotkeyChainService:
        repository = PresetRepository(config_dir=self.tmp_path)
        preset = repository.get(preset_name)
        self.assertIsNotNone(preset, f"Preset {preset_name} should be available.")
        assert preset
        resolver = ChainResolver(preset)
        return HotkeyChainService(resolver)

    def test_multi_letter_priority_wins_over_single_letter(self) -> None:
        service = self.make_service("ru")

        result = service.apply("bl", cursor=2)
        self.assertIsNotNone(result)
        assert result
        self.assertEqual(result.current, "ъ")
        self.assertEqual((result.start, result.end), (0, 1))

        second = service.apply(result.text, cursor=1)
        self.assertIsNotNone(second)
        assert second
        self.assertEqual(second.current, "bl")
        self.assertEqual((second.start, second.end), (0, 2))

    def test_selection_cycles_through_chain(self) -> None:
        service = self.make_service("de")
        text = "Über"

        result = service.apply(text, cursor=0, selection=(0, 1))
        self.assertIsNotNone(result)
        assert result
        self.assertEqual(result.text, "Uber")
        self.assertEqual(result.current, "U")
        self.assertEqual(result.previous, "Ü")

        next_result = service.apply(result.text, cursor=0, selection=(0, 1))
        self.assertIsNotNone(next_result)
        assert next_result
        self.assertEqual(next_result.text, text)

    def test_longer_chain_symbols_take_precedence(self) -> None:
        service = self.make_service("ru")

        result = service.apply("shch", cursor=4)
        self.assertIsNotNone(result)
        assert result
        self.assertEqual(result.current, "щ")

        revert = service.apply(result.text, cursor=len(result.text))
        self.assertIsNotNone(revert)
        assert revert
        self.assertEqual(revert.current, "shch")

    def test_no_chain_match_returns_none(self) -> None:
        service = self.make_service("de")
        self.assertIsNone(service.apply("plain", cursor=5))
        self.assertIsNone(service.apply("plain", cursor=0, selection=(0, 2)))

    def test_serbian_cyrillic_trigger_cycles(self) -> None:
        service = self.make_service("sr")

        text = "ч"
        seen = []
        for _ in range(6):
            result = service.apply(text, cursor=len(text))
            self.assertIsNotNone(result)
            assert result
            seen.append(result.current)
            self.assertIn(result.previous, {"ч", "c", "č", "ć", "ц", "ћ"})
            text = result.text

        self.assertIn("c", seen)
        self.assertTrue(any("ч" in value for value in seen))
        self.assertIn(text, {"ч", "ћ"})

    def test_serbian_soft_sign_pair(self) -> None:
        service = self.make_service("sr")

        text = "ль"
        result = service.apply(text, cursor=2)
        self.assertIsNotNone(result)
        assert result
        self.assertEqual(result.previous, "ль")
        self.assertNotEqual(result.current, "ль")
        self.assertTrue(any(char in result.current for char in ("l", "љ")))

        third = service.apply(result.text, cursor=len(result.text))
        self.assertIsNotNone(third)
        assert third
        self.assertNotEqual(third.current, result.current)


if __name__ == "__main__":
    unittest.main()
