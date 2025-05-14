# src/utils/files.py
"""Utilities for file handling operations."""
import gzip
from pathlib import Path
import logging
from typing import List, Optional # Added Optional
from contextlib import contextmanager # Added contextmanager

# Note: 'contextlib.contextmanager' and 'struct' were not needed for the selected functions.
# 'struct' is still not needed.

logger = logging.getLogger(__name__)

# def get_file_handle(file_path: str, mode: str): # This function is defined below by the moved code.
# This is the original get_file_handle, which is identical to the one moved from core.
# We will keep the one that was part of the moved block for simplicity, assuming it's tested with managed_files.
# The one at lines 15-20 will be effectively replaced by the one within the appended block.
# For clarity, I will remove this original one and keep the one that came with managed_files.
# Actually, the appended code uses get_file_handle. The original get_file_handle is fine.
# The appended code for managed_files calls get_file_handle.
# The file content shows get_file_handle at 15-20, then is_binary at 23-25, then is_file at 28-30.
# Then find_stdf_files at 33-41.
# Then validate_input_file at 46-51.
# Then the appended block starts with @contextmanager for managed_files.
# The appended block also has its own get_file_handle, is_binary, reset_and_check_binary.
# This means get_file_handle and is_binary are now duplicated.

# Let's keep the first definitions and remove the later ones that were appended if they are duplicates.
# The `managed_files` was appended. It calls `get_file_handle` and `reset_and_check_binary`.
# `reset_and_check_binary` calls `is_binary`.
# So, we need `get_file_handle`, `is_binary`, `reset_and_check_binary` to be defined *before* `managed_files`.

# Current structure after previous insert:
# 1. Original get_file_handle (lines 15-20)
# 2. Original is_binary (lines 23-25)
# 3. Original is_file (lines 28-30)
# 4. Original find_stdf_files (lines 33-41) - TO BE REMOVED
# 5. Original validate_input_file (lines 46-51)
# 6. Appended @contextmanager managed_files (starts line 52) - This calls get_file_handle, reset_and_check_binary
# 7. Appended is_binary (lines 74-76) - DUPLICATE, TO BE REMOVED
# 8. Appended reset_and_check_binary (lines 79-84) - This calls is_binary

# The `get_file_handle` at lines 15-20 is fine and used by the appended `managed_files`.
# The `is_binary` at lines 23-25 is fine and used by the appended `reset_and_check_binary`.

# Removing find_stdf_files (lines 33-41)
# Removing the second (appended) is_binary (lines 74-76)

# Cleaned up comments
def get_file_handle(file_path: str, mode: str):
    """Get appropriate file handle for regular or gzip files."""
    file_extension = Path(file_path).suffix.lower()
    if file_extension == '.gz':
        return gzip.open(file_path, mode)
    return open(file_path, mode)

def is_binary(content: bytes) -> bool:
    """Check if content is binary."""
    return b'\x00' in content

def is_file(path: str) -> bool:
    """Check if path is a valid file."""
    return Path(path).is_file()

# Removed find_stdf_files function
# def find_stdf_files(path: Path) -> List[Path]:
#     """Find all STDF files in a directory and its subdirectories."""
#     if path.is_file():
#         return [path]
#
#     stdf_files = []
#     for pattern in ['*.stdf', '*.STDF']:
#         stdf_files.extend(path.rglob(pattern))
#     return sorted(stdf_files)  # Sort for predictable processing order

# Original comment for validate_input_file was:
# Note: This function originally imported 'is_file' from '.files'.
# Since 'is_file' is now in this same file, the relative import is no longer needed.
def validate_input_file(input_stdf_file: str) -> None:
    """Validate input STDF file existence."""
    if not is_file(input_stdf_file): # is_file is now local to this module
        message = f"File {input_stdf_file} does not exist"
        logger.error(message)
        raise ValueError(message)
@contextmanager
def managed_files(stdf_path: str, atdf_path: Optional[str] = None):
    """Context manager for handling file resources safely."""
    stdf_file = None
    atdf_file = None
    try:
        # Assumes get_file_handle is defined in this module (which it is)
        stdf_file = get_file_handle(stdf_path, 'rb')
        reset_and_check_binary(stdf_file) # Assumes reset_and_check_binary is defined in this module

        if atdf_path:
            atdf_file = get_file_handle(atdf_path, 'w')

        yield stdf_file, atdf_file

    finally:
        if stdf_file:
            stdf_file.close()
        if atdf_file:
            atdf_file.close()


# Removed duplicate is_binary function that was here.
# The first definition (lines 57-59) is kept.

def reset_and_check_binary(file_handle) -> None:
    """Reset file pointer and verify binary content."""
    file_handle.seek(0)
    if not is_binary(file_handle.read()): # Assumes is_binary is defined in this module
        raise ValueError("File content is not binary")
    file_handle.seek(0)