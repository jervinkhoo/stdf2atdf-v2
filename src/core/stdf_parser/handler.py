# src/core/stdf_parser/handler.py
"""
Handles the parsing of STDF files, reading records, and unpacking data.
Consolidates logic from old src/core/stdf/handler.py and STDF-specific
parts of src/core/utils/setup.py.
"""

import logging
import struct
from typing import Dict, List, Optional, Any, Tuple, IO

# Relative imports for components within stdf_parser
from .unpackers import unpack_dtype, check_invalid_and_set_None_after_unpack
from .templates import get_record_types, create_stdf_mapping, get_stdf_template

# Import from top-level utils
from ...utils.files import get_file_handle # Assuming file handling happens here

logger = logging.getLogger(__name__)

# --- Functions moved from src/core/utils/setup.py ---

def setup_record_flags(records_to_process: Optional[List[str]]) -> Dict[str, bool]:
    """Set up record processing flags."""
    # Uses get_record_types from .templates
    record_flags = {record_type: True for record_type in get_record_types()}
    if records_to_process:
        # Initialize all to False if specific records are requested
        record_flags.update({record_type: False for record_type in get_record_types()})
        # Then set the requested ones to True
        record_flags.update({rec: True for rec in records_to_process if rec in record_flags})
    return record_flags

def determine_endianness(byte: bytes) -> str:
    """Determine endianness from STDF file byte."""
    # '>' = big-endian, '<' = little-endian
    return '>' if ord(byte) == 1 else '<'

def determine_file_params(stdf_file: IO[bytes]) -> Dict[str, Any]:
    """Determine STDF file parameters like endianness."""
    # Assuming stdf_file is an open binary file handle
    original_pos = stdf_file.tell()
    try:
        stdf_file.seek(4) # CPU_TYPE byte offset in FAR record
        byte = stdf_file.read(1)
        if not byte:
             raise EOFError("Could not read CPU_TYPE byte to determine endianness.")
        endianness = determine_endianness(byte)
    finally:
        stdf_file.seek(original_pos) # Reset position
    return {'endianness': endianness}

def read_record_header(stdf_file: IO[bytes], endianness: str) -> Optional[Tuple[int, int, int]]:
    """Read and parse STDF record header (REC_LEN, REC_TYP, REC_SUB)."""
    header = stdf_file.read(4)
    if not header:
        return None # End of file
    if len(header) < 4:
        logger.warning(f"Incomplete record header found at end of file. Expected 4 bytes, got {len(header)}.")
        return None # Incomplete header
    rec_len, rec_typ, rec_sub = struct.unpack(endianness + 'HBB', header)
    return rec_len, rec_typ, rec_sub

# --- Functions moved from src/core/stdf/handler.py ---


def handle_stdf_entry(stdf_template: Dict, data: bytes, endianness: str) -> Dict:
    """Process data fields within a single STDF record."""
    offset = 0
    stdf_processed_entry = {}
    
    data_len = len(data) # Length of the current record's data payload

    if data_len == 0: # Handles records like EPS
        logger.debug(f"Record type {stdf_template.get('record_type', 'Unknown')} has empty data payload. No fields to parse.")
        return stdf_processed_entry

    # Start from third field (skip rec_len, rec_typ, rec_sub which are in header)
    # Ensure 'fields' key exists in the template
    if 'fields' not in stdf_template:
        logger.error(f"Template for record type {stdf_template.get('record_type', 'Unknown')} is missing 'fields' key.")
        return {} # Or raise an error

    fields_to_process = list(stdf_template['fields'].items())[3:]

    for stdf_field, stdf_info in fields_to_process:
        # >>> THE FIX IS HERE <<<
        # Check if all data has been consumed BEFORE trying to parse the current field
        if offset >= data_len:
            logger.debug(f"No more data in record {stdf_template.get('record_type', 'Unknown')} to parse field '{stdf_field}'. "
                         f"Offset: {offset}, DataLen: {data_len}. Field will retain default/None.")
            break # Stop processing further fields for this record; all data consumed.
        # >>> END OF THE PRIMARY FIX <<<
        
        
        # Ensure stdf_info is a dictionary before accessing keys
        if not isinstance(stdf_info, dict):
             logger.warning(f"Invalid field info format for {stdf_field} in record {stdf_template.get('record_type', 'Unknown')}. Skipping field.")
             continue

        dtype = stdf_info.get('dtype')
        ref = stdf_info.get('ref')

        if dtype is None:
             logger.warning(f"Missing 'dtype' for field {stdf_field} in record {stdf_template.get('record_type', 'Unknown')}. Skipping field.")
             continue

        array_size = 0
        if ref:
            ref_field_info = stdf_template['fields'].get(ref)
            if isinstance(ref_field_info, dict) and 'value' in ref_field_info:
                 array_size = ref_field_info['value']
            else:
                 logger.warning(f"Reference field '{ref}' not found or invalid for field '{stdf_field}' in record {stdf_template.get('record_type', 'Unknown')}. Assuming array size 0.")
                 # Decide how to handle this - skip field, assume 0, raise error?
                 # Skipping field might be safest if array size is critical.
                 continue # Skip this field if array size reference is broken

        try:
            # Uses unpack_dtype from .unpackers
            value, offset = unpack_dtype(dtype, data, endianness, offset, array_size=array_size)
        except struct.error as e:
            logger.error(f"Struct unpack error for field {stdf_field} (dtype {dtype}) in record {stdf_template.get('record_type', 'Unknown')}: {e}. Offset: {offset}, Data length: {data_len}")
            # Decide how to handle - skip record, return partial, raise?
            # Returning partial data might be problematic. Let's skip the rest of the fields for this record.
            break
        except IndexError as e:
             logger.error(f"Index error (likely insufficient data) for field {stdf_field} (dtype {dtype}) in record {stdf_template.get('record_type', 'Unknown')}: {e}. Offset: {offset}, Data length: {data_len}")
             break # Stop processing this record
        except Exception as e: # Catch other potential unpack errors
             logger.error(f"Unexpected error unpacking field {stdf_field} (dtype {dtype}) in record {stdf_template.get('record_type', 'Unknown')}: {e}. Offset: {offset}, Data length: {data_len}")
             break # Stop processing this record


        stdf_info['value'] = value # Update the template dict (might be useful for subsequent refs)
        stdf_processed_entry[stdf_field] = value

        # Uses check_invalid_and_set_None_after_unpack from .unpackers
        # This function modifies stdf_info['value'] in place
        check_invalid_and_set_None_after_unpack(stdf_template, stdf_field)
        # Update the processed entry again if the value was set to None
        stdf_processed_entry[stdf_field] = stdf_info['value']


        if offset > data_len:
             logger.warning(f"Offset ({offset}) exceeded data length ({data_len}) after processing field {stdf_field} in record {stdf_template.get('record_type', 'Unknown')}. Record may be corrupt or truncated.")
             break # Stop processing this record
        elif offset == data_len:
             break # End of data for this record

    # Check if offset matches rec_len at the end (optional validation)
    # rec_len_from_header = stdf_template['fields']['rec_len']['value']
    # if offset != rec_len_from_header:
    #    logger.warning(f"Final offset ({offset}) does not match record length ({rec_len_from_header}) for record {stdf_template.get('record_type', 'Unknown')}")

    return stdf_processed_entry
# handle_stdf_entries function removed as per refactoring plan.
# Its logic will be integrated into src/converter.py process_record.
# --- Main Orchestration Function ---

# def parse_stdf_file(stdf_file_path: str, records_filter: Optional[List[str]] = None) -> Dict[str, List[Dict]]:
#     """
#     Parses a complete STDF file.
#
#     Args:
#         stdf_file_path (str): Path to the STDF file.
#         records_filter (Optional[List[str]]): Optional list of record types (e.g., ['MIR', 'PTR']) to process.
#                                              If None, all records are processed.
#
#     Returns:
#         Dict[str, List[Dict]]: A dictionary where keys are record type names (e.g., "MIR", "PTR")
#                                and values are lists of dictionaries, each representing a parsed record.
#                                This is the "Raw STDF Records" output.
#     """
#     logger.info(f"Starting STDF parsing for file: {stdf_file_path}")
#     stdf_mapping = create_stdf_mapping()
#     record_flags = setup_record_flags(records_filter)
#     endianness = '<' # Default assumption, will be determined by FAR
#
#     try:
#         # Uses get_file_handle from ...utils.files
#         with get_file_handle(stdf_file_path, 'rb') as stdf_file:
#             # Determine endianness from FAR (File Attributes Record), which must be the first record.
#             header_info = read_record_header(stdf_file, endianness) # Use default '<' first time
#             if header_info is None:
#                 logger.error(f"File {stdf_file_path} appears to be empty or has no header.")
#                 return stdf_processed_entries
#
#             rec_len, rec_typ, rec_sub = header_info
#             if not (rec_typ == 0 and rec_sub == 10): # Check if it's FAR
#                  logger.warning(f"First record is not FAR (Type 0, Sub 10). Found Type {rec_typ}, Sub {rec_sub}. Attempting to determine endianness.")
#                  # Attempt to determine endianness anyway, might fail if file is corrupt
#                  try:
#                       file_params = determine_file_params(stdf_file)
#                       endianness = file_params['endianness']
#                       logger.info(f"Determined endianness: {'Big-endian' if endianness == '>' else 'Little-endian'}")
#                       # Re-read header with potentially correct endianness
#                       stdf_file.seek(0) # Go back to start
#                       header_info = read_record_header(stdf_file, endianness)
#                       if header_info is None: raise EOFError("Empty file after seeking.")
#                       rec_len, rec_typ, rec_sub = header_info
#                  except Exception as e:
#                       logger.error(f"Could not determine endianness or re-read header from non-FAR start: {e}. Aborting parse.")
#                       return stdf_processed_entries # Return empty if we can't even start
#             else:
#                  # Process FAR to get actual endianness
#                  far_data = stdf_file.read(rec_len)
#                  if len(far_data) < rec_len:
#                       logger.error(f"Could not read full FAR record. Expected {rec_len} bytes, got {len(far_data)}. Aborting.")
#                       return stdf_processed_entries
#
#                  # Unpack CPU_TYPE (offset 0 in FAR data, after header) and STDF_VER (offset 1)
#                  cpu_type_byte = far_data[0:1] # Read the single byte for CPU_TYPE
#                  endianness = determine_endianness(cpu_type_byte)
#                  logger.info(f"Determined endianness from FAR: {'Big-endian' if endianness == '>' else 'Little-endian'}")
#                  # Optionally unpack and log STDF version
#                  # stdf_ver = struct.unpack(endianness + 'B', far_data[1:2])[0]
#                  # logger.info(f"STDF Version: {stdf_ver}")
#                  # We don't actually need to store FAR fields currently, just needed endianness.
#
#             # Reset file pointer to the start to read all records including FAR (if needed later)
#             # Or seek past FAR if we don't need it: stdf_file.seek(4 + rec_len)
#             stdf_file.seek(0)
#
#             # Main record processing loop
#             while True:
#                 header_info = read_record_header(stdf_file, endianness)
#                 if header_info is None:
#                     break # End of file
#
#                 rec_len, rec_typ, rec_sub = header_info
#                 record_data = stdf_file.read(rec_len)
#
#                 if len(record_data) < rec_len:
#                     logger.warning(f"Incomplete record data for Type {rec_typ}, Sub {rec_sub}. Expected {rec_len} bytes, got {len(record_data)}. Skipping record.")
#                     continue # Skip incomplete record
#
#                 try:
#                     # Uses get_stdf_template from .templates
#                     stdf_template = get_stdf_template(stdf_mapping, rec_typ, rec_sub)
#                     record_type_name = stdf_template['record_type']
#
#                     # Check if this record type should be processed
#                     if record_flags.get(record_type_name, False):
#                          # Directly call handle_stdf_entry instead of handle_stdf_entries
#                          processed_entry = handle_stdf_entry(stdf_template, record_data, endianness)
#                          stdf_processed_entries[record_type_name].append(processed_entry)
#
#                 except ValueError as e:
#                     # Raised by get_stdf_template if mapping not found
#                     logger.warning(f"Skipping unknown record type: {e}")
#                 except Exception as e:
#                     logger.error(f"Unexpected error processing record Type {rec_typ}, Sub {rec_sub}: {e}", exc_info=True)
#                     # Decide whether to continue or abort on unexpected errors
#
#     except FileNotFoundError:
#         logger.error(f"STDF file not found: {stdf_file_path}")
#         raise # Re-raise the exception
#     except EOFError as e:
#          logger.error(f"Unexpected end of file encountered in {stdf_file_path}: {e}")
#          # Return whatever was processed so far
#     except Exception as e:
#         logger.error(f"An unexpected error occurred during STDF parsing of {stdf_file_path}: {e}", exc_info=True)
#         raise # Re-raise unexpected exceptions
#
#     logger.info(f"Finished STDF parsing for file: {stdf_file_path}")
#     return stdf_processed_entries