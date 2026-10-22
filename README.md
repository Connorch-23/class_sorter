# Class Sorter

A Python CLI tool that assigns summer-camp campers to activity classes across
scheduling periods based on ranked preferences.

## How It Works

1. **Load** — Reads camper and class data from CSV files.
2. **Assign** — Runs a greedy, preference-ranked assignment algorithm across
   multiple random seeds and keeps the highest-scoring result.
3. **Export** — Writes a master roster CSV with each camper's assigned class
   per period and their satisfaction score.

### Scoring

Each camper receives a score based on how well their assignments matched their
ranked preferences. A 1st-choice match scores `1.0`, a 2nd-choice scores
`0.5`, a 3rd-choice scores `0.33`, and so on (`1 / rank`). The algorithm runs
across multiple random seeds and selects the run with the highest total score.

---

## Installation

Requires **Python 3.14+** and [uv](https://docs.astral.sh/uv/).

```bash
uv sync
```

---

## Usage

Place your input CSVs in the `inputs/` directory, then run:

```bash
uv run class-sorter
```

Results are saved to `outputs/sorted_campers.csv`.

---

## Input Files

### `inputs/campers_input.csv`

| Column | Type | Notes |
|---|---|---|
| `first_name` | `str` | |
| `last_name` | `str` | |
| `cabin` | `str` | e.g. `"11"`, `"4L"` |
| `age` | `int` | Must be non-negative |
| `allowed_to_shoot` | `bool` | `TRUE`/`FALSE`; anything else → `False` |
| `preferences` | `str` | Semicolon-delimited, e.g. `riflery;climbing;kayaking` |

### `inputs/classes_input.csv`

| Column | Type | Notes |
|---|---|---|
| `class_id` | `str` | Unique class name, e.g. `"riflery"` |
| `minimum_age` | `int \| empty` | Empty cell means no age restriction |
| `shooting_permissions_needed` | `bool` | Same coercion as above |
| `capacity_a` … `capacity_d` | `int \| empty` | Capacity per period; empty or `0` means not offered that period |

---

## Output File

### `outputs/sorted_campers.csv`

| Column | Notes |
|---|---|
| `id` | Auto-assigned camper ID |
| `last_name`, `first_name`, `cabin` | From input |
| `A`, `B`, `C`, `D` | Assigned class for each period |
| `score` | Camper's preference-satisfaction score |

---

## Project Structure

```
src/class_sorter/
├── main.py                  # CLI entry point
├── models/
│   ├── campers.py           # Camper dataclass
│   ├── classes.py           # Class dataclass
│   └── sections.py          # Section dataclass
└── services/
    ├── data_loader.py       # CSV parsing and validation
    ├── assignment.py        # Greedy assignment engine
    └── output_data.py       # CSV export

inputs/                      # Input CSVs
outputs/                     # Generated results (git-ignored)
tests/                       # pytest test suite
```

---

## Development

Run the test suite:

```bash
uv run pytest
```

Add a dependency:

```bash
uv add <package>
```