---
name: Python implementation rules
description: Architecture, package layout, CSV schemas, and coding/testing rules for the Python class sorter in src/class_sorter and tests.
alwaysApply: true
---
## PYTHON IMPLEMENTATION — What Is Being Built

> This section governs all code under `src/class_sorter/` and `tests/`.
>
> The Python implementation is **designed independently**. Do not import, mirror, or
> assume any correspondence with Java field names, method names, class hierarchies,
> indexing conventions, or behavioral contracts. The two implementations solve the same
> problem in different languages with different designs.

### Python: Purpose and Scope
The Python implementation is a **backend CLI system** (no GUI) that:
1. Loads camper and class data from CSV files.
2. Validates the input data.
3. Assigns campers to classes based on preferences.
4. Exports the results to a CSV file.

### Python: Package Layout

```
src/class_sorter/
├── __init__.py
├── main.py                        # CLI entry point: loads data, builds objects, orchestrates assignment (assignment call is stubbed/commented out)
├── models/
│   ├── __init__.py
│   ├── campers.py                 # Camper dataclass
│   ├── classes.py                 # Class dataclass (owns its Section objects)
│   └── sections.py                # Section dataclass (owns its enrolled-camper list)
├── services/
│   ├── __init__.py
│   ├── data_loader.py             # load_campers() and load_classes() — pandas-based CSV parsing and validation
│   └── assignment.py              # Assignment logic — currently empty, not yet implemented
└── validators/                    # Directory exists but is empty; no validators have been written yet

tests/
├── __init__.py
├── test_campers.py
├── test_classes.py
├── test_sections.py
├── test_data_loader.py
└── test_main.py                   # Contains only a placeholder test (assert True)

inputs/
├── campers_input.csv
├── classes_input.csv
└── Classes-test.csv
```

### Python: CSV Input Schemas

**`inputs/campers_input.csv`**

| Column | Type | Notes |
|---|---|---|
| `first_name` | `str` | |
| `last_name` | `str` | |
| `cabin` | `str` | Cabin identifier (numeric string or alphanumeric, e.g. `"11"`, `"4L"`) |
| `age` | `int` | Must be a non-negative integer |
| `allowed_to_shoot` | `bool` | `"TRUE"`/`"FALSE"` in CSV; anything other than `"true"` (case-insensitive) is coerced to `False` |
| `preferences` | `list[str]` | Semicolon-delimited in CSV (e.g. `riflery;climbing;paintball`); parsed into a list by the loader |

The loader rejects: missing required columns, extra columns, non-integer `age`, negative `age`. An empty file (headers only) raises `ValueError`. A non-existent path raises `FileNotFoundError`.

**`inputs/classes_input.csv`**

| Column | Type | Notes |
|---|---|---|
| `class_id` | `str` | Unique name for the class (e.g. `"riflery"`, `"arts and crafts"`) |
| `minimum_age` | `int \| None` | Optional; empty cell means no age restriction |
| `shooting_permissions_needed` | `bool` | Same coercion rules as `allowed_to_shoot` |
| `capacity_a` … `capacity_d` | `int` | One column per period (`capacity_a`, `capacity_b`, `capacity_c`, `capacity_d`); empty cell or `0` means the class is not offered that period |

At least one `capacity_*` column must be present. The loader rejects: missing required columns, extra columns, non-integer capacity or `minimum_age` values, negative values in any numeric column. An empty file raises `ValueError`.

The loader produces a `period_capacities` dict (e.g. `{"A": 15, "B": 15}`) by uppercasing the suffix of each `capacity_*` column and dropping periods with capacity `0` or `NaN`. The raw `capacity_*` columns are dropped from the returned records.

### Python: Models (`models/`)

**`Camper` (`models/campers.py`)** — `@dataclass`
- Fields (all `__init__` params): `first_name: str`, `last_name: str`, `cabin: str`, `age: int`, `allowed_to_shoot: bool`, `preferences: deque[str]`.
- Auto-assigned in `__post_init__`: `id: int` (auto-incremented class-level counter `_id_counter`).
- Private state (not `__init__` params): `_enrolled_sections: dict[str, Section]` — keyed by period string.
- `preferences` is deduplicated on construction using `dict.fromkeys()` to preserve order; a `None` input becomes an empty `deque`.
- `enrolled_sections` property returns a shallow copy of `_enrolled_sections`.
- `add_section(section)` — adds to `_enrolled_sections` keyed by `section.period`.
- `remove_section(section)` — removes from `_enrolled_sections`; warns if period not found, raises `ValueError` on object mismatch.

**`Section` (`models/sections.py`)** — `@dataclass`
- Fields: `period: str`, `parent_class_id: str`, `capacity: int`.
- Private state: `_enrolled_campers: list[Camper]`.
- `enrolled_campers` property returns a shallow copy.
- `can_enroll(camper)` — returns `True` only if the section has remaining capacity AND the camper is not already enrolled in this period.
- `enroll_camper(camper)` — appends camper to roster and calls `camper.add_section(self)`; rolls back roster addition if `add_section` raises; returns `True` on success, `False` if `can_enroll` fails.
- `unenroll_camper(camper)` — removes camper from roster and calls `camper.remove_section(self)`; returns `True` on success, `False` if camper not found.
- `get_remaining_capacity()` — returns `capacity - len(_enrolled_campers)`.

**`Class` (`models/classes.py`)** — `@dataclass`
- Fields: `class_id: str`, `minimum_age: int | None`, `period_capacities: dict[str, int]`, `shooting_permissions_needed: bool` (default `False`).
- `__post_init__` creates one `Section` per entry in `period_capacities`; stored in private `_sections: dict[str, Section]`.
- `sections` property returns `_sections` directly.
- `get_section(period)` — returns the `Section` for that period, or `None`.
- `can_enroll(camper)` — returns `False` if camper is under `minimum_age` or if `shooting_permissions_needed` and `camper.allowed_to_shoot` is `False`; otherwise returns `True` if any section has remaining capacity.
- `retrieve_optimal_section(camper)` — finds periods not already in `camper.enrolled_sections`, sorts the corresponding sections by descending remaining capacity, and returns the best one (or `None` if none are available).

### Python: Services (`services/`)

**`data_loader.py`** — implemented.
- `load_campers(file_path) -> list[dict]`: reads CSV, validates structure and types, parses `preferences` from semicolon-delimited string to `list[str]`, returns list of record dicts ready for `Camper(**record)`.
- `load_classes(file_path) -> list[dict]`: reads CSV, validates structure and types, builds `period_capacities` dict, drops raw `capacity_*` columns, returns list of record dicts ready for `Class(**record)`.

**`assignment.py`** — **not yet implemented** (file exists but is empty). This service will assign campers to class sections based on ranked preferences. The call site in `main.py` is commented out.

### Python: `main.py`

Current state: loads CSVs via `data_loader`, constructs `Camper` and `Class` objects, prints counts. The assignment call (`sort_campers`) and CSV export (`export_results`) are stubbed out with comments. File paths are hardcoded to `inputs/classes_input.csv` and `inputs/campers_input.csv` relative to the working directory.

Future state: accept CLI arguments for input/output paths, call the assignment service, and write results to an output CSV.

### Python: Output Format

Not yet implemented. The intended output is a CSV written to `outputs/sorted_campers.csv`, but the schema and export logic have not been defined or built yet.

### Python: Tooling
- Package manager: **uv**. Use `uv add` to add dependencies. Do not edit `uv.lock`
  manually.
- Python version: **3.14** (pinned in `.python-version`).
- Build backend: `uv-build`.
- CLI entry point: `class-sorter` → `class_sorter.main:main`.
- Current dependencies: `pandas>=2.0.0`; dev dependency: `pytest>=9.1.1`.
- `script.py` at the repo root is a scratch file; it is not part of the package.

### Python: Testing
- All tests live in `tests/`. Framework is `pytest`.
- Test files follow the naming convention `test_<module>.py`.
- Tests must not rely on real CSV files at fixed filesystem paths. Use `pytest`'s
  `tmp_path` fixture or `io.StringIO` to supply test data in-memory.
- Every implemented module in `services/` and `models/` must have a corresponding test
  file.
- Do not hardcode absolute file paths in tests (the Java `AppTest.java` tests that
  reference `/Users/connorhitchings/Desktop/...` are an explicit anti-pattern).

**Test coverage by file:**

| Test file | Module under test | Status |
|---|---|---|
| `test_campers.py` | `models/campers.py` | Implemented |
| `test_sections.py` | `models/sections.py` | Implemented |
| `test_classes.py` | `models/classes.py` | Implemented (some tests commented out) |
| `test_data_loader.py` | `services/data_loader.py` | Implemented |
| `test_main.py` | `main.py` | Placeholder only (`assert True`) |

**Key testing patterns in use:**
- `csv_factory` fixture in `test_data_loader.py` uses `tmp_path` to write CSVs from a list of dicts via `pd.DataFrame(...).to_csv(...)`.
- Model tests construct objects directly from in-memory dicts; no file I/O.
- `@pytest.mark.parametrize` used in `test_data_loader.py` to test each numeric column's negative-value rejection independently.
- Boolean coercion of `allowed_to_shoot` to `False` for non-standard strings (e.g. `"MAYBE"`) is a documented and tested decision.