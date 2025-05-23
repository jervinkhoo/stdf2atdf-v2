# src/core/atdf_generator/handler.py
"""
Handles the generation of ATDF file content from processed data.
Consolidates logic from old src/core/atdf/handler.py related to
ATDF dictionary creation and file writing.
Uses formatters and templates from within this module.
"""
import sys
import logging
from typing import Dict, Any, List, Optional, IO

# Relative imports for components within atdf_generator
from .formatters import * # Import all formatting functions
from .templates import get_atdf_template # Import template access function

# Import from top-level utils
# from ...utils.epoch import get_datetime_from_epoch # Moved to formatters
# The function format_atdf_datetime_from_epoch is now imported via 'from .formatters import *'

logger = logging.getLogger(__name__)

# --- Function moved from src/core/atdf/handler.py ---
# Responsible for mapping STDF data to ATDF structure using formatters
def handle_atdf_entry(atdf_template: Dict, stdf_template: Dict) -> Dict:
    """Process ATDF record_type data based on STDF input."""
    record_type = atdf_template['record_type']
    atdf_processed_entry = {}

    # Map STDF field names to the corresponding formatting functions
    # This map uses the NEW function names (format_xxx)
    field_formatter_map = {
        ('pass_fail_flag', 'PTR'): format_pass_fail_flag,
        ('pass_fail_flag', 'MPR'): format_pass_fail_flag,
        ('alarm_flags', 'PTR'): format_alarm_flags,
        ('alarm_flags', 'MPR'): format_alarm_flags,
        ('programmed_state', 'PLR'): format_state_field,
        ('returned_state', 'PLR'): format_state_field,
        ('data_file_type', 'FAR'): format_data_file_type,
        ('pass_fail_code', 'PRR'): format_pass_fail_code,
        ('retest_code', 'PRR'): format_retest_code,
        ('abort_code', 'PRR'): format_abort_code,
        ('head_number', 'PCR'): format_head_or_site_number,
        ('head_number', 'HBR'): format_head_or_site_number,
        ('head_number', 'SBR'): format_head_or_site_number,
        ('head_number', 'TSR'): format_head_or_site_number,
        ('site_number', 'PCR'): format_head_or_site_number,
        ('site_number', 'HBR'): format_head_or_site_number,
        ('site_number', 'SBR'): format_head_or_site_number,
        ('site_number', 'TSR'): format_head_or_site_number,
        ('limit_compare', 'PTR'): format_limit_compare,
        ('limit_compare', 'MPR'): format_limit_compare,
        ('pass_fail_flag', 'FTR'): format_ftr_pass_fail_flag,
        ('alarm_flags', 'FTR'): format_ftr_alarm_flags,
        ('relative_address', 'FTR'): format_ftr_relative_address,
        ('generic_data', 'GDR'): format_generic_data,
        ('mode_array', 'PLR'): format_mode_array,
        ('radix_array', 'PLR'): format_radix_array,
        ('states_array', 'MPR'): format_states_array
    }

    for atdf_field, atdf_info in atdf_template['fields'].items():
        stdf_ref = atdf_info.get('stdf')
        value = None # Default value

        if isinstance(stdf_ref, (list, tuple)):
            # Handle cases where multiple STDF fields map to one ATDF field
            try:
                stdf_values = [stdf_template['fields'][field]['value'] for field in stdf_ref]
                key = (atdf_field, record_type)
                formatter = field_formatter_map.get(key)
                if formatter:
                    value = formatter(stdf_values)
                else:
                    # If no specific formatter, maybe join or handle differently?
                    # For now, set to None if no formatter defined for list/tuple input.
                    value = None
                    logger.debug(f"No specific formatter found for list/tuple input {stdf_ref} for {atdf_field} in {record_type}")
            except KeyError as e:
                logger.warning(f"Missing STDF field {e} referenced by ATDF field {atdf_field} in {record_type}")
                value = None # Assign None if source data is missing

        elif isinstance(stdf_ref, str):
            # Handle single STDF field mapping
            try:
                stdf_value = stdf_template['fields'][stdf_ref]['value']
                key = (atdf_field, record_type)
                formatter = field_formatter_map.get(key)
                if formatter:
                    value = formatter(stdf_value)
                else:
                    # Use default formatter if no specific one is found
                    value = format_default_value(stdf_value)
            except KeyError as e:
                 logger.warning(f"Missing STDF field {e} referenced by ATDF field {atdf_field} in {record_type}")
                 value = None # Assign None if source data is missing
            
        elif stdf_ref is None and atdf_field == 'atdf_version' and record_type == 'FAR':
            # Handle special case for ATDF version in FAR
            value = 2 # Default ATDF version
        
        # Assign the processed value (could be None)
        atdf_info['value'] = value
        atdf_processed_entry[atdf_field] = value

    return atdf_processed_entry


# Helper function to format values for ATDF text output based on field type
def _format_value_for_atdf_text(field_name: str, value: Any, record_type: str) -> str:
    """
    Formats a Python value (potentially list or list of lists) into the
    correct string representation for the ATDF text file based on field name.
    """
    if value is None:
        return ""

    # Handle specific array formats based on field name and record type
    if field_name == 'PROGRAMMED_STATE' and record_type == 'PLR':
        if isinstance(value, (list, tuple)) and all(isinstance(sublist, (list, tuple)) for sublist in value):
            # List of lists format: inner comma, outer slash
            group_strings = [','.join(map(str, group)) for group in value]
            return '/'.join(group_strings)
    elif field_name == 'RETURNED_STATE' and record_type == 'PLR':
         if isinstance(value, (list, tuple)) and all(isinstance(sublist, (list, tuple)) for sublist in value):
            # List of lists format: inner comma, outer slash
            group_strings = [','.join(map(str, group)) for group in value]
            return '/'.join(group_strings)
    elif field_name == 'GENERIC_DATA' and record_type == 'GDR':
        if isinstance(value, (list, tuple)):
            # Simple list format: pipe separator
            return '|'.join(map(str, value))
    elif field_name == 'MODE_ARRAY' and record_type == 'PLR':
         if isinstance(value, (list, tuple)):
            # Simple list format: comma separator
            return ','.join(map(str, value))
    elif field_name == 'RADIX_ARRAY' and record_type == 'PLR':
         if isinstance(value, (list, tuple)):
            # Simple list format: comma separator
            return ','.join(map(str, value))
    elif field_name == 'STATES_ARRAY' and record_type == 'MPR':
         if isinstance(value, (list, tuple)):
            # Simple list format: comma separator
            return ','.join(map(str, value))
    # Add other specific array/list formats here as needed

    # Default handling for scalar types or lists that don't need special joining
    # This will catch lists from format_default_value for example, joining with comma
    if isinstance(value, (list, tuple)):
         return ','.join(map(str, value))

    # Default string conversion for all other types (int, float, bool, str)
    return str(value)


# --- Function moved from src/core/atdf/handler.py ---
# Responsible for writing a processed ATDF entry to the file
def write_atdf_file(atdf_file: IO[str], atdf_processed_entry: Dict[str, Any], atdf_template: Dict[str, Any]):
    template_fields = atdf_template.get('fields', {})
    record_type = atdf_template.get('record_type', 'Unknown')
    record_header = atdf_template.get('header', f"{record_type}:")

    # 1. Write record header
    atdf_file.write(record_header)

    # 2. Handle records with no fields defined in their template (e.g., EPS)
    if not template_fields:
        atdf_file.write("\n")
        return

    field_order = list(template_fields.keys())

    # 3. Determine the index of the last field that actually needs to be written
    # A field needs to be written if it has a value (not None and not an empty string)
    # OR if it is marked as required in the template.
    last_field_to_write_index = -1
    for i in range(len(field_order) - 1, -1, -1):
        field_name_check = field_order[i]
        value_check = atdf_processed_entry.get(field_name_check)
        is_required_check = template_fields[field_name_check].get('req', False)

        if (value_check is not None and value_check != "") or is_required_check:
            last_field_to_write_index = i
            break

    # 4. If no fields need to be written (all optional and empty/None)
    #    This is the key fix for empty DTR records.
    if last_field_to_write_index == -1:
        atdf_file.write("\n")
        return

    # 5. Write field values up to and including the last_field_to_write_index
    for i in range(last_field_to_write_index + 1):
        field_name = field_order[i]
        value = atdf_processed_entry.get(field_name) # Get the (possibly raw) value

        # --- YOUR ORIGINAL TIMESTAMP FORMATTING LOGIC ---
        # This block is kept as per your existing code if it's needed here.
        # If handle_atdf_entry already formats timestamps, this 'if' might not trigger often for these fields.
        
        # if (field_name in ['modification_timestamp', 'setup_time', 'start_time', 'finish_time']
        #         and record_type in ['ATR', 'MIR', 'MRR', 'WIR', 'WRR'] # Used record_type from above
        #         and isinstance(value, int)):
        #     try:
        #         # Assuming format_atdf_datetime_from_epoch is imported or defined
        #         value_str = format_atdf_datetime_from_epoch(value)
        #         if value_str is None:
        #             value_str = ""
        #     except Exception as e:
        #          logger.error(f"Error formatting timestamp for {field_name} from epoch {value} in {record_type}: {e}")
        #          value_str = ""
        # else:
        #      value_str = "" if value is None else str(value)
             
        TIMESTAMP_FIELDS = {'modification_timestamp', 'setup_time', 'start_time', 'finish_time'}
        TIMESTAMP_RECORD_TYPES = {'ATR', 'MIR', 'MRR', 'WIR', 'WRR'}
        
        if field_name in TIMESTAMP_FIELDS and \
           record_type in TIMESTAMP_RECORD_TYPES and \
           isinstance(value, int):
            # format_atdf_datetime_from_epoch handles its own errors, logs them,
            # and returns None on failure. Defaults to UTC for conversion.
            formatted_dt = format_atdf_datetime_from_epoch(value)
            value_str = formatted_dt or ""  # Converts None to an empty string
        else:
            # Use the helper function for other field types
            value_str = _format_value_for_atdf_text(field_name, value, record_type)
        
        
             
        # --- END OF YOUR ORIGINAL TIMESTAMP FORMATTING LOGIC ---

        atdf_file.write(value_str)

        if i < last_field_to_write_index: # If not the last field being written
            atdf_file.write("|")
        # No 'else' needed here for the newline, it's handled after the loop

    # 6. Write the final newline for the record
    atdf_file.write("\n")

# Placeholder for the main function that will orchestrate using these handlers
# def generate_atdf_file(processed_records: Dict[str, List[Dict]], output_file_path: str):
#     logger.info(f"Starting ATDF file generation: {output_file_path}")
#     # Get ATDF templates
#     # Open output file
#     # Iterate through processed_records (in correct ATDF order if necessary)
#     # For each record:
#     #    Get the corresponding atdf_template
#     #    Call write_atdf_file(file_handle, record_dict, atdf_template)
#     logger.info(f"Finished ATDF file generation: {output_file_path}")
#     pass