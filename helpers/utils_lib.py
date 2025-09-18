"""
Test Utilities Module
This module contains helper functions for test cases:

"""

import pandas as pd
from helpers.constants import FILES_DIR_PATH

def check_file_for_duplicate_cols(file_name):
    """
    Checks a CSV file for duplicate columns by comparing column values.

    Args:
        file_name (str or Path): Path to the CSV file to check.

    Returns:
        bool: True if no duplicate columns are found, False otherwise.

    Raises:
        FileNotFoundError: If the file does not exist.
        pd.errors.EmptyDataError: If the file is empty.
        pd.errors.ParserError: If the file cannot be parsed.
    """

    df = pd.read_csv(file_name)
    duplicate_cols = set()
    no_of_cols = df.shape[1]
    for x in range(no_of_cols):
        starting_col = df.iloc[:, x].str.strip() if df.iloc[:, x].dtype == "object" else df.iloc[:, x]
        for y in range(x+1, no_of_cols):
            next_col = df.iloc[:, y].str.strip() if df.iloc[:, y].dtype == "object" else df.iloc[:, y]
            if starting_col.equals(next_col):
                duplicate_cols.add(df.columns.values[y])

    if len(duplicate_cols) > 0:
        print(f"File contains duplicate columns : {duplicate_cols}")
        return False
    else:
        return True


def get_list_of_test_files_from_dir():
    """
    Returns a list of files in the `files` directory whose names start with 'y_'.

    Returns:
        list: List of `Path` objects representing the files found.

    """
    list_of_files = [f_name for f_name in FILES_DIR_PATH.glob("y_*")]
    return list_of_files


def check_file_column_data_types(file_name, data_definition, types_to_check = None):
    """
    Checks if the columns in a CSV file match expected data types as defined in the data definition.

    Args:
        file_name (Path): Path to the CSV file to check.
        data_definition (dict): Dictionary mapping file stems to column data type definitions.
        types_to_check (list, optional): List of data types to check. If None, checks all supported types.

    Returns:
        bool: True if all checked columns match expected types, False otherwise.
    """

    if types_to_check is None:
        data_type = ["ALPHANUMERICAL", "COUNTRY", "DATE", "CLOSED SET OF OPTIONS", "PATTERN",
                          "CLOSED SET OF", "CURRENCY", "MONETARY", "NATURAL NUMBER", "[YES/NO]"]
    else:
        data_type = list(map(lambda x: x.upper(), types_to_check))

    df_data = pd.read_csv(file_name)
    result = {}
    print("File being processed is: ", file_name.stem)

    if data_definition[file_name.stem]:
        for col in df_data.columns:
            if col in data_definition[file_name.stem] and data_definition[file_name.stem].get(col) is not None:
                expected_type = data_definition[file_name.stem].get(col)

                # Only process if expected_type is in the list of types to check
                if expected_type.upper() not in data_type:
                    result[col] = "Skipped"
                    continue
                else:
                    if expected_type.upper() in ["ALPHANUMERICAL"]:
                        # Check if all values in the column are alphanumeric to avoid AttributeError
                        if df_data[col].dtypes == "object":
                            result[col] = True if df_data[col].str.isalnum().all() else False
                        else:
                            result[col] = False
                    elif expected_type.upper() == "COUNTRY":
                        result[col] = True if df_data[col].str.isalpha().all() else False
                    elif expected_type.upper() == "DATE":
                        result[col] = True if pd.api.types.is_datetime64_any_dtype(df_data[col]) else False
                    elif expected_type.upper() in ["CLOSED SET OF OPTIONS", "PATTERN", "CLOSED SET OF"]:
                        result[col] = True if pd.api.types.is_string_dtype(df_data[col]) else False
                    elif expected_type.upper() in ["CURRENCY", "MONETARY", "NATURAL NUMBER"]:
                        result[col] = True if (pd.api.types.is_float_dtype(df_data[col]) or
                                          pd.api.types.is_integer_dtype(df_data[col])) else False
                    elif expected_type.upper() == "[YES/NO]":
                        result[col] = True if df_data[col].isin(["Yes", "No"]).all() else False
                    else:
                        print(f"Data type {expected_type} not handled.")
                        result[col] = False
            else:
                print(f"Column {col} NOT found in data definition file for {file_name.stem}.")
                result[col] = False

        print("Result of data type checks: ", result)
        return all(result.values())
    else:
        print(f"No data definition found for file {file_name.stem}")
        return False
