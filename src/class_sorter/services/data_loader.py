import pandas as pd
import numpy as np


def load_campers(file_path):
    raw_campers = pd.read_csv(file_path)

    # Validate records exist
    if len(raw_campers) == 0:
        raise ValueError("Campers must be populated in input file")

    # Validate dataframe structure
    expected_columns = [
        "first_name",
        "last_name",
        "cabin",
        "age",
        "allowed_to_shoot",
        "preferences"
        ]

    actual = set(raw_campers.columns)
    expected = set(expected_columns)

    missing = expected - actual
    extra = actual - expected

    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    if extra:
        raise ValueError(f"Unexpected columns: {sorted(extra)}")

    # Validate data types and handle empty cells
    numeric_columns = ["age"]
    for col in numeric_columns:
        # Convert to numeric, treating NaN as 0 for validation purposes
        temp_series = pd.to_numeric(raw_campers[col], errors="coerce").fillna(0)

        # Check if all values (after conversion) are integers
        if not (temp_series == temp_series.astype(int)).all():
            raise TypeError(f"Column {col} must contain integer values")

        # Actually convert the column to have proper integer type with NaN for missing values
        raw_campers[col] = pd.to_numeric(raw_campers[col], errors="coerce")

    col = "allowed_to_shoot"
    mapping = {"true": True, "false": False, "": False, "nan": False}

    # Coerce 'allowed_to_shoot' to boolean: Only 'true' becomes True, everything else is False
    col = "allowed_to_shoot"
    normalized = raw_campers[col].astype(str).str.strip().str.lower()
    # Map the values
    raw_campers[col] = normalized.map(mapping).fillna(False).astype(bool)

    text_columns = [
        "first_name",
        "last_name",
        "cabin",
        "preferences"
    ]
    for col in text_columns:
        raw_campers[col] = raw_campers[col].astype(str)

    # Convert preferences string into a list of strings
    raw_campers['preferences'] = raw_campers['preferences'].astype(str).str.split(';')


    return raw_campers.replace({np.nan: None}).to_dict(orient='records')


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

    col = "shooting_permissions_needed"
    mapping = {"true": True, "false": False, "": False, "nan": False}

    # Coerce 'shooting_permissions_needed' to boolean: Only 'true' becomes True, everything else is False
    normalized = raw_classes[col].astype(str).str.strip().str.lower()
    # Map the values
    raw_classes[col] = normalized.map(mapping).fillna(False).astype(bool)

    text_columns = ["class_id"]
    for col in text_columns:
        raw_classes[col] = raw_classes[col].astype(str)

    raw_classes.replace({np.nan: None})
    return raw_classes
