"""
Module for validating file structure and data types in Janus Henderson test files.

Contains test cases to:
- Check for duplicate columns in test files.
- Verify that file columns match expected data types.

Uses pytest for parameterized testing across multiple files.
"""

import pytest
from helpers.utils_lib import (check_file_column_data_types, get_list_of_test_files_from_dir,
                               check_file_for_duplicate_cols)

class TestFileValidations:
    @pytest.mark.parametrize("file_to_verify", get_list_of_test_files_from_dir())
    def test_for_duplicate_columns(self, file_to_verify):
        """
        Test to ensure there are no duplicate columns in the given test file.

        Args:
            file_to_verify (Path): Path to the file to be validated. Provided by the pytest fixture.

        Asserts:
            True if no duplicate columns are found, otherwise fails the test.
        """

        assert check_file_for_duplicate_cols(file_to_verify)

    @pytest.mark.parametrize("file_to_verify", get_list_of_test_files_from_dir())
    def test_file_column_data_types(self, file_to_verify, data_definition, data_types_to_validate):
        """
        Test to verify that the columns in the given file match the expected data types.

        Args:
            file_to_verify (Path): Path to the file to be validated.
            data_definition (dict): Dictionary defining expected column data types.

        Asserts:
            True if all columns match the expected data types, otherwise fails the test.
        """
        assert check_file_column_data_types(file_to_verify, data_definition, data_types_to_validate)
