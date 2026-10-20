import pandas as pd
import pytest
import logging


from class_sorter.services.data_loader import load_classes
from class_sorter.services.data_loader import load_campers

logger = logging.getLogger(__name__)


@pytest.fixture
def csv_factory(tmp_path):
    """A factory to create CSVs with custom content for each test."""

    def _make_csv(rows, columns=None, filename="classes.csv"):
        path = tmp_path / filename
        pd.DataFrame(rows, columns=columns, dtype=object).to_csv(path, index=False)
        return path

    return _make_csv


class TestLoadClasses:
    # Fixtures
    @pytest.fixture
    def expected_columns(self):
        """The exact header the loader expects, in file order."""
        return [
            "class_id",
            "minimum_age",
            "shooting_permissions_needed",
        ]


    @pytest.fixture
    def valid_rows(self):
        """Small, realistic dataset as a list of dicts (one dict per CSV row).

        Mirrors the real classes_input.csv, including its empty cells:
        drama has no minimum_age, five_stand has no capacity_a, and
        paintball has no capacity_d.
        """
        return [
            {
                "class_id": "riflery",
                "capacity_a": 15,
                "capacity_b": 15,
                "capacity_c": 15,
                "capacity_d": 15,
                "minimum_age": 12,
                "shooting_permissions_needed": True,
            },
            {
                "class_id": "drama",
                "capacity_a": 15,
                "capacity_b": 15,
                "capacity_c": 15,
                "capacity_d": 15,
                "minimum_age": None,
                "shooting_permissions_needed": False,
            },
            {
                "class_id": "five_stand",
                "capacity_a": None,
                "capacity_b": 1,
                "capacity_c": 15,
                "capacity_d": 15,
                "minimum_age": 14,
                "shooting_permissions_needed": True,
            },
            {
                "class_id": "paintball",
                "capacity_a": 10,
                "capacity_b": 10,
                "capacity_c": 10,
                "capacity_d": None,
                "minimum_age": 12,
                "shooting_permissions_needed": True,
            },
        ]

    @pytest.fixture
    def valid_csv_path(self, csv_factory, valid_rows):
        """Create a valid CSV file and return its path."""
        return csv_factory(valid_rows)

    # ------------------------------------------------------------------
    # Happy path
    # ------------------------------------------------------------------

    def test_loads_valid_csv(self, valid_csv_path):
        """Loader returns a DataFrame without raising on a well-formed CSV."""
        classes = load_classes(valid_csv_path)
        assert isinstance(classes, list)

    def test_returns_list_with_expected_columns(
        self, valid_csv_path, expected_columns
    ):
        """Every expected column is present in the returned DataFrame."""
        classes = pd.DataFrame(load_classes(valid_csv_path))
        assert set(expected_columns) - set(classes.columns) == set()

    def test_single_row_csv(self, csv_factory):
        """Loader works correctly when the CSV contains exactly one data row."""
        row = [
            {
                "class_id": "archery",
                "capacity_a": 20,
                "capacity_b": 20,
                "capacity_c": 20,
                "capacity_d": 20,
                "minimum_age": 8,
                "shooting_permissions_needed": False,
            }
        ]
        classes = load_classes(csv_factory(row))
        assert len(classes) == 1
        assert classes[0]["class_id"] == "archery"

    # ------------------------------------------------------------------
    # Incorrect columns
    # ------------------------------------------------------------------

    def test_missing_column_raises_valueerror(self, csv_factory):
        """A single missing column triggers ValueError naming that column."""
        rows = [
            {
                "class_id": "archery",
                'capacity_a': 20,
                "capacity_b": 20,
                "capacity_c": 20,
                "capacity_d": 20,
                #"minimum_age": 8,
                "shooting_permissions_needed": False,
            }
        ]
        with pytest.raises(ValueError, match="minimum_age"):
            load_classes(csv_factory(rows))

    def test_missing_multiple_columns_lists_all(self, csv_factory):
        """When several columns are missing, ALL of them appear in the error message.

        The loader builds a list of every missing column, so the message
        must name each one — not just the first it encounters.
        """
        rows = [
            {
                "class_id": "archery",
                'capacity_a': 20,
                "capacity_b": 20,
                "capacity_c": 20,
                "capacity_d": 20,
                #"minimum_age": 8,
                #"shooting_permissions_needed": False,
            }
        ]
        with pytest.raises(ValueError) as exc_info:
            load_classes(csv_factory(rows))
        error_message = str(exc_info.value)
        assert "minimum_age" in error_message
        assert "shooting_permissions_needed" in error_message

    def test_extra_columns_raises_value_error(self, csv_factory, valid_rows):
        """If any extra columns are passed through the CSV file, it raises ValueError.

        The loader builds a list of every missing column, so the message
        must name each one — not just the first it encounters.
        """
        rows = [row.copy() for row in valid_rows]
        for row in rows:
            row.update({"middle_name": 0, "maximum_age": 100})
        with pytest.raises(ValueError) as exc_info:
            load_classes(csv_factory(rows))
        error_message = str(exc_info.value)
        assert "middle_name" in error_message
        assert "maximum_age" in error_message

    # ------------------------------------------------------------------
    # Invalid numeric data
    # ------------------------------------------------------------------

    def test_non_numeric_in_capacity_raises_typeerror(self, csv_factory):
        """A non-numeric string in a capacity column does NOT raise — it documents
        a known gap in the loader.

        pd.to_numeric(..., errors='coerce') silently converts unreadable
        values to NaN, then fillna(0) turns them into 0, which passes the
        integer check. No TypeError is ever raised for strings like 'abc'.

        This test pins that current (permissive) behaviour so a future
        tightening of the loader is a conscious, visible change.
        """
        rows = [
            {
                "class_id": "archery",
                "capacity_a": "abc",  # <-- bad value
                "capacity_b": 20,
                "capacity_c": 20,
                "capacity_d": 20,
                "minimum_age": 8,
                "shooting_permissions_needed": False,
            }
        ]
        # Loader does NOT raise; 'abc' is coerced to NaN then treated as 0, left out of the periods dict
        classes = load_classes(csv_factory(rows))
        with pytest.raises(KeyError):
            classes[0]['period_capacities']['A']

    def test_float_in_numeric_column_raises_typeerror(self, csv_factory):
        """A genuine decimal (e.g. 3.14) raises TypeError; a whole-number
        float (e.g. 15.0) is accepted because it compares equal to its int.
        """
        decimal_rows = [
            {
                "class_id": "archery",
                "capacity_a": 3.14,  # <-- not a whole number
                "capacity_b": 20,
                "capacity_c": 20,
                "capacity_d": 20,
                "minimum_age": 8,
                "shooting_permissions_needed": False,
            }
        ]
        with pytest.raises(TypeError):
            load_classes(csv_factory(decimal_rows))

        whole_rows = [
            {
                "class_id": "archery",
                "capacity_a": 15.0,  # <-- whole number written as float; should pass
                "capacity_b": 20,
                "capacity_c": 20,
                "capacity_d": 20,
                "minimum_age": 8,
                "shooting_permissions_needed": False,
            }
        ]
        # Must not raise
        load_classes(csv_factory(whole_rows))

    # ------------------------------------------------------------------
    # Negative values
    # ------------------------------------------------------------------

    @pytest.mark.parametrize(
        "col", ["capacity_a", "capacity_b", "capacity_c", "capacity_d", "minimum_age"]
    )
    def test_negative_value_raises_valueerror(self, col, csv_factory):
        """Each numeric column rejects negative values independently.

        Parametrize runs this test once per column so a regression in
        one column cannot be hidden by a failure in another.
        """
        row = {
            "class_id": "archery",
            "capacity_a": 20,
            "capacity_b": 20,
            "capacity_c": 20,
            "capacity_d": 20,
            "minimum_age": 8,
            "shooting_permissions_needed": False,
        }
        row[col] = -1  # inject a negative into whichever column is under test
        with pytest.raises(ValueError, match=col):
            load_classes(csv_factory([row]))

    # ------------------------------------------------------------------
    # NaN / empty cells
    # ------------------------------------------------------------------

    def test_empty_numeric_cells_pass_validation(self, valid_csv_path):
        """Rows with missing numeric values pass all validation.

        valid_rows already contains three different real-world empty cells
        (drama's minimum_age, five_stand's capacity_a, paintball's
        capacity_d), so valid_csv_path exercises this without a separate
        CSV needing to be built.
        """
        # Should not raise
        df = load_classes(valid_csv_path)
        assert len(df) == 4

    # ------------------------------------------------------------------
    # Edge cases
    def test_empty_csv_with_only_headers_raises(self, csv_factory, expected_columns):
        """A CSV file with only headers raises an exception.

        There should always be at least one class put on by the camp.
        """
        with pytest.raises(ValueError, match="Classes must be populated in input file"):
            load_classes(csv_factory([], columns=expected_columns))

    def test_nonexistent_file_raises_filenotfounderror(self):
        """Passing a path that does not exist surfaces a FileNotFoundError.

        This is raised by pandas.read_csv before any of our own validation
        runs. The test documents the caller-facing contract: bad path → clear
        error, not a silent empty result.
        """
        with pytest.raises(FileNotFoundError):
            load_classes("/nonexistent/path/to/classes.csv")


class TestLoadCampers:
    # Fixtures

    @pytest.fixture
    def expected_columns(self):
        """The exact header the loader expects, in file order."""
        return [
            "first_name",
            "last_name",
            "cabin",
            "age",
            "allowed_to_shoot",
            "preferences"
        ]

    @pytest.fixture
    def valid_rows(self):
        """Small, realistic dataset as a list of dicts (one dict per CSV row).

        Mirrors the real classes_input.csv, including its empty cells:
        drama has no minimum_age, five_stand has no capacity_a, and
        paintball has no capacity_d.
        """
        return [
            {
                "first_name": "Tyrese",
                "last_name": "Allen",
                "cabin": "11",
                "age": 12,
                "allowed_to_shoot": "TRUE",
                "preferences": ["riflery", "climbing", "paintball", "kayaking", "riflery", "12 stand"],
            },
            {
                "first_name": "David",
                "last_name": "Atkins",
                "cabin": "11",
                "age": 13,
                "allowed_to_shoot": "TRUE",
                "preferences": ["paintball", "arts and crafts", "5 stand", "kayaking", "drama", "12 stand"],
            },
            {
                "first_name": "Abigail",
                "last_name": "Bach",
                "cabin": "4",
                "age": 12,
                "allowed_to_shoot": "TRUE",
                "preferences": ["riflery", "drama", "5 stand", "kayaking", "photography", "12 stand"],
            },
            {
                "first_name": "Elena ",
                "last_name": "Bishop",
                "cabin": "4",
                "age": 14,
                "allowed_to_shoot": "FALSE",
                "preferences": ["arts and crafts", "horses", "sports", "archery", "fishing", "12 stand"],
            },
            {
                "first_name": "Julia",
                "last_name": "Brissie",
                "cabin": "4",
                "age": 12,
                "allowed_to_shoot": "FALSE",
                "preferences": ["horses", "sports", "drama", "arts and crafts", "kayaking", "12 stand"],
            },
            {
                "first_name": "Danielle Mae",
                "last_name": "Casinillo",
                "cabin": "4L",
                "age": 15,
                "allowed_to_shoot": "FALSE",
                "preferences": ["archery", "newspaper", "arts and crafts", "sports", "5 stand", "12 stand"],
            },
            {
                "first_name": "Paisley",
                "last_name": "Clarke",
                "cabin": "13",
                "age": 14,
                "allowed_to_shoot": "FALSE",
                "preferences": ["photography", "drama", "fishing", "sports", "arts and crafts", "12 stand"],
            },
            {
                "first_name": "Miranda",
                "last_name": "Cole",
                "cabin": "4",
                "age": 13,
                "allowed_to_shoot": "FALSE",
                "preferences": ["drama", "archery", "newspaper", "fishing", "climbing", "12 stand"],
            },
            {
                "first_name": "Jennifer",
                "last_name": "Crews",
                "cabin": "4L",
                "age": 12,
                "allowed_to_shoot": "TRUE",
                "preferences": ["riflery", "sports", "horses", "photography", "archery", "12 stand"],
            },
            {
                "first_name": "Giulia",
                "last_name": "Duarte",
                "cabin": "13",
                "age": 13,
                "allowed_to_shoot": "TRUE",
                "preferences": ["drama", "fishing", "kayaking", "archery", "horses", "12 stand"],
            },
        ]

    @pytest.fixture
    def valid_csv_path(self, csv_factory, valid_rows):
        """Create a valid CSV file and return its path."""
        return csv_factory(valid_rows)

    # Happy path

    def test_loads_valid_csv(self, valid_csv_path):
        """Loader returns a DataFrame without raising on a well-formed CSV."""
        campers = load_campers(valid_csv_path)
        assert isinstance(campers, list)

    def test_returns_list_with_expected_columns(
        self, valid_csv_path, expected_columns
    ):
        """Every expected column is present in the returned DataFrame."""
        df = pd.DataFrame(load_campers(valid_csv_path))
        assert list(df.columns) == expected_columns

    def test_single_row_csv(self, csv_factory, valid_rows):
        """Loader works correctly when the CSV contains exactly one data row."""

        df = pd.DataFrame(load_campers(csv_factory(valid_rows[:1])))
        assert len(df) == 1
        assert not df.empty

    # Incorrect columns
    def test_missing_column_raises_valueerror(self, csv_factory, valid_rows):
        """A single missing column triggers ValueError naming that column."""
        row = {k: v for k, v in valid_rows[0].items() if k != "first_name"}
        with pytest.raises(ValueError, match="first_name"):
            load_campers(csv_factory([row]))

    def test_missing_multiple_columns_lists_all(self, csv_factory, valid_rows):
        """When several columns are missing, ALL of them appear in the error message.

        The loader builds a list of every missing column, so the message
        must name each one — not just the first it encounters.
        """
        missing_cols = ["first_name", "preferences", "age"]
        row = {k: v for k, v in valid_rows[0].items() if k not in missing_cols}

        with pytest.raises(ValueError) as exc_info:
            load_campers(csv_factory([row]))
        error_message = str(exc_info.value)
        for col in missing_cols:
            assert col in error_message

    def test_extra_columns_raises_value_error(self, csv_factory, valid_rows):
        """If any extra columns are passed through the CSV file, it raises ValueError.

        The loader builds a list of every missing column, so the message
        must name each one — not just the first it encounters.
        """
        dirty_rows = [row.copy() for row in valid_rows]
        for row in dirty_rows:
            row.update({"birthday": "10-24-2015", "nickname": "charlie"})
        with pytest.raises(ValueError) as exc_info:
            load_campers(csv_factory(dirty_rows))
        error_message = str(exc_info.value)
        assert "birthday" in error_message
        assert "nickname" in error_message

    def test_numeric_conversion_for_age(self, csv_factory, valid_rows):
        """
        The 'age' column is provided as strings in the CSV.
        Does the loader convert 'age' to an integer type?
        """
        df = pd.DataFrame(load_campers(csv_factory(valid_rows)))
        assert pd.api.types.is_integer_dtype(df["age"])
        assert df.iloc[0]["age"] == 12

    # ------------------------------------------------------------------
    # Negative values
    # ------------------------------------------------------------------

    def test_negative_value_raises_valueerror(self, csv_factory, valid_rows):
        """Each numeric column rejects negative values independently.

        Parametrize runs this test once per column so a regression in
        one column cannot be hidden by a failure in another.
        """
        row = valid_rows[0].copy()
        col = 'age'
        row[col] = -1  # inject a negative into whichever column is under test
        with pytest.raises(ValueError, match=col):
            load_campers(csv_factory([row]))

    def test_invalid_boolean_values(self, csv_factory, valid_rows):
        """
        DECISION REQUIRED: If 'allowed_to_shoot' contains 'maybe' or 'N/A',
        should the loader raise a ValueError, or coerce it to False?

        Implementation assumes the loader should be robust and coerce invalid
        boolean strings to False.
        """
        row = valid_rows[0].copy()
        row["allowed_to_shoot"] = "MAYBE"

        campers = load_campers(csv_factory([row]))
        # Expecting coercion to False for non-standard boolean strings
        assert not campers[0]["allowed_to_shoot"]

    # ------------------------------------------------------------------
    # Edge Cases
    # ------------------------------------------------------------------

    def test_empty_csv_with_only_headers_raises(self, csv_factory, expected_columns):
        """A CSV with only headers should raise a ValueError."""
        with pytest.raises(ValueError, match="Campers must be populated in input file"):
            load_campers(csv_factory([], columns=expected_columns))

    def test_nonexistent_file_raises_filenotfounderror(self):
        """Passing a bad path should surface FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            load_campers("/nonexistent/path/to/campers.csv")

    def test_empty_cells_handling(self, csv_factory, valid_rows):
        """Empty cells are handled as NaN/None by pandas."""
        # Create a row where the last name is empty
        row = valid_rows[0].copy()
        row["last_name"] = ""

        df = pd.DataFrame(load_campers(csv_factory([row])))
        # Check if the value is treated as a null/NaN value
        assert pd.isna(df.iloc[0]["last_name"])
