# src/core/stdf/unpackers.py
import re
import struct
import logging

logger = logging.getLogger(__name__)

def unpack_C1(data, endianness, offset):
    result = struct.unpack(endianness + 's', data[offset:offset + 1])[0]
    if result == b'\x00':
        return None, offset + 1
    else:
        return result.decode(), offset + 1


# def unpack_Cn(data, endianness, offset):
#     byte_count, offset = unpack_U1(data, endianness, offset)
#     value = ''
#     for _ in range(byte_count):
#         temp, offset = unpack_C1(data, endianness, offset)
#         value += temp
#     return value, offset

def unpack_Cn(data, endianness, offset):
    byte_count, offset = unpack_U1(data, endianness, offset)
    value = ''
    try:
        for _ in range(byte_count):
            temp, offset = unpack_C1(data, endianness, offset)
            if temp is None:
                logger.warning("Encountered None value while unpacking string")
                continue
            value += temp
    except Exception as e:
        logger.error(f"Error unpacking string: {e}")
        return None, offset

    return value, offset

def unpack_U1(data, endianness, offset):
    return struct.unpack(endianness + 'B', data[offset:offset + 1])[0], offset + 1


def unpack_U2(data, endianness, offset):
    return struct.unpack(endianness + 'H', data[offset:offset + 2])[0], offset + 2


def unpack_U4(data, endianness, offset):
    return struct.unpack(endianness + 'I', data[offset:offset + 4])[0], offset + 4


def unpack_I1(data, endianness, offset):
    return struct.unpack(endianness + 'b', data[offset:offset + 1])[0], offset + 1


def unpack_I2(data, endianness, offset):
    return struct.unpack(endianness + 'h', data[offset:offset + 2])[0], offset + 2


def unpack_I4(data, endianness, offset):
    return struct.unpack(endianness + 'i', data[offset:offset + 4])[0], offset + 4


def unpack_R4(data, endianness, offset):
    return struct.unpack(endianness + 'f', data[offset:offset + 4])[0], offset + 4


def unpack_R8(data, endianness, offset):
    return struct.unpack(endianness + 'd', data[offset:offset + 8])[0], offset + 8


# def unpack_B0(data, endianness, offset):
#     return "Special pad field"

# def unpack_B0(data, endianness, offset):
#     return 'PAD', offset + 1

def unpack_B1(data, endianness, offset):
    temp, offset = unpack_U1(data, endianness, offset)
    value = format(temp, '08b')
    return value, offset


def unpack_Vn(data, endianness, offset, array_size):
    variable_data_type_mapping = {
        # 0: { 'dtype': 'B*0', 'atdf': '' },
        1: {'dtype': 'U*1', 'atdf': 'U'},
        2: {'dtype': 'U*2', 'atdf': 'M'},
        3: {'dtype': 'U*4', 'atdf': 'B'},
        4: {'dtype': 'I*1', 'atdf': 'I'},
        5: {'dtype': 'I*2', 'atdf': 'S'},
        6: {'dtype': 'I*4', 'atdf': 'L'},
        7: {'dtype': 'R*4', 'atdf': 'F'},
        8: {'dtype': 'R*8', 'atdf': 'D'},
        10: {'dtype': 'C*n', 'atdf': 'T'},
        11: {'dtype': 'B*n', 'atdf': 'X'},
        12: {'dtype': 'D*n', 'atdf': 'Y'},
        13: {'dtype': 'N*1', 'atdf': 'N'},
    }

    new_list = []
    for _ in range(array_size):
        data_type_code, offset = unpack_U1(data, endianness, offset)

        if data_type_code in variable_data_type_mapping:
            is_array = True
            if data_type_code == 12:
                is_array = False
            data_type = variable_data_type_mapping[data_type_code]['dtype']
            temp, offset = unpack_dtype(data_type, data, endianness, offset, is_array=is_array)
            temp = variable_data_type_mapping[data_type_code]['atdf'] + str(temp)
            new_list.append(temp)
        else:
            print("Invalid data type")

    return new_list, offset


def unpack_Bn(data, endianness, offset):
    byte_count, offset = unpack_U1(data, endianness, offset)

    binary_string = ''
    for _ in range(byte_count):
        temp, offset = unpack_B1(data, endianness, offset)
        binary_string += temp

    decimal_number = int(binary_string, 2) if binary_string else None
    value = hex(decimal_number)[2:].upper() if decimal_number else None

    return value, offset


def unpack_Dn(data, endianness, offset, is_array):
    bit_count, offset = unpack_U2(data, endianness, offset)

    byte_count = (bit_count + 7) // 8

    value = data[offset:offset + byte_count].hex().upper()

    offset += byte_count

    if (is_array == False):
        return value, offset
    elif (is_array == True):
        return hex_to_bit_positions(value), offset


def unpack_N1(data, endianness, offset):
    return hex(struct.unpack(endianness + 'B', data[offset:offset + 1])[0] & 0x0F)[2:].upper(), offset + 1  # extract only the lower nibble


def unpack_xC1(data, endianness, offset, array_size):
    return struct.unpack(endianness + '{}s'.format(array_size),
                         data[offset:offset + 1 * array_size]), offset + 1 * array_size


def unpack_xCn(data, endianness, offset, array_size):
    new_list = []
    for _ in range(array_size):
        byte_count, offset = unpack_U1(data, endianness, offset)

        temp = struct.unpack(endianness + str(byte_count) + 's', data[offset:offset + byte_count])[0].decode()
        offset += byte_count
        new_list.append(temp)
    return new_list, offset


def unpack_xU1(data, endianness, offset, array_size):
    return struct.unpack(endianness + '{}B'.format(array_size),
                         data[offset:offset + 1 * array_size]), offset + 1 * array_size


def unpack_xU2(data, endianness, offset, array_size):
    return struct.unpack(endianness + '{}H'.format(array_size),
                         data[offset:offset + 2 * array_size]), offset + 2 * array_size


def unpack_xR4(data, endianness, offset, array_size):
    return struct.unpack(endianness + '{}f'.format(array_size),
                         data[offset:offset + 4 * array_size]), offset + 4 * array_size


def unpack_xN1(data, endianness, offset, array_size):
    new_list = []
    i = 0
    while i < array_size:
        nibble_lower = 0
        nibble_higher = 0
        byte, offset = unpack_U1(data, endianness, offset)

        nibble_lower = byte & 0x0F  # extract only the lower nibble
        new_list.append(nibble_lower)
        i += 1
        if not i < array_size: break

        nibble_higher = (byte >> 4) & 0x0F  # extract only the higher nibble
        new_list.append(nibble_higher)
        i += 1
        if not i < array_size: break
    return new_list, offset


def hex_to_bit_positions(hex_value):
    new_list = []
    for byte_index, byte_value in enumerate(bytes.fromhex(hex_value)):
        for bit_index in range(8):
            if byte_value & (1 << bit_index):
                new_list.append((byte_index * 8) + bit_index + 1)
    return new_list


def unpack_dtype(dtype, data, endianness, offset, **kwargs):
    array_size = kwargs.get("array_size", 0)
    is_array = kwargs.get("is_array", True)

    match dtype:
        case "C*1":
            return unpack_C1(data, endianness, offset)

        case "C*n":
            return unpack_Cn(data, endianness, offset)

        case "U*1":
            return unpack_U1(data, endianness, offset)

        case "U*2":
            return unpack_U2(data, endianness, offset)

        case "U*4":
            return unpack_U4(data, endianness, offset)

        case "I*1":
            return unpack_I1(data, endianness, offset)

        case "I*2":
            return unpack_I2(data, endianness, offset)

        case "I*4":
            return unpack_I4(data, endianness, offset)

        case "R*4":
            return unpack_R4(data, endianness, offset)

        case "R*8":
            return unpack_R8(data, endianness, offset)

        # case "B*0":
        #     return unpack_B0(data, endianness, offset)

        case "B*1":
            return unpack_B1(data, endianness, offset)

        case "V*n":
            return unpack_Vn(data, endianness, offset, array_size)

        case "B*n":
            return unpack_Bn(data, endianness, offset)

        case "D*n":
            return unpack_Dn(data, endianness, offset, is_array)

        case "N*1":
            return unpack_N1(data, endianness, offset)

        case "xC*1":
            return unpack_xC1(data, endianness, offset, array_size)

        case "xC*n":
            return unpack_xCn(data, endianness, offset, array_size)

        case "xU*1":
            return unpack_xU1(data, endianness, offset, array_size)

        case "xU*2":
            return unpack_xU2(data, endianness, offset, array_size)

        case "xR*4":
            return unpack_xR4(data, endianness, offset, array_size)

        case "xN*1":
            return unpack_xN1(data, endianness, offset, array_size)

        case _:
            message = f"Invalid data type: {dtype}"
            logger.error(message)
            raise ValueError(message)


# def check_invalid_and_set_None_after_unpack(stdf_template, field):
#     """Check for invalid values and set to None if applicable."""
#     field_info = stdf_template['fields'][field]
#     missing = field_info.get('missing')
#     value = field_info.get('value')
#     dtype = field_info.get('dtype')

#     if missing is None:
#         return

#     if isinstance(missing, int):
#         if value == missing:
#             field_info['value'] = None
#             return

#     if isinstance(missing, str):
#         if missing == "length byte = 0":
#             if dtype == "C*n" and value == "":
#                 field_info['value'] = None
#                 return
#             elif dtype == "B*n" and value is None:
#                 return
#             elif dtype == "D*n":
#                 if (isinstance(value, str) and value == "") or \
#                 (isinstance(value, tuple) and len(value) == 0):
#                     field_info['value'] = None
#                     return
#             elif dtype == "xC*n":
#                 # For xC*n, 'value' is a tuple of strings.
#                 # If all strings in the tuple are empty, then the field is considered missing.
#                 if isinstance(value, tuple):
#                     # Check if the tuple is empty OR all elements in the tuple are empty strings
#                     if not value or all(s == "" for s in value):
#                         field_info['value'] = None
#                         return
#                 elif value is None: # If unpack_xCn somehow returned None (e.g., array_size was 0 and it was handled that way)
#                     field_info['value'] = None # Or it's already None
#                     return
        
#         # Check for space
#         if missing == 'space' and value == " ":
#             field_info['value'] = None
#             return

#         # Check for special counts
#         for count_field in ['indx_cnt', 'num_bins', 'rtn_icnt', 'rslt_cnt', 'pgm_icnt']:
#             if count_field in missing and stdf_template['fields'].get(count_field, {}).get('value', 1) == 0:
#                 field_info['value'] = None
#                 return

#         # Check bitwise flags
#         for flag_field in ['opt_flag', 'test_flg']:
#             if flag_field in missing:
#                 decimal_value = int(stdf_template['fields'][flag_field]['value'], 2)
#                 matches = [int(m) for m in re.findall(r'\b\d+\b', missing)]
#                 expected_bit = matches.pop()
#                 for bit_pos in matches:
#                     if (decimal_value >> bit_pos) & 1 == expected_bit:
#                         field_info['value'] = None
#                         return # Stop checking if one of the positions results in 1

def check_invalid_and_set_None_after_unpack(stdf_template: dict, field: str): # Removed unused record_data_len, current_offset
    """Check for invalid values and set to None if applicable based on 'missing' conditions."""
    field_info = stdf_template['fields'][field]
    missing_condition = field_info.get('missing')
    value = field_info.get('value')
    dtype = field_info.get('dtype')

    if missing_condition is None:
        return

    # 1. Handle integer missing values (e.g., 65535, 4294967295 for U*2/U*4)
    if isinstance(missing_condition, int):
        if value == missing_condition:
            field_info['value'] = None
            # logger.debug(f"Field '{field}' value '{value}' matched integer missing condition '{missing_condition}'. Set to None.")
            return

    # 2. Handle string-based missing conditions
    if isinstance(missing_condition, str):
        # A. Exact string matches
        if missing_condition == "length byte = 0":
            if dtype == "C*n" and value == "":
                field_info['value'] = None
            elif dtype == "B*n" and value is None: # unpack_Bn already returns None
                pass # Value is already None
            elif dtype == "D*n":
                if (isinstance(value, str) and value == "") or \
                   (isinstance(value, (list, tuple)) and len(value) == 0):
                    field_info['value'] = None
            elif dtype == "xC*n":
                if isinstance(value, (list, tuple)) and (not value or all(s == "" for s in value)):
                    field_info['value'] = None
                elif value is None: # Should be redundant if unpacker handles array_size=0 well
                    field_info['value'] = None
            # If a value was set to None, log and return
            if field_info['value'] is None and value is not None : # only log if changed
                 # logger.debug(f"Field '{field}' with dtype '{dtype}' met 'length byte = 0'. Original value: '{value}'. Set to None.")
                 pass
            return # Processed "length byte = 0"

        if missing_condition == 'space':
            if value == " ":
                field_info['value'] = None
                # logger.debug(f"Field '{field}' value was a space. Set to None.")
            return # Processed "space"

        # B. Pattern-based: Count field checks (e.g., "indx_cnt = 0")
        # This assumes the missing string is *exactly* "FIELD_NAME = 0"
        count_match = re.fullmatch(r"(\w+)\s*=\s*0", missing_condition) # Use fullmatch for exact pattern
        if count_match:
            count_field_name = count_match.group(1)
            # Check if this count_field_name is one of the known ones, or just proceed
            # known_count_fields = ['indx_cnt', 'num_bins', 'rtn_icnt', 'rslt_cnt', 'pgm_icnt']
            # if count_field_name in known_count_fields:
            if count_field_name in stdf_template['fields']:
                count_field_value = stdf_template['fields'][count_field_name].get('value')
                if count_field_value == 0:
                    field_info['value'] = None
                    # logger.debug(f"Field '{field}' set to None because dependent count field '{count_field_name}' is 0.")
                return # Processed count field dependency
            else:
                logger.warning(f"Missing condition '{missing_condition}' for field '{field}' "
                               f"references non-existent count field '{count_field_name}'.")
                return


        # C. Pattern-based: Bitwise flag checks (e.g., "opt_flag bit X = V" or "opt_flag bit X or Y = V")
        flag_pattern_match = re.fullmatch(
            r"([a-zA-Z0-9_]+)\s+bit\s+([0-9\s]*(?:or\s*[0-9\s*]+)*)\s*=\s*([01])",
            missing_condition,
            re.IGNORECASE # Make the match case-insensitive for the flag name
        )
        if flag_pattern_match:
            flag_name_from_missing = flag_pattern_match.group(1) # This will be 'opt_flag' (or 'OPT_FLAG' if it were that)
            bits_str = flag_pattern_match.group(2)
            expected_bit_value = int(flag_pattern_match.group(3))

            # Get the actual value of the flag field (e.g., opt_flag's value)
            # When accessing stdf_template['fields'], the key should match exactly how it's defined there.
            # If stdf_template['fields'] uses 'opt_flag' (lowercase), then use that.
            # The flag_name_from_missing might be 'OPT_FLAG' if re.IGNORECASE matched it.
            # So, we might need to check against both cases or normalize.
            # A simpler way: iterate through known flag fields from your template.

            # Let's refine how we get the flag_actual_value_str to be robust to case in flag_name_from_missing
            # if the keys in stdf_template['fields'] are consistently one case (e.g. lowercase)

            actual_flag_field_key_in_template = None
            # Find the correct key in stdf_template['fields'] matching flag_name_from_missing, case-insensitively
            for key in stdf_template['fields'].keys():
                if key.lower() == flag_name_from_missing.lower(): # Compare lowercase versions
                    actual_flag_field_key_in_template = key
                    break
            
            if actual_flag_field_key_in_template and actual_flag_field_key_in_template in stdf_template['fields']:
                flag_actual_value_str = stdf_template['fields'][actual_flag_field_key_in_template].get('value')

                if not isinstance(flag_actual_value_str, str) or not all(c in '01' for c in flag_actual_value_str):
                    logger.warning(f"Flag field '{actual_flag_field_key_in_template}' for '{field}' is not a binary string: '{flag_actual_value_str}'. Cannot evaluate missing condition: '{missing_condition}'.")
                    return

                try:
                    flag_actual_decimal_value = int(flag_actual_value_str, 2)
                    bit_positions_to_check = [int(b.strip()) for b in bits_str.replace("or", " ").split()]

                    for bit_pos in bit_positions_to_check:
                        actual_bit = (flag_actual_decimal_value >> bit_pos) & 1
                        if actual_bit == expected_bit_value:
                            field_info['value'] = None
                            return 
                except ValueError:
                    logger.warning(f"Could not parse binary string for flag '{actual_flag_field_key_in_template}': '{flag_actual_value_str}' or bit positions from '{bits_str}'.")
                    return
            else:
                logger.warning(f"Missing condition '{missing_condition}' for field '{field}' "
                               f"references flag field '{flag_name_from_missing}' which was not found (case-insensitively) in the template fields.")
            return

        # If no specific string pattern matched above, log it if it's an unhandled string.
        # This helps identify if new 'missing' string formats appear.
        logger.warning(f"Unhandled string 'missing' condition for field '{field}': '{missing_condition}'. Value remains: '{value}'.")