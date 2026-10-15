import pandas as pd


def load_campers(file_path):
    raw_campers = pd.read_csv(file_path)
    return raw_campers


def load_classes(file_path):
    raw_classes = pd.read_csv(file_path)

    # Validate records exist
    if len(raw_classes) == 0:
        raise ValueError("Classes must be populated in input file")

    # Validate dataframe structure
    expected_columns = [
        "class_id",
        "capacity_a",
        "capacity_b",
        "capacity_c",
        "capacity_d",
        "minimum_age",
        "shooting_permissions_needed",
    ]

    actual = set(raw_classes.columns)
    expected = set(expected_columns)

    missing = expected - actual
    extra = actual - expected

    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    if extra:
        raise ValueError(f"Unexpected columns: {sorted(extra)}")

    # Validate data types and handle empty cells
    numeric_columns = [
        "capacity_a",
        "capacity_b",
        "capacity_c",
        "capacity_d",
        "minimum_age",
    ]
    for col in numeric_columns:
        # Convert to numeric, treating NaN as 0 for validation purposes
        temp_series = pd.to_numeric(raw_classes[col], errors="coerce").fillna(0)

        # Check if all values (after conversion) are integers
        if not (temp_series == temp_series.astype(int)).all():
            raise TypeError(f"Column {col} must contain integer values")

        # Actually convert the column to have proper integer type with NaN for missing values
        raw_classes[col] = pd.to_numeric(raw_classes[col], errors="coerce")

    # Validate that numeric columns are non-negative
    for col in ["capacity_a", "capacity_b", "capacity_c", "capacity_d", "minimum_age"]:
        if (raw_classes[col] < 0).any():
            raise ValueError(f"Column {col} must contain non-negative values")

    # Pick a validation method
    # col = 'shooting_permissions_needed'
    # mapping = {'true': True, 'false': False, '': False, 'nan': False}

    # normalized = raw_classes[col].astype(str).str.strip().str.lower()

    # invalid = normalized[~normalized.isin(mapping)].unique()
    # if len(invalid):
    #     raise ValueError(f"{col} must be true/false or blank, got: {list(invalid)}")

    # raw_classes[col] = normalized.map(mapping)

    # # Validate shooting_permissions_needed is a boolean column (with blanks as False)
    # raw_classes['shooting_permissions_needed'] = raw_classes['shooting_permissions_needed'].astype(str).str.lower()

    # # Replace blank/NaN values with False
    # raw_classes['shooting_permissions_needed'] = raw_classes['shooting_permissions_needed'].replace('', False)
    # raw_classes['shooting_permissions_needed'] = raw_classes['shooting_permissions_needed'].fillna(False)

    # # Check if all values are boolean
    # if not raw_classes['shooting_permissions_needed'].apply(lambda x: isinstance(x, bool)).all():
    #     invalid_vals = raw_classes[~raw_classes['shooting_permissions_needed'].apply(lambda x: isinstance(x, bool))]['shooting_permissions_needed'].unique()
    #     raise ValueError(f"shooting_permissions_needed must contain boolean values (True/False): {invalid_vals}")

    return raw_classes
