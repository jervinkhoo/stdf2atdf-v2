# src/core/data_transformers/record_modifiers/base.py
# Moved from src/core/atdf/modifiers/base.py # Updated to reflect terminology change

from typing import Dict, Any, Optional
import logging
# Imports will need adjustment after specific modifiers are moved and renamed
from .advantest_modifier import process_advantest # Placeholder name adjustment
from .teradyne_modifier import process_teradyne # Placeholder name adjustment
from .eagle_modifier import process_eagle # Placeholder name adjustment

logger = logging.getLogger(__name__)


def modify_record(record_type: str, record_data: Dict[str, Any], # Renamed function
                  modifier_type: Optional[str] = None) -> Dict[str, Any]: # Renamed parameter
    """
    Applies a specific modification to a record based on the modifier_type.

    Args:
        record_type: Type of the record (e.g., 'PIR', 'PTR')
        record_data: Dictionary containing record data
        modifier_type: String identifier for which record modifier to use # Updated parameter name and description

    Returns:
        Modified record_data dictionary
    """
    if not modifier_type: # Renamed variable
        return record_data

    try:
        modifier_function = get_modifier(modifier_type) # Use renamed variable
        return modifier_function(record_type, record_data)
    except ValueError as e: # Catching ValueError specifically as raised by get_modifier
        logger.error(f"Error during record modification: {str(e)}")
        # Reraise or handle as appropriate, for now, returning original data
        # Or, more robustly, raise a custom exception or the original one:
        # raise ValueError(f"Unknown modifier type: {modifier_type}") from e
        return record_data # Or re-raise e
    except Exception as e: # Catch other potential errors during modification itself
        logger.error(f"Unexpected error during record modification for type {modifier_type}: {str(e)}")
        return record_data


def get_modifier(modifier_type: str): # Renamed from get_preprocessor
    """
    Factory function to get the appropriate modifier based on type.
    """
    # Map uses modifier type string identifiers (e.g., 'advantest') as keys.
    modifiers = {
        'advantest': process_advantest,
        'teradyne': process_teradyne,
        'eagle': process_eagle
    }

    if modifier_type not in modifiers:
        raise ValueError(f"Unknown modifier type: {modifier_type}")

    return modifiers[modifier_type]