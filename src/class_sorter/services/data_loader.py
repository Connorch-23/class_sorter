import pandas as pd

def load_classes(file_path):
    raw_classes = pd.read_csv(file_path)
    
    # Validate dataframe structure
    expected_columns = [
        'class_id', 'capacity_a', 'capacity_b', 'capacity_c', 
        'capacity_d', 'minimum_age', 'shooting_permissions_needed'
    ]
    
    if not all(col in raw_classes.columns for col in expected_columns):
        missing_cols = [col for col in expected_columns if col not in raw_classes.columns]
        raise ValueError(f"Missing required columns: {missing_cols}")
    
    # Validate data types and handle empty cells
    numeric_columns = ['capacity_a', 'capacity_b', 'capacity_c', 'capacity_d', 'minimum_age']
    for col in numeric_columns:
        # Convert to numeric, treating NaN as 0 for validation purposes
        temp_series = pd.to_numeric(raw_classes[col], errors='coerce').fillna(0)
        
        # Check if all values (after conversion) are integers
        if not (temp_series == temp_series.astype(int)).all():
            raise TypeError(f"Column {col} must contain integer values")
        
        # Actually convert the column to have proper integer type with NaN for missing values
        raw_classes[col] = pd.to_numeric(raw_classes[col], errors='coerce')
    
    # Validate that numeric columns are non-negative
    for col in ['capacity_a', 'capacity_b', 'capacity_c', 'capacity_d', 'minimum_age']:
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