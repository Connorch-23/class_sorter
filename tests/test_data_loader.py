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
            "capacity_a",
            "capacity_b",
            "capacity_c",
            "capacity_d",
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
        df = load_classes(valid_csv_path)
        assert isinstance(df, pd.DataFrame)

    def test_returns_dataframe_with_expected_columns(
        self, valid_csv_path, expected_columns
    ):
        """Every expected column is present in the returned DataFrame."""
        df = load_classes(valid_csv_path)
        assert list(df.columns) == expected_columns

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
        df = load_classes(csv_factory(row))
        assert len(df) == 1
        assert df.iloc[0]["class_id"] == "archery"

    # ------------------------------------------------------------------
    # Incorrect columns
    # ------------------------------------------------------------------

    def test_missing_column_raises_valueerror(self, csv_factory):
        """A single missing column triggers ValueError naming that column."""
        rows = [
            {
                # 'capacity_a' is intentionally absent
                "class_id": "archery",
                "capacity_b": 20,
                "capacity_c": 20,
                "capacity_d": 20,
                "minimum_age": 8,
                "shooting_permissions_needed": False,
            }
        ]
        with pytest.raises(ValueError, match="capacity_a"):
            load_classes(csv_factory(rows))

    def test_missing_multiple_columns_lists_all(self, csv_factory):
        """When several columns are missing, ALL of them appear in the error message.

        The loader builds a list of every missing column, so the message
        must name each one — not just the first it encounters.
        """
        rows = [
            {
                # capacity_b, capacity_c, and minimum_age are all absent
                "class_id": "archery",
                "capacity_a": 20,
                "capacity_d": 20,
                "shooting_permissions_needed": False,
            }
        ]
        with pytest.raises(ValueError) as exc_info:
            load_classes(csv_factory(rows))
        error_message = str(exc_info.value)
        assert "capacity_b" in error_message
        assert "capacity_c" in error_message
        assert "minimum_age" in error_message

    def test_extra_columns_raises_value_error(self, csv_factory, valid_rows):
        """If any extra columns are passed through the CSV file, it raises ValueError.

        The loader builds a list of every missing column, so the message
        must name each one — not just the first it encounters.
        """
        rows = [row.copy() for row in valid_rows]
        for row in rows:
            row.update({"capacity_e": 0, "maximum_age": 100})
        with pytest.raises(ValueError) as exc_info:
            load_classes(csv_factory(rows))
        error_message = str(exc_info.value)
        assert "capacity_e" in error_message
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
        # Loader does NOT raise; 'abc' is coerced to NaN then treated as 0
        df = load_classes(csv_factory(rows))
        assert pd.isna(df.iloc[0]["capacity_a"])

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
        with pytest.raises(TypeError, match="capacity_a"):
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
            "preference_1",
            "preference_2",
            "preference_3",
            "preference_4",
            "preference_5",
            "preference_6",
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
                "preference_1": "riflery",
                "preference_2": "climbing",
                "preference_3": "paintball",
                "preference_4": "kayaking",
                "preference_5": "riflery",
                "preference_6": "12 stand",
            },
            {
                "first_name": "David",
                "last_name": "Atkins",
                "cabin": "11",
                "age": 13,
                "allowed_to_shoot": "TRUE",
                "preference_1": "paintball",
                "preference_2": "arts and crafts",
                "preference_3": "5 stand",
                "preference_4": "kayaking",
                "preference_5": "drama",
                "preference_6": "12 stand",
            },
            {
                "first_name": "Abigail",
                "last_name": "Bach",
                "cabin": "4",
                "age": 12,
                "allowed_to_shoot": "TRUE",
                "preference_1": "riflery",
                "preference_2": "drama",
                "preference_3": "5 stand",
                "preference_4": "kayaking",
                "preference_5": "photography",
                "preference_6": "12 stand",
            },
            {
                "first_name": "Elena ",
                "last_name": "Bishop",
                "cabin": "4",
                "age": 14,
                "allowed_to_shoot": "FALSE",
                "preference_1": "arts and crafts",
                "preference_2": "horses",
                "preference_3": "sports",
                "preference_4": "archery",
                "preference_5": "fishing",
                "preference_6": "12 stand",
            },
            {
                "first_name": "Julia",
                "last_name": "Brissie",
                "cabin": "4",
                "age": 12,
                "allowed_to_shoot": "FALSE",
                "preference_1": "horses",
                "preference_2": "sports",
                "preference_3": "drama",
                "preference_4": "arts and crafts",
                "preference_5": "kayaking",
                "preference_6": "12 stand",
            },
            {
                "first_name": "Danielle Mae",
                "last_name": "Casinillo",
                "cabin": "4L",
                "age": 15,
                "allowed_to_shoot": "FALSE",
                "preference_1": "archery",
                "preference_2": "newspaper",
                "preference_3": "arts and crafts",
                "preference_4": "sports",
                "preference_5": "5 stand",
                "preference_6": "12 stand",
            },
            {
                "first_name": "Paisley",
                "last_name": "Clarke",
                "cabin": "13",
                "age": 14,
                "allowed_to_shoot": "FALSE",
                "preference_1": "photography",
                "preference_2": "drama",
                "preference_3": "fishing",
                "preference_4": "sports",
                "preference_5": "arts and crafts",
                "preference_6": "12 stand",
            },
            {
                "first_name": "Miranda",
                "last_name": "Cole",
                "cabin": "4",
                "age": 13,
                "allowed_to_shoot": "FALSE",
                "preference_1": "drama",
                "preference_2": "archery",
                "preference_3": "newspaper",
                "preference_4": "fishing",
                "preference_5": "climbing",
                "preference_6": "12 stand",
            },
            {
                "first_name": "Jennifer",
                "last_name": "Crews",
                "cabin": "4L",
                "age": 12,
                "allowed_to_shoot": "TRUE",
                "preference_1": "riflery",
                "preference_2": "sports",
                "preference_3": "horses",
                "preference_4": "photography",
                "preference_5": "archery",
                "preference_6": "12 stand",
            },
            {
                "first_name": "Giulia",
                "last_name": "Duarte",
                "cabin": "13",
                "age": 13,
                "allowed_to_shoot": "TRUE",
                "preference_1": "drama",
                "preference_2": "fishing",
                "preference_3": "kayaking",
                "preference_4": "archery",
                "preference_5": "horses",
                "preference_6": "12 stand",
            },
        ]

    @pytest.fixture
    def valid_csv_path(self, csv_factory, valid_rows):
        """Create a valid CSV file and return its path."""
        return csv_factory(valid_rows)

    # Happy path

    def test_loads_valid_csv(self, valid_csv_path):
        """Loader returns a DataFrame without raising on a well-formed CSV."""
        df = load_campers(valid_csv_path)
        assert isinstance(df, pd.DataFrame)

    def test_returns_dataframe_with_expected_columns(
        self, valid_csv_path, expected_columns
    ):
        """Every expected column is present in the returned DataFrame."""
        df = load_campers(valid_csv_path)
        logger.warning(df.columns)
        logger.warning(expected_columns)
        assert list(df.columns) == expected_columns

    def test_single_row_csv(self, csv_factory, valid_rows):
        """Loader works correctly when the CSV contains exactly one data row."""

        df = load_campers(csv_factory(valid_rows[:1]))
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
        missing_cols = ["first_name", "preference_6", "age"]
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
            row.update({"preference_7": "paragliding", "nickname": "charlie"})
        with pytest.raises(ValueError) as exc_info:
            load_campers(csv_factory(dirty_rows))
        error_message = str(exc_info.value)
        assert "preference_7" in error_message
        assert "nickname" in error_message

    def test_numeric_conversion_for_age(self, csv_factory, valid_rows):
        """
        The 'age' column is provided as strings in the CSV.
        Does the loader convert 'age' to an integer type?
        """
        df = load_campers(csv_factory(valid_rows))
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
            load_classes(csv_factory([row]))

    def test_invalid_boolean_values(self, csv_factory, valid_rows):
        """
        DECISION REQUIRED: If 'allowed_to_shoot' contains 'maybe' or 'N/A',
        should the loader raise a ValueError, or coerce it to False?

        Implementation assumes the loader should be robust and coerce invalid
        boolean strings to False.
        """
        row = valid_rows[0].copy()
        row["allowed_to_shoot"] = "MAYBE"

        df = load_campers(csv_factory([row]))
        # Expecting coercion to False for non-standard boolean strings
        assert not df.iloc[0]["allowed_to_shoot"]

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
        """
        DECISION REQUIRED: If a preference column is empty (,,),
        should it be an empty string, None, or NaN?

        Implementation assumes empty cells are handled as NaN/None by pandas.
        """
        # Create a row where the 3rd preference is empty
        row = valid_rows[0].copy()
        row["preference_3"] = ""

        df = load_campers(csv_factory([row]))
        # Check if the value is treated as a null/NaN value
        assert pd.isna(df.iloc[0]["preference_3"])
