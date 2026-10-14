import pytest
import pandas as pd
from class_sorter.services.data_loader import load_classes


class TestLoadClasses:
    # ------------------------------------------------------------------
    # Fixtures
    # ------------------------------------------------------------------
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
                "capacity_a": 15, "capacity_b": 15, "capacity_c": 15, "capacity_d": 15,
                "minimum_age": 12,
                "shooting_permissions_needed": True,
            },
            {
                "class_id": "drama",
                "capacity_a": 15, "capacity_b": 15, "capacity_c": 15, "capacity_d": 15,
                "minimum_age": None,
                "shooting_permissions_needed": False,
            },
            {
                "class_id": "five_stand",
                "capacity_a": None, "capacity_b": 1, "capacity_c": 15, "capacity_d": 15,
                "minimum_age": 14,
                "shooting_permissions_needed": True,
            },
            {
                "class_id": "paintball",
                "capacity_a": 10, "capacity_b": 10, "capacity_c": 10, "capacity_d": None,
                "minimum_age": 12,
                "shooting_permissions_needed": True,
            },
        ]
 
    @pytest.fixture
    def csv_factory(self, tmp_path):
        """A factory to create CSVs with custom content for each test."""
 
        def _make_csv(rows, columns=None, filename="classes.csv"):
            path = tmp_path / filename
            pd.DataFrame(rows, columns=columns, dtype=object).to_csv(path, index=False)
            return path
 
        return _make_csv
 
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
    
    def test_returns_dataframe_with_expected_columns(self, valid_csv_path, expected_columns):
        """Every expected column is present in the returned DataFrame."""
        df = load_classes(valid_csv_path)
        assert list(df.columns) == expected_columns
    
    def test_single_row_csv(self, csv_factory):
        """Loader works correctly when the CSV contains exactly one data row."""
        row = [{
            "class_id": "archery",
            "capacity_a": 20, "capacity_b": 20, "capacity_c": 20, "capacity_d": 20,
            "minimum_age": 8,
            "shooting_permissions_needed": False,
        }]
        df = load_classes(csv_factory(row))
        assert len(df) == 1
        assert df.iloc[0]["class_id"] == "archery"
    
    # ------------------------------------------------------------------
    # Incorrect columns
    # ------------------------------------------------------------------

    def test_missing_column_raises_valueerror(self, csv_factory):
        """A single missing column triggers ValueError naming that column."""
        rows = [{
            # 'capacity_a' is intentionally absent
            "class_id": "archery",
            "capacity_b": 20, "capacity_c": 20, "capacity_d": 20,
            "minimum_age": 8,
            "shooting_permissions_needed": False,
        }]
        with pytest.raises(ValueError, match="capacity_a"):
            load_classes(csv_factory(rows))
    
    def test_missing_multiple_columns_lists_all(self, csv_factory):
        """When several columns are missing, ALL of them appear in the error message.

        The loader builds a list of every missing column, so the message
        must name each one — not just the first it encounters.
        """
        rows = [{
            # capacity_b, capacity_c, and minimum_age are all absent
            "class_id": "archery",
            "capacity_a": 20, "capacity_d": 20,
            "shooting_permissions_needed": False,
        }]
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
        [row.update({"capacity_e": 0, "maximum_age": 100}) for row in valid_rows]
        with pytest.raises(ValueError) as exc_info:
            load_classes(csv_factory(valid_rows))
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
        rows = [{
            "class_id": "archery",
            "capacity_a": "abc",   # <-- bad value
            "capacity_b": 20, "capacity_c": 20, "capacity_d": 20,
            "minimum_age": 8,
            "shooting_permissions_needed": False,
        }]
        # Loader does NOT raise; 'abc' is coerced to NaN then treated as 0
        df = load_classes(csv_factory(rows))
        assert pd.isna(df.iloc[0]["capacity_a"])
    
    def test_float_in_numeric_column_raises_typeerror(self, csv_factory):
        """A genuine decimal (e.g. 3.14) raises TypeError; a whole-number
        float (e.g. 15.0) is accepted because it compares equal to its int.
        """
        decimal_rows = [{
            "class_id": "archery",
            "capacity_a": 3.14,   # <-- not a whole number
            "capacity_b": 20, "capacity_c": 20, "capacity_d": 20,
            "minimum_age": 8,
            "shooting_permissions_needed": False,
        }]
        with pytest.raises(TypeError, match="capacity_a"):
            load_classes(csv_factory(decimal_rows))

        whole_rows = [{
            "class_id": "archery",
            "capacity_a": 15.0,   # <-- whole number written as float; should pass
            "capacity_b": 20, "capacity_c": 20, "capacity_d": 20,
            "minimum_age": 8,
            "shooting_permissions_needed": False,
        }]
        # Must not raise
        load_classes(csv_factory(whole_rows))
    
    # ------------------------------------------------------------------
    # Negative values
    # ------------------------------------------------------------------

    @pytest.mark.parametrize("col", ["capacity_a", "capacity_b", "capacity_c", "capacity_d", "minimum_age"])
    def test_negative_value_raises_valueerror(self, col, csv_factory):
        """Each numeric column rejects negative values independently.

        Parametrize runs this test once per column so a regression in
        one column cannot be hidden by a failure in another.
        """
        row = {
            "class_id": "archery",
            "capacity_a": 20, "capacity_b": 20, "capacity_c": 20, "capacity_d": 20,
            "minimum_age": 8,
            "shooting_permissions_needed": False,
        }
        row[col] = -1   # inject a negative into whichever column is under test
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
    
