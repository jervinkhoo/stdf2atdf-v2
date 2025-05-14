# src/core/data_transformers/record_modifiers/advantest_modifier.py
# Moved from src/core/atdf/modifiers/advantest.py
from typing import Dict, Any

def process_advantest(record_type: str, record_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Modifier (Preprocessor) for Advantest tester data.
    Modify this file directly to add Advantest-specific processing logic.
    """
    if record_type == 'MIR':
        # Example: Add Advantest-specific MIR processing
        if 'tester_type' in record_data:
            #record_data['tester_type'] = record_data['tester_type'].replace('_', '-')
            record_data['tester_type'] = "V93000"

        # Add any custom fields needed
        # record_data['advantest_version'] = 'V93000'
        # record_data['test_cell'] = 'CELL1'

    elif record_type == 'SDR':
        # Add Advantest-specific SDR processing
        if 'handler_type' in record_data:
            record_data['handler_type'] = f"ADV_{record_data['handler_type']}"

    return record_data