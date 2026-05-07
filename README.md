# PokemonRPG Database Generator

This repository extracts Pokemon data from custom RPG PDFs, merges it with game data from the Redux engine, and generates structured JSON databases plus printable PDF character sheets.

---

## Table of Contents

1. [Installation](#installation)
2. [Project Structure](#project-structure)
3. [Data Flow Overview](#data-flow-overview)
4. [Shell Scripts (entry points)](#shell-scripts-entry-points)
5. [Extraction Scripts](#extraction-scripts)
6. [Redux Integration Scripts](#redux-integration-scripts)
7. [PTU/PTE Merge Scripts](#ptupte-merge-scripts)
8. [PDF Generation Scripts](#pdf-generation-scripts)
9. [Utility Scripts (other_tools/)](#utility-scripts-other_tools)
10. [Core Modules](#core-modules)
11. [Data Files Reference](#data-files-reference)

---

## Installation

You need Python 3.10+ installed. Open a terminal in this folder.

**Linux:**
```bash
python -m venv my_env
source my_env/bin/activate
pip install pymupdf requests reportlab pypdf pandas PyPDF2 pydantic
```

**Windows:**
```powershell
# First, allow script execution (once per machine):
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

python -m venv my_env
cd my_env/Scripts ; .\activate ; cd ../..
pip install pymupdf requests reportlab pypdf PyPDF2 pandas pydantic
```

**Activate the environment before any run:**

```bash
# Fish shell (Linux):
source my_env/bin/activate.fish

# Bash/Zsh (Linux):
source my_env/bin/activate

# Windows PowerShell:
cd my_env/Scripts ; .\activate ; cd ../..
```

---

## Project Structure

```
PokemonRPG_Database_generator/
├── input_pdf/                  # Source PDFs to parse
├── data/                       # Database files (JSON, CSV, PDF)
│   ├── db_pokedex.json         # External Pokemon reference database
│   ├── reduxData_last.json     # Redux engine game data
│   ├── ptuabilities.csv        # PTU-specific abilities
│   └── ptumoves.csv            # PTU-specific moves
├── output/
│   ├── initials/               # Raw extraction results
│   ├── redux/                  # After Redux merge
│   ├── pte/                    # After PTU/PTE merge
│   └── finals/                 # Final combined outputs
├── images/                     # Cached Pokemon artwork
├── other_tools/                # Utility scripts
├── parsers.py                  # Core PDF parsing engine
├── pokemon_data.py             # Pydantic data models
└── my_env/                     # Python virtual environment
```

---

## Data Flow Overview

```
PDFs (input_pdf/)  +  data/db_pokedex.json
         |
         v
  extract_pokemon_database.py  ──>  output/initials/pokemons.json
  extract_abilities_database.py ──>  output/initials/abilities.json
  extract_move_database.py      ──>  output/initials/moves.json
         |
         v
  extractRedux_pokemons.py  ──>  output/redux/pokemons.json
  extractRedux_abilities.py ──>  output/redux/abilities.json
  extractRedux_moves.py     ──>  output/redux/moves.json
         |
         v
  extract_abilities_ptu_csv.py  ──>  output/pte/  +  output/finals/
  extract_move_ptu_csv.py       ──>  output/pte/  +  output/finals/
  extractRedux_pokemons.py      ──>  output/pte/  +  output/finals/
         |
         v
  generate_poke_pdf.py  ──>  output/pdf_temp/*.pdf  +  output/pdf/pokedex.pdf
```

---

## Shell Scripts (entry points)

These are the main entry points for running the full pipeline. Run them from the project root with the virtual environment **already activated**.

---

### `generate_abilities.sh`

Runs the full abilities pipeline in order.

```bash
bash generate_abilities.sh
```

**What it does:**
1. `extract_abilities_database.py` — Parses `input_pdf/Abilities.pdf` → `output/initials/abilities.json`
2. `extractRedux_abilities.py` — Merges with Redux engine abilities → `output/redux/abilities.json`
3. `extract_abilities_ptu_csv.py` — Adds PTU abilities from CSV → `output/pte/` and `output/finals/`

**Outputs:** `output/finals/abilities.json`, `output/finals/abilities.csv`

---

### `generate_moves.sh`

Runs the full moves pipeline in order.

```bash
bash generate_moves.sh
```

**What it does:**
1. `extract_move_database.py input_pdf/Moves.html -o move.csv` — Parses HTML move list → `output/initials/moves.json`
2. `extractRedux_moves.py` — Merges with Redux engine moves → `output/redux/moves.json`
3. `extract_move_ptu_csv.py` — Adds PTU moves from CSV → `output/pte/` and `output/finals/`

**Outputs:** `output/finals/moves.json`, `output/finals/moves.csv`

---

### `generate_pokemons.sh`

Runs the full Pokemon pipeline in order. This requires the abilities and moves pipelines to have been run first.

```bash
bash generate_pokemons.sh
```

**What it does:**
1. `extract_pokemon_database.py` — Parses all source PDFs → `output/initials/pokemons.json`
2. `extractRedux_pokemons.py` — Merges with Redux engine species data → `output/redux/`, `output/pte/`, `output/finals/`
3. `generate_poke_pdf.py` — Generates PDF character sheets for every Pokemon

**Outputs:** `output/finals/pokemons.json`, `output/pdf/pokedex.pdf`, individual PDFs in `output/pdf_temp/`

**Prerequisites:** Run `generate_abilities.sh` and `generate_moves.sh` first.

---

## Extraction Scripts

These scripts perform the initial extraction from source PDFs and HTML files.

---

### `extract_pokemon_database.py`

Parses all source Pokedex PDFs and produces the initial Pokemon database.

**How to run:**
```bash
python extract_pokemon_database.py
```

**Inputs:**
- `input_pdf/pokedex1-7_final_version.pdf` — Generations 1–7 (pages 14–865)
- `input_pdf/GalarDex + Armor_Crown.pdf` — Galar region (pages 2–120)
- `input_pdf/Gen 9 Homebrew Dex.pdf` — Gen 9 custom (pages 3–116)
- `input_pdf/Gen9 DLC.pdf` — Gen 9 DLC content (pages 1–19)
- `input_pdf/InsurgenceDex 1.05.pdf` — Pokemon Insurgence (pages 3–206)
- `input_pdf/HisuiDex.pdf` — Legends Arceus (pages 3–30)
- `input_pdf/Eveeloutions.pdf` — Eevee evolutions (pages 0–9)
- `input_pdf/Pokemon MegaDex.pdf` — Mega evolutions (pages 8–114)
- `data/db_pokedex.json` — Reference database for name matching

**Outputs:**
- `data/pokemon.json` — Raw merged list (intermediate)
- `output/initials/pokemons.json` — Cleaned list with OCR corrections and mega evolution data applied

**What it does:**
1. Loads the reference Pokedex database for name validation.
2. Calls `parse_extracted_text_gen8()` or `parse_extracted_text_gen9()` on each PDF across the specified page ranges.
3. Merges all parsed Pokemon into a single list.
4. Parses mega evolution data from the MegaDex PDF and attaches it to matching Pokemon.
5. Applies an OCR correction table (e.g. `"nolvern"` → `"noivern"`, `"salandlt"` → `"salandit"`) to fix scanning artefacts.
6. Writes the final corrected list to `output/initials/pokemons.json`.

---

### `extract_abilities_database.py`

Parses the abilities reference PDF and extracts name + effect text for each ability.

**How to run:**
```bash
python extract_abilities_database.py
```

**Inputs:**
- `input_pdf/Abilities.pdf`

**Outputs:**
- `output/initials/abilities.json`

**What it does:** Calls `parse_full_abilities()` on the abilities PDF and writes the resulting list of `{name, effect}` objects as JSON.

---

### `extract_move_database.py`

Parses an HTML file containing PTU moves and extracts structured move data.

**How to run:**
```bash
python extract_move_database.py <html_file> -o <output.csv> [options]
```

**Arguments:**

| Argument | Required | Description |
|---|---|---|
| `html_file` | Yes | Path to the HTML file (e.g. `input_pdf/Moves.html`) |
| `-o / --output` | Yes | Path for the output CSV (the JSON is always written to `output/initials/moves.json`) |
| `--type` | No | Filter by type (e.g. `Fire`, `Water`). Default: all |
| `--frequency` | No | Filter by frequency (e.g. `At-Will`, `Scene`). Default: all |
| `--damage_base` | No | Filter by damage base value. Default: all |
| `--damage_type` | No | Filter by damage type (`Physical`, `Special`, `Status`). Default: all |

**Example:**
```bash
python extract_move_database.py input_pdf/Moves.html -o move.csv
python extract_move_database.py input_pdf/Moves.html -o fire_moves.csv --type Fire
```

**Outputs:**
- `output/initials/moves.json` — Full move list as JSON (filters do NOT apply to the JSON; they only affect the CSV)

---

### `extract_pokemon_last_sheets.py`

Alternative extraction script for a newer "final" PDF format. Used when the source sheets have been reformatted and the standard Gen 8/9 parsers don't apply.

**How to run:**
```bash
python extract_pokemon_last_sheets.py
```

**Inputs:**
- `data/output_part1.pdf` — The final-format PDF (pages 0–200)
- `data/db_pokedex.json` — Reference database for name matching

**Outputs:**
- `output/finals/pokemons.json`

**What it does:** Same flow as `extract_pokemon_database.py` but uses `parse_extracted_text_final()` and reads from a different source PDF. The same OCR correction table is applied.

---

## Redux Integration Scripts

These scripts merge the initial extracted data with data from the Redux game engine (`data/reduxData_last.json`).

---

### `extractRedux_abilities.py`

Merges abilities extracted from the PDF with abilities defined in the Redux engine.

**How to run:**
```bash
python extractRedux_abilities.py
```

**Inputs:**
- `data/reduxData_last.json`
- `output/initials/abilities.json`

**Outputs:**
- `output/redux/abilities.json`

**What it does:**
1. Reads the Redux ability list and converts each entry to `{name, effect, id}`.
2. For each Redux ability, checks if it already exists in the initial list (by name, case-insensitive).
   - If it does not exist, appends it.
   - If it does exist, updates its `id` field with the Redux ID.
3. Sorts the final list alphabetically by name.

---

### `extractRedux_moves.py`

Merges moves extracted from HTML with moves defined in the Redux engine.

**How to run:**
```bash
python extractRedux_moves.py
```

**Inputs:**
- `data/reduxData_last.json`
- `output/initials/moves.json`

**Outputs:**
- `output/redux/moves.json`

**What it does:**
1. Reads the Redux move list.
2. For each Redux move not already in the initial list (by name, case-insensitive):
   - Maps type indices to type name strings using `reduxData_last.json["typeT"]`.
   - Maps the `split` field to a class string (`Physical`/`Special`/`Status`) using `reduxData_last.json["splitT"]`.
   - Uses the move description as the effect.
   - Fills frequency, AC, damage base, and range as `"TBD"` / `-1` since those aren't in the Redux data.
   - Appends the move with its Redux `id`.
3. If the move already exists, updates its `id` field.
4. Sorts the final list alphabetically.

---

### `extractRedux_pokemons.py`

The core integration script. Builds the full Pokemon roster by combining Redux engine species data with metadata extracted from the PDFs.

**How to run:**
```bash
python extractRedux_pokemons.py
```

**Inputs:**
- `data/reduxData_last.json`
- `output/redux/abilities.json`
- `output/redux/moves.json`
- `output/initials/pokemons.json`

**Outputs:**
- `output/redux/pokemons.json`
- `output/pte/pokemons.json`
- `output/finals/pokemons.json`

**What it does, per Redux species entry:**
1. **Stats** — Divides each base stat by 10 and rounds to convert from the Redux scale to the PTU scale.
2. **Types** — Maps type IDs to type name strings.
3. **Abilities** — Maps ability IDs to names. The first 2 go to `base_abilities`, the next 3 to `advanced_abilities`, the rest to `high_abilities`.
4. **Moves** — Maps `levelUpMoves` IDs to move names with their required levels.
5. **TM / Tutor / Egg moves** — Maps IDs to move names.
6. **Metadata** (height, weight, gender ratios, egg groups, capabilities, skills) — Looked up from `output/initials/pokemons.json` by matching the base name (stripping `redux_`, `alola_`, `hisuian_`, `therian_` prefixes).
7. After building the Redux list, any Pokemon from the initial list that doesn't already exist in the Redux list (by name) is appended.
8. Applies several name normalizations (e.g. `galarian` → `galar`, `alolan` → `alola`).

---

## PTU/PTE Merge Scripts

These scripts add PTU-specific content (from CSV files) on top of the Redux-merged data.

---

### `extract_abilities_ptu_csv.py`

Adds abilities from `data/ptuabilities.csv` to the Redux ability list.

**How to run:**
```bash
python extract_abilities_ptu_csv.py
```

**Inputs:**
- `output/redux/abilities.json`
- `data/ptuabilities.csv` — Columns: `Name`, `Effect`

**Outputs:**
- `output/pte/abilities.json`
- `output/pte/abilities.csv`
- `output/finals/abilities.json`
- `output/finals/abilities.csv`

**What it does:**
1. Loads the Redux abilities list.
2. Reads each row from the PTU CSV.
3. If the ability name already exists, appends it with a `_pte` suffix to avoid collision.
4. Otherwise, adds it as-is with `id = -1`.
5. Writes the combined list to both `pte/` and `finals/`.

---

### `extract_move_ptu_csv.py`

Adds moves from `data/ptumoves.csv` to the Redux move list, and infers dice rolls from the damage base.

**How to run:**
```bash
python extract_move_ptu_csv.py
```

**Inputs:**
- `output/redux/moves.json`
- `data/ptumoves.csv` — Columns: `Attack Name`, `Type`, `Class`, `Frequency`, `Range`, `AC`, `DB`, `Effect`, `Versatile Effect`, `Attack Tier`

**Outputs:**
- `output/pte/moves.json`
- `output/pte/moves.csv`
- `output/finals/moves.json`
- `output/finals/moves.csv`

**What it does:**
1. Loads Redux moves and builds a lookup table `{damage_base → roll}` from existing roll strings.
2. Reads each row from the PTU CSV and constructs a `FullMove` object.
3. For each PTU move, looks up its damage base in the roll table to fill the `roll` field. Exits with an error if a damage base has no known roll.
4. If the move name already exists in the Redux list, appends with `_pte` suffix.
5. Normalizes some common typos in frequency and class strings.
6. Writes the combined list to both `pte/` and `finals/`.

---

## PDF Generation Scripts

### `generate_poke_pdf.py`

Generates a PDF character sheet for every Pokemon in the final database and merges them into a single Pokedex PDF.

**How to run:**
```bash
python generate_poke_pdf.py
```

**Inputs:**
- `output/finals/pokemons.json` (or `output/redux/pokemons.json` — check the `load_pokemon()` call at the top)
- Pokemon artwork: looked up first in the local `images/` folder, then downloaded from pokemondb.net and cached

**Outputs:**
- `output/pdf_temp/<pokemon_name>.pdf` — One sheet per Pokemon
- `output/pdf/pokedex.pdf` — All sheets merged into one file

**What each sheet contains:**
- Pokemon name and types
- Base stats table (HP, ATK, DEF, SP.ATK, SP.DEF, SPD)
- Abilities (Base, Advanced, High)
- Capabilities and Skills tables
- Physical info (height, weight, gender ratio, egg group, diet, habitat)
- Level-up moves, TM moves, Tutor moves, Egg moves

**Image resolution strategy:**
1. Check `images/<name>.jpg` or `images/<name>.png`
2. Check `images/megadex_<name>.jpg/.png` for Mega forms
3. Download from `https://img.pokemondb.net/artwork/<name>.jpg`
4. Fall back to sprite from `https://forwardfeed.github.io/...` if artwork is unavailable
5. Cache downloaded images in `images/`

---

### `other_tools/generate_poke_pdf_new_redux.py`

An updated version of the PDF generator with Redux-specific formatting adjustments. Use this instead of `generate_poke_pdf.py` when generating sheets from Redux data.

**How to run:**
```bash
python other_tools/generate_poke_pdf_new_redux.py
```

Same inputs, outputs, and behavior as `generate_poke_pdf.py`.

---

## Utility Scripts (`other_tools/`)

---

### `other_tools/generate_pokemon.py`

Interactive wizard that generates a fully-configured Pokemon RPG character sheet as a Markdown file, applying level points, nature bonuses, and move selection.

**How to run:**
```bash
cd other_tools
python generate_pokemon.py
```

**Inputs (interactive prompts):**

| Prompt | Values |
|---|---|
| Pokemon name | Any name in `data/pokemon_old.json` |
| Level | Any positive integer |
| Rarity | `Normal`, `Shiny`, or `Platine` |
| Card | `None`, `Normal`, `Shiny`, or `Platine` |
| Nature (choose or roll) | See below |
| Stat points | Distribute `10 + level` points across 6 stats, or enter `default` for auto |
| Moves | Select up to 6 level-up moves by index, or type `fill` for auto |
| Egg moves | Enter up to 3 move names, type `stop` to finish |

**Nature selection:**
- Enter `y` to choose manually: provide the buffed stat then the lowered stat from `[HP, ATK, DEF, SPATK, SPDEF, SPD]`.
- Enter `n` to roll randomly: 3 natures are rolled using 2d6, you pick one by entering `1`, `2`, or `3`.

**Stat bonuses by rarity and card:**

| Rarity / Card | Bonus per stat | Nature bonus |
|---|---|---|
| Normal rarity | +0 | +2 to buffed stat |
| Shiny rarity | +2 | +2 to buffed stat |
| Platine rarity | +4 | +2 to buffed stat |
| Normal card | +1 | +1 extra to nature stat |
| Shiny card | +2 | +1 extra to nature stat |
| Platine card | +3 | +1 extra to nature stat |

**Outputs:**
- `<pokemon_name>.md` — A Markdown character sheet in the current folder

**Derived stats computed:**
- **Hit Points** = Level + (HP × 3) + 10
- **Phys Evade** = DEF ÷ 10
- **Spec Evade** = SP.DEF ÷ 10
- **Speed Evade** = SPD ÷ 10
- **Tutor Points** = Level ÷ 5 (floor)

---

### `other_tools/split_output.py`

Splits a large PDF into smaller chunks of a fixed page count.

**How to run:**
```bash
python other_tools/split_output.py
```

The script is configured by editing the `split_pdf()` call at the bottom of the file:

```python
split_pdf("output_pdf/merged_dex.pdf", max_pages=200, output_prefix="output")
```

| Parameter | Default | Description |
|---|---|---|
| `input_pdf` | `"output_pdf/merged_dex.pdf"` | Path to the PDF to split |
| `max_pages` | `200` | Maximum pages per output file |
| `output_prefix` | `"output"` | Prefix for output filenames |

**Outputs:** Files named `<prefix>_part1.pdf`, `<prefix>_part2.pdf`, etc.

---

### `other_tools/list_pokemons.py`

Generates a plain-text list of all Pokemon names with placeholders for move tracking.

**How to run:**
```bash
python other_tools/list_pokemons.py
```

**Inputs:**
- A `pokemon.json` file (path is hard-coded to a sibling web project — edit `json_pokes` in the script if needed)

**Outputs:**
- `list_pokemons.txt` — Each entry has the Pokemon name, a blank "level up moves" line, and a blank "ct / egg moves" line

---

### `other_tools/gen_sound_list.py`

Generates a list of moves grouped by sound type (for audio design purposes).

**How to run:**
```bash
python other_tools/gen_sound_list.py
```

**Outputs:** `sound_moves.txt`

---

### `other_tools/add_last_abilities.py`

Adds a batch of new abilities to the abilities database. Edit the script to add new entries before running.

**How to run:**
```bash
python other_tools/add_last_abilities.py
```

---

### `other_tools/extractAlreadyExistingRedux_abilities.py`

Identifies which Redux abilities already have a match in the extracted abilities list. Useful for auditing coverage.

**How to run:**
```bash
python other_tools/extractAlreadyExistingRedux_abilities.py
```

---

### `other_tools/extractMissingRedux_abilities.py`

Identifies Redux abilities that are NOT present in the extracted abilities list (missing entries).

**How to run:**
```bash
python other_tools/extractMissingRedux_abilities.py
```

---

### `other_tools/extraMissingPokemonsFromNewRedux.py`

Identifies Pokemon present in the new Redux data that are missing from the current database.

**How to run:**
```bash
python other_tools/extraMissingPokemonsFromNewRedux.py
```

---

### `other_tools/try_to_parse_img.py` / `try_to_parse_img_alola.py` / `try_to_parse_img_redux.py`

Image extraction utilities that pull Pokemon artwork from PDFs. Each variant targets a different PDF format (standard, Alola forms, Redux). Used for populating the `images/` folder from source PDFs rather than downloading.

**How to run:**
```bash
python other_tools/try_to_parse_img.py
```

---

### `other_tools/return_empty.py`

Returns empty/stub data structures. Used for testing and as a placeholder when a parser has no data to return.

---

## Core Modules

These are not run directly — they are imported by the scripts above.

---

### `parsers.py`

The PDF and HTML parsing engine. Contains all logic for extracting structured data from source files.

**Key functions:**

| Function | Description |
|---|---|
| `extract_two_columns_text(pdf_path, page_numbers)` | Extracts text from two-column PDFs by splitting the page width in half |
| `extract_one_column_text(pdf_path, page_to_read)` | Extracts single-column text, detecting section headers by bold formatting |
| `extract_one_column_imgs(pdf_path, page_to_read)` | Extracts and saves embedded images from a PDF page |
| `parse_extracted_text_gen8(input_pdf, indexes, db_names)` | Parses Gen 1–8 Pokemon data from the standard sheet format |
| `parse_extracted_text_gen9(input_pdf, indexes, db_names)` | Parses Gen 9 Pokemon data from the updated sheet format |
| `parse_extracted_text_final(input_pdf, indexes, db_names)` | Parses the final formatted version of the sheets |
| `parse_mega_evolutions(input_pdf, range_to_read)` | Extracts mega evolution data (types, abilities, stats, images) |
| `parse_full_abilities(filepath)` | Parses ability names and descriptions from a PDF |
| `parse_full_moves(filepath)` | Parses complete move data from an HTML file |
| `to_serializable(obj)` | Converts Pydantic models and nested objects to JSON-serializable dicts |

---

### `pokemon_data.py`

Pydantic v2 data models with validation. Ensures data integrity throughout the pipeline.

**Models:**

| Model | Key fields |
|---|---|
| `Capability` | `name`, `value` |
| `Skill` | `name`, `roll` |
| `Ability` | `name`, `effect`, `id` |
| `Move` | `name`, `level`, `type` |
| `MegaEvolution` | `types`, `ability`, `hp`, `atk`, `def_`, `sp_atk`, `sp_def`, `speed`, `image_path` |
| `Pokemon` | All 30+ fields: stats, types, abilities, moves, egg info, capabilities, skills, mega evolution |
| `FullMove` | `name`, `types`, `frequency`, `AC`, `damage_base`, `roll`, `m_class`, `range`, `effect`, `blessing`, `special_effect`, `contest_types`, `contest_effect`, `extra_lines`, `id` |

**Accepted values (used for validation):**
- `accepted_types`: all Pokemon types including custom ones
- `accepted_freqs`: `At-Will`, `EOT`, `Scene`, `Daily`, etc.
- `accepted_classes`: `Physical`, `Special`, `Status`
- `accepted_ACs`: `2` through `6`, plus `""` for no-roll moves

---

## Data Files Reference

| File | Description |
|---|---|
| `data/db_pokedex.json` | External reference database with English/Japanese names, used for name validation during PDF parsing |
| `data/reduxData_last.json` | Full Redux engine export: species, moves, abilities, types, evolutions |
| `data/ptuabilities.csv` | PTU-specific abilities not in the Redux engine |
| `data/ptumoves.csv` | PTU-specific moves not in the Redux engine |
| `input_pdf/Abilities.pdf` | Scanned PDF of ability descriptions |
| `input_pdf/Moves.html` | HTML table of all PTU moves |
| `input_pdf/*.pdf` | Source Pokedex PDFs for each region/game |
