"""
Pytest configuration module for test file and data definition management.

Provides fixtures to:
- Retrieve test file paths from the project directory.
- Load data field definitions from an Excel file.
- Map file prefixes to their column code and type definitions for parameterized testing.
"""

import pytest
import pandas as pd
from pathlib import Path

from helpers.constants import REQU_DIR_PATH
from helpers.utils_lib import get_list_of_test_files_from_dir

@pytest.fixture(scope="class")
def t_files():
    """
    Retrieves a list of test file paths from the directory specified in the project constants.

    Returns:
        list: List of test file paths.
    """
    return get_list_of_test_files_from_dir()


@pytest.fixture(scope="class")
def d_def_file():
    """
    Loads the data field definitions from the Excel file specified by REQU_DIR_PATH.

    Returns:
        pd.DataFrame: DataFrame containing the data field definitions.
    """
    d_file = Path(REQU_DIR_PATH.joinpath("Data Fields_New.xlsx"))
    return pd.read_excel(d_file)


@pytest.fixture(scope="class")
def data_definition(t_files, d_def_file):
    """
    Creates a dictionary mapping file prefixes to their corresponding column code and type definitions.

    Args:
        t_files (list): List of test file paths.
        d_def_file (pd.DataFrame): DataFrame containing data field definitions.

    Returns:
        dict: Dictionary where each key is a file prefix and the value is another dictionary
        mapping column codes to their types.
    """
    dd_dict = {}
    for d_file in t_files:
        df_excel = d_def_file
        file_prefix = d_file.stem
        # Create dataframe with required columns only
        d_filter = df_excel["Column Code"].str.contains(file_prefix, na=False)
        df_subset = df_excel[d_filter][["Column Code", "Type"]]
        df_subset["Column Code"] = df_subset["Column Code"].str.replace(file_prefix+".", "c")

        # Convert dataframe to dictionary, with "Column Code" as key and "Type" as value.
        # Set Column Code as index, select column Type and then convert to dictionary.
        dd_dict[file_prefix] = (df_subset.set_index("Column Code")["Type"].to_dict())
    return dd_dict

@pytest.fixture(scope="function")
def data_types_to_validate():
    """
    Provides a list of data types to check in the test files.

    Returns:
        list: List of data types to check.
    """
    # Read this from config file later.

    # Pass data types to verify as a list.
    # Eg: data_types = ["ALPHANUMERICAL", "COUNTRY", "DATE",]
    # data_type = None for verifying all supported data types.
    # data_types = ["[Yes/No]"]
    data_types = None
    return data_types