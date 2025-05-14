# src/core/atdf_generator/handler.py
"""
Handles the generation of ATDF file content from processed data.
Consolidates logic from old src/core/atdf/handler.py related to
ATDF dictionary creation and file writing.
Uses formatters and templates from within this module.
"""
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
    }

    for atdf_field, atdf_info in atdf_template['fields'].items():
        stdf_ref = atdf_info.get('stdf')
        value = None # Default value

        if isinstance(stdf_ref, tuple):
            # Handle cases where multiple STDF fields map to one ATDF field
            try:
                stdf_values = [stdf_template['fields'][field]['value'] for field in stdf_ref]
                key = (atdf_field, record_type)
                formatter = field_formatter_map.get(key)
                if formatter:
                    value = formatter(stdf_values)
                else:
                    # If no specific formatter, maybe join or handle differently?
                    # For now, set to None if no formatter defined for tuple input.
                    value = None
                    logger.debug(f"No specific formatter found for tuple input {stdf_ref} for {atdf_field} in {record_type}")
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


# --- Function moved from src/core/atdf/handler.py ---
# Responsible for writing a processed ATDF entry to the file
def write_atdf_file(atdf_file: IO[str], atdf_processed_entry: Dict, atdf_template: Dict):
    """
    Write ATDF record to file using processed entry data while validating against template.

    Args:
        atdf_file: File handle to write to (opened in text mode).
        atdf_processed_entry: Dictionary containing the processed ATDF values.
        atdf_template: Template containing field requirements and record header.
    """
    template_fields = atdf_template.get('fields', {}) # Use .get for safety
    record_header = atdf_template.get('header', f"{atdf_template.get('record_type', 'Unknown')}:") # Use .get

    # Write record header
    atdf_file.write(record_header)

    if not template_fields:
        atdf_file.write("\n")
        return

    # Create a working list of field names based on the template order
    field_order = list(template_fields.keys())
    fields_to_write_dict = {}

    # Populate the dictionary with values from the processed entry, respecting template order
    for field_name in field_order:
         if field_name in atdf_processed_entry:
              fields_to_write_dict[field_name] = atdf_processed_entry[field_name]
         else:
              # Handle case where processed entry might be missing a field defined in template
              # This shouldn't happen if handle_atdf_entry populates all fields
              fields_to_write_dict[field_name] = None 
              logger.warning(f"Field '{field_name}' defined in template for {atdf_template.get('record_type')} but missing in processed entry.")


    # Determine the last field that needs to be written (non-empty or required)
    last_field_index = -1
    for i in range(len(field_order) - 1, -1, -1):
        key = field_order[i]
        value = fields_to_write_dict.get(key)
        # Check requirement based on the original template_fields definition
        is_required = template_fields[key].get('req', False) if key in template_fields else False

        if value not in [None, ""] or is_required:
            last_field_index = i
            break

    # Write field values up to the last required/non-empty one
    for index, field_name in enumerate(field_order):
        if index > last_field_index:
            break # Stop after the last field that needs writing

        value = fields_to_write_dict.get(field_name)

        # Handle timestamp conversion specifically for writing
        # Note: This assumes the value is still epoch int if it needs formatting.
        # If handle_atdf_entry already formatted it, this check needs adjustment.
        # Let's assume handle_atdf_entry provides the final value, except maybe dates.
        # Re-evaluating the date handling: get_datetime_from_epoch now returns datetime obj.
        # The formatting should happen HERE before writing, using the datetime obj.
        # This requires handle_atdf_entry to pass the raw epoch int or datetime obj.
        # Let's assume for now handle_atdf_entry provides the final STRING value
        # (except maybe for dates that need specific ATDF format).
        # We will move the date formatting logic here from utils/epoch.py later.

        # Temporary check based on field name - refine later
        if (field_name in ['modification_timestamp', 'setup_time', 'start_time', 'finish_time']
                and atdf_template['record_type'] in ['ATR', 'MIR', 'MRR', 'WIR', 'WRR']
                and isinstance(value, int)): # Check if it's still an int (epoch)
            try:
                # format_atdf_datetime_from_epoch now returns the correctly formatted ATDF string or None
                value_str = format_atdf_datetime_from_epoch(value)
                if value_str is None: # Handle case where conversion failed in format_atdf_datetime_from_epoch
                    value_str = ""
            except Exception as e: # Catch any unexpected error from format_atdf_datetime_from_epoch itself
                 logger.error(f"Error obtaining formatted timestamp for field {field_name} from epoch {value}: {e}")
                 value_str = "" # Default to empty string on error
        else:
             value_str = "" if value is None else str(value)


        atdf_file.write(value_str)

        # Add separator or newline
        if index == last_field_index:
            atdf_file.write("\n")
        else:
            atdf_file.write("|")

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