from __future__ import annotations

from pathlib import Path
import json

import pytest

from char_switch_logic import Chain, Preset, PresetExporter, PresetImporter, PresetRepository


def create_repository(tmp_path: Path) -> PresetRepository:
    return PresetRepository(config_dir=tmp_path)


def test_loads_default_presets(tmp_path: Path) -> None:
    repository = create_repository(tmp_path)

    presets = repository.list_presets()

    assert {"de", "sr", "ru"}.issubset(presets.keys())
    german = repository.get("de")
    assert german is not None
    assert german.description
    # German preset relies mostly on pairs
    assert all(len(chain.symbols) == 2 or chain.trigger in {'"', "'"} for chain in german.chains)
    serbian = repository.get("sr")
    assert serbian is not None
    assert any("ч" in chain.symbols for chain in serbian.chains)


def test_save_and_reload_custom_preset(tmp_path: Path) -> None:
    repository = create_repository(tmp_path)
    greek = Preset(
        name="el",
        description="Greek transliteration basics.",
        chains=[Chain(trigger="ch", symbols=["ch", "χ"])],
    )

    saved_path = repository.save_custom(greek)
    assert saved_path.exists()

    # New repository instance should pick up the saved preset automatically.
    reloaded = create_repository(tmp_path).get("el")
    assert reloaded is not None
    assert reloaded.description == "Greek transliteration basics."
    assert reloaded.chains[0].symbols == ["ch", "χ"]


def test_export_and_import_roundtrip(tmp_path: Path) -> None:
    repository = create_repository(tmp_path)
    german = repository.get("de")
    assert german is not None

    exporter = PresetExporter(repository)
    export_path = tmp_path / "export" / "german.json"
    output_path = exporter.export("de", export_path)
    assert output_path.exists()

    # Modify exported preset and import under a new repository instance.
    data = json.loads(export_path.read_text(encoding="utf-8"))
    data["name"] = "de_custom"
    data["description"] = "Modified German preset."
    export_path.write_text(json.dumps(data), encoding="utf-8")

    repo_import_target = create_repository(tmp_path / "second_config")
    importer = PresetImporter(repo_import_target)
    imported = importer.import_file(export_path)

    assert imported.name == "de_custom"
    assert repo_import_target.get("de_custom") is not None


def test_import_requires_overwrite_when_conflicting(tmp_path: Path) -> None:
    repository = create_repository(tmp_path)
    exporter = PresetExporter(repository)
    export_path = tmp_path / "conflict.json"
    exporter.export("de", export_path)

    importer = PresetImporter(repository)
    with pytest.raises(ValueError):
        importer.import_file(export_path)

    loaded = json.loads(export_path.read_text(encoding="utf-8"))
    loaded["description"] = "Tweaked description."
    export_path.write_text(json.dumps(loaded), encoding="utf-8")

    imported = importer.import_file(export_path, overwrite=True)
    assert imported.description == "Tweaked description."
