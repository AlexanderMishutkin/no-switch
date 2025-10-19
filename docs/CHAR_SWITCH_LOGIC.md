# Character Switching Core Logic

This document outlines how No Switch manages character replacement chains, language-focused presets, and user customization. It describes the expected behavior before we implement the production code.

## Core Concepts

- **Replacement chain** – an ordered list of symbols (e.g., `["U", "Ü", "Ù", "Ū"]`). The listener swaps the currently selected character for the next symbol in the chain whenever the active hotkey fires. The last symbol wraps around to the first.
- **Preset** – a named collection of replacement chains. Presets can be shipped with the application (defaults) or created by the user (custom). Only one preset is active at a time.
- **Active preset** – the preset currently used by the runtime. Hotkey events consult chains from the active preset only.

## Default Presets

Defaults ship with the app so users can get started without manual configuration. Each preset targets a specific language or workflow and may include a mix of Latin and non-Latin characters. Some languages only need pairs while others rely on longer chains.

- **German** – relies on simple pairs such as `A` ↔ `Ä`, `O` ↔ `Ö`, `U` ↔ `Ü`, `S` ↔ `ß`, and straight ↔ curly punctuation. Chains are mostly length two and cycle directly between the base and accented form.
- **Serbian** – blends Serbian Latin and Cyrillic needs. Many pairs simply swap Latin ↔ Cyrillic glyphs (e.g., `Đ` ↔ `Ђ`), while a few chains cover multi-letter sounds (`Њ` ↔ `Nj`, `Љ` ↔ `Lj`). The preset favors pairs wherever possible to keep cycling predictable.
- **English symbols** (placeholder) – provides quick access to typographic symbols (e.g., `--` ↔ `—`, `'` ↔ `’`, `" "` ↔ `“ ”`) for users who primarily type in English.

Default presets are stored in `resources/` so they can be loaded on first run or restored later.

## Custom Presets

Users can create their own presets by:

1. **Duplicating a default preset** or starting from an empty one.
2. **Adding chains** – specify a base character and the ordered list of replacements.
3. **Reordering symbols** inside a chain to control the cycling order.
4. **Reprioritizing chains** – longer or more specific triggers (e.g., `bl`) can be ordered ahead of generic ones (`b`) so they win lookups.
5. **Removing symbols** that are not useful for their workflow.
6. **Saving and exporting** the preset under a custom name for future reuse or sharing.

Custom presets live in the user configuration directory (exact path TBD) and override defaults when names collide. Exported presets are saved as shareable files (likely JSON or YAML).

## Selecting the Active Preset

- Exactly one preset is active at runtime. The UI and CLI will expose a control to switch presets.
- When the active preset changes, the listener reloads its chains immediately.
- If the chosen preset is missing or corrupt, fall back to a default preset (likely the first default, e.g., German) and notify the user.

## Chain Resolution Rules

- Chains are looked up by the currently selected character (case-sensitive by default).
- Chain order matters: the engine evaluates chains from highest to lowest priority, allowing multi-character triggers (like `bl`) to match before single-character fallbacks (`b`).
- If a character belongs to multiple chains, the most specific chain (e.g., matching script and case) wins. Collision resolution strategy (priority order or last-write wins) must be defined in the implementation.
- When a chain is exhausted, the next hotkey event cycles back to the starting character.
- Users can opt in to “sticky original” behavior, where the base character always remains in the chain to guarantee a reversible cycle.

## Configuration Persistence

- Default presets are read-only; updates require a new release.
- Custom presets are stored in a user-writable location. The app writes the entire preset (name + chains) after each modification and on explicit export.
- The currently active preset name is stored separately so the app can restore it on startup.

## Exporting and Importing Presets

- **Export** – users can save any custom or modified preset to disk. The export includes metadata (name, version, locale tags) and all chains.
- **Import** – users can load a preset file, preview its chains, and either replace an existing preset or store it alongside others.
- File validation ensures imported data matches the schema before it becomes available to the runtime.

## Planned Enhancements

- Allow sharing presets (export/import as JSON or YAML).
- Support per-application preset overrides (e.g., a code editor uses different chains than a writing app).
- Provide a library of community presets download-able from the UI once networking policies permit.

## Implementation Outline

We expect three major operational areas, each backed by dedicated modules:

1. **Load / Export / Import Presets** (`preset_io.py`)
   - `PresetRepository`
   - `PresetImporter`
   - `PresetExporter`
2. **Edit Presets** (`preset_editor.py`)
   - `PresetEditor`
   - `ChainPriorityManager`
3. **Use Presets at Runtime** (`chain_runtime.py`)
   - `ChainResolver`
   - `HotkeyChainService`
