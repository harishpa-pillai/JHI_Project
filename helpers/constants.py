"""
Constants Module
Provides constants for managing directory paths in the test suite.
"""

from pathlib import Path
# Constants for managing Directory names.

FILES_DIR_NAME = "files"
REQU_DIR_NAME = "requirements"
ROOT_DIR_PATH = Path(__file__).resolve().parent.parent
FILES_DIR_PATH = ROOT_DIR_PATH.joinpath(FILES_DIR_NAME)
REQU_DIR_PATH = ROOT_DIR_PATH.joinpath(REQU_DIR_NAME)