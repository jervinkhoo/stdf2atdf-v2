# src/core/atdf_generator/formatters.py
# Contains functions moved from src/core/atdf/parsers.py
# Renamed parse_xxx to format_xxx to better reflect their role here.

import datetime
import logging
import pytz # For timezone handling

logger = logging.getLogger(__name__)

def format_pass_fail_flag(stdf_values): # Renamed from parse_pass_fail_flag
    test_flg, parm_flg = int(stdf_values[0], 2), int(stdf_values[1], 2)
    test_flg_bit_6 = (test_flg >> 6) & 1
    test_flg_bit_7 = (test_flg >> 7) & 1
    parm_flg_bit_5 = (parm_flg >> 5) & 1
    if test_flg_bit_6 == 0:
        if test_flg_bit_7 == 0:
            return "P" if parm_flg_bit_5 == 0 else "A"
        else:
            return None
    else:
        return "F"

def format_alarm_flags(stdf_values): # Renamed from parse_alarm_flags
    test_flg, parm_flg = int(stdf_values[0], 2), int(stdf_values[1], 2)
    flags = {
        'A': (test_flg >> 0) & 1,
        'D': (parm_flg >> 1) & 1,
        'H': (parm_flg >> 3) & 1,
        'L': (parm_flg >> 4) & 1,
        'N': (test_flg >> 4) & 1,
        'O': (parm_flg >> 2) & 1,
        'S': (parm_flg >> 0) & 1,
        'T': (test_flg >> 3) & 1,
        'U': (test_flg >> 2) & 1,
        'X': (test_flg >> 5) & 1,
    }
    return ''.join([key for key, value in flags.items() if value]) if any(flags.values()) else None

# def process_atdf_record_data_state_field(chal, char): # Original commented out
#     """
#     Process state fields from STDF to ATDF format.
#     Combines characters by pairs or formats single characters into comma-separated strings.
#
#     Args:
#         chal (list): First character array list, may be None.
#         char (list): Second character array list, may be None.
#
#     Returns:
#         str: Combined state fields as '/'-separated string, with states comma-separated.
#     """
#     result = []
#
#     if chal is None:
#         for cha in char:
#             organized_string = ','.join([f"{c.replace(' ', '')}" for c in cha])
#             result.append(organized_string)
#     elif char is None:
#         for cha in chal:
#             organized_string = ','.join([f"{c.replace(' ', '')}" for c in cha])
#             result.append(organized_string)
#     else:
#         for cha_left, cha_right in zip(chal, char):
#             organized_string = ','.join(
#                 [f"{cl.replace(' ', '')}{cr.replace(' ', '')}" for cl, cr in zip(cha_left, cha_right)])
#             result.append(organized_string)
#
#     return '/'.join(result)

def format_state_field(stdf_values): # Renamed from parse_state_field
    """
    Process state fields from STDF to ATDF format.
    Combines characters by pairs or formats single characters into comma-separated strings.

    Args:
        chal (list): First character array list, may be None.
        char (list): Second character array list, may be None.

    Returns:
        str: Combined state fields as '/'-separated string, with states comma-separated.
    """
    chal, char = stdf_values[0], stdf_values[1]

    if chal is None:
        iterable = char
        format_function = lambda cha: ','.join([c.replace(' ', '') for c in cha])
    elif char is None:
        iterable = chal
        format_function = lambda cha: ','.join([c.replace(' ', '') for c in cha])
    else:
        iterable = zip(chal, char)
        format_function = lambda cha_pair: ','.join(
            [cl.replace(' ', '') + cr.replace(' ', '') for cl, cr in zip(cha_pair[0], cha_pair[1])]
        )

    result = [format_function(cha) for cha in iterable]

    return '/'.join(result)

def format_data_file_type(_): # Renamed from parse_data_file_type
    return 'A'

def format_pass_fail_code(stdf_value): # Renamed from parse_pass_fail_code
    binary_value = int(stdf_value, 2)
    bit_3 = (binary_value >> 3) & 1
    bit_4 = (binary_value >> 4) & 1
    if bit_4 == 0:
        return "P" if bit_3 == 0 else "F"
    return "F"

def format_retest_code(stdf_value): # Renamed from parse_retest_code
    binary_value = int(stdf_value, 2)
    bit_0 = (binary_value >> 0) & 1
    bit_1 = (binary_value >> 1) & 1
    if bit_1 == 0 and bit_0 == 0:
        return None
    elif bit_1 == 0 and bit_0 == 1:
        return "I"
    elif bit_1 == 1 and bit_0 == 0:
        return "C"

def format_abort_code(stdf_value): # Renamed from parse_abort_code
    binary_value = int(stdf_value, 2)
    bit_2 = (binary_value >> 2) & 1
    return None if bit_2 == 0 else "Y"

def format_head_or_site_number(stdf_value): # Renamed from parse_head_or_site_number
    return None if stdf_value == 255 else stdf_value

def format_limit_compare(stdf_value): # Renamed from parse_limit_compare
    binary_value = int(stdf_value, 2)
    bit_6 = (binary_value >> 6) & 1
    bit_7 = (binary_value >> 7) & 1
    return ''.join(['L' if bit_6 else '', 'H' if bit_7 else '']) if any([bit_6, bit_7]) else None

def format_ftr_pass_fail_flag(stdf_value): # Renamed from parse_ftr_pass_fail_flag
    binary_value = int(stdf_value, 2)
    bit_6 = (binary_value >> 6) & 1
    bit_7 = (binary_value >> 7) & 1
    if bit_6 == 0:
        return "P" if bit_7 == 0 else "F"
    return "F"

def format_ftr_alarm_flags(stdf_value): # Renamed from parse_ftr_alarm_flags
    binary_value = int(stdf_value, 2)
    flags = {
        'A': (binary_value >> 0) & 1,
        'N': (binary_value >> 4) & 1,
        'T': (binary_value >> 3) & 1,
        'U': (binary_value >> 2) & 1,
        'X': (binary_value >> 5) & 1,
    }
    return ''.join([key for key, value in flags.items() if value]) if any(flags.values()) else None

def format_ftr_relative_address(stdf_value): # Renamed from parse_ftr_relative_address
    return hex(stdf_value)[2:] if isinstance(stdf_value, int) else None

def format_generic_data(stdf_value): # Renamed from parse_generic_data
    return '|'.join(stdf_value)

def format_mode_array(stdf_value): # Renamed from parse_mode_array
    return ','.join(hex(num)[2:] for num in stdf_value)

def format_radix_array(stdf_value): # Renamed from parse_radix_array
    mapping = {2: 'B', 8: 'O', 10: 'D', 16: 'H', 20: 'S'}
    if all(element == 0 for element in stdf_value):
        return None
    return ','.join(mapping[element] for element in stdf_value)

def format_default_value(stdf_value): # Renamed from process_default_value
    if stdf_value is None:
        return None
    elif isinstance(stdf_value, tuple):
        return ','.join(map(str, stdf_value))
    return stdf_value

def format_atdf_datetime_from_epoch(epoch_time: int, timezone_str: str = 'UTC') -> str:
    """
    Convert Unix epoch time to an ATDF-specific datetime string (HH:MM:SS DD-MMM-YYYY)
    in the specified timezone. Defaults to UTC if no timezone_str is provided.
    Returns None if epoch_time is None or invalid, or if timezone_str is invalid.
    """
    if epoch_time is None:
        logger.warning("format_atdf_datetime_from_epoch received None for epoch_time.")
        return None
    try:
        # Ensure epoch_time is an integer or float
        if not isinstance(epoch_time, (int, float)):
            raise TypeError(f"epoch_time must be an integer or float, got {type(epoch_time)}")

        # Create a datetime object from epoch_time, explicitly making it UTC.
        dt_object_utc = datetime.datetime.fromtimestamp(epoch_time, datetime.timezone.utc)

        # Get the target timezone
        target_tz = pytz.timezone(timezone_str)
        
        # Convert UTC datetime object to the target timezone
        dt_object_localized = dt_object_utc.astimezone(target_tz)
        
        return dt_object_localized.strftime('%H:%M:%S %d-%b-%Y').upper() # ATDF specific format
    except pytz.UnknownTimeZoneError:
        logger.error(f"Invalid timezone string provided: '{timezone_str}'")
        return None
    except (TypeError, ValueError) as e:
        logger.error(f"Error converting epoch time '{epoch_time}' with timezone '{timezone_str}': {e}")
        return None