from __future__ import annotations

import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from src.char_switch_logic.preset_io import (
    Chain,
    Preset,
    PresetExporter,
    PresetImporter,
    PresetRepository,
)


class PresetIOTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.tmp_path = Path(self.temp_dir.name)
        self.repository = PresetRepository(config_dir=self.tmp_path)

    def test_loads_default_presets(self) -> None:
        presets = self.repository.list_presets()
        self.assertTrue({"de", "sr", "ru"}.issubset(presets.keys()))

        german = self.repository.get("de")
        self.assertIsNotNone(german)
        assert german
        self.assertTrue(german.description)
        self.assertTrue(all(len(chain.symbols) == 2 or chain.trigger in {'"', "'"} for chain in german.chains))

        serbian = self.repository.get("sr")
        self.assertIsNotNone(serbian)
        assert serbian
        self.assertTrue(any("ч" in chain.symbols for chain in serbian.chains))
        self.assertTrue(any(chain.trigger == "ч" for chain in serbian.chains))

        russian = self.repository.get("ru")
        self.assertIsNotNone(russian)
        assert russian
        self.assertTrue(any(chain.trigger == "bl" and "ы" in chain.symbols for chain in russian.chains))

    def test_save_and_reload_custom_preset(self) -> None:
        greek = Preset(
            name="el",
            description="Greek transliteration basics.",
            chains=[Chain(trigger="ch", symbols=["ch", "χ"])],
        )
        saved_path = self.repository.save_custom(greek)
        self.assertTrue(saved_path.exists())

        reloaded = PresetRepository(config_dir=self.tmp_path).get("el")
        self.assertIsNotNone(reloaded)
        assert reloaded
        self.assertEqual(reloaded.description, "Greek transliteration basics.")
        self.assertEqual(reloaded.chains[0].symbols, ["ch", "χ"])

    def test_export_and_import_roundtrip(self) -> None:
        german = self.repository.get("de")
        self.assertIsNotNone(german)
        assert german

        exporter = PresetExporter(self.repository)
        export_path = self.tmp_path / "export" / "german.json"
        output_path = exporter.export("de", export_path)
        self.assertTrue(output_path.exists())

        data = json.loads(export_path.read_text(encoding="utf-8"))
        data["name"] = "de_custom"
        data["description"] = "Modified German preset."
        export_path.write_text(json.dumps(data), encoding="utf-8")

        with TemporaryDirectory() as target_tmp:
            repo_import_target = PresetRepository(config_dir=Path(target_tmp))
            importer = PresetImporter(repo_import_target)
            imported = importer.import_file(export_path)
            self.assertEqual(imported.name, "de_custom")
            self.assertIsNotNone(repo_import_target.get("de_custom"))

    def test_import_requires_overwrite_when_conflicting(self) -> None:
        exporter = PresetExporter(self.repository)
        export_path = self.tmp_path / "conflict.json"
        exporter.export("de", export_path)

        importer = PresetImporter(self.repository)
        with self.assertRaises(ValueError):
            importer.import_file(export_path)

        loaded = json.loads(export_path.read_text(encoding="utf-8"))
        loaded["description"] = "Tweaked description."
        export_path.write_text(json.dumps(loaded), encoding="utf-8")

        imported = importer.import_file(export_path, overwrite=True)
        self.assertEqual(imported.description, "Tweaked description.")


if __name__ == "__main__":
    unittest.main()
