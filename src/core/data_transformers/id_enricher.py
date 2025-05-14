# src/core/data_transformers/id_enricher.py
"""
Handles the enrichment of processed records with hierarchical IDs (w_id, p_id).
Logic moved from src/core/atdf/handler.py.
"""
import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

# Helper function moved from src/core/atdf/handler.py
def _find_latest_parent_record(
    record_type_to_find: str,
    all_processed_entries: Dict[str, List[Dict[str, Any]]],
    current_head_num: Optional[int],
    current_site_num: Optional[int]
) -> Optional[Dict[str, Any]]:
    """
    Helper to find the most recent parent record (e.g., WIR or PIR)
    matching head and site numbers if available.
    Searches in reverse order.
    """
    if record_type_to_find not in all_processed_entries or not all_processed_entries[record_type_to_find]:
        return None
    
    for parent_entry in reversed(all_processed_entries[record_type_to_find]):
        parent_head_num = parent_entry.get('head_number') 
        parent_site_num = parent_entry.get('site_number') 

        # More robust matching: if current has context, parent must match. If current lacks, parent can lack.
        if current_head_num is not None and parent_head_num != current_head_num:
            continue
        if current_site_num is not None and parent_site_num != current_site_num:
            continue
            
        return parent_entry
    return None

# Function moved from src/core/atdf/handler.py
def add_hierarchical_ids(
    record_type: str,
    current_entry_dict: Dict[str, Any],
    all_processed_entries: Dict[str, List[Dict[str, Any]]], # This is the collection of lists of dicts for the current file
    counters: Dict[str, int]
) -> Dict[str, Any]:
    """
    Adds w_id and p_id keys ONLY WHEN APPLICABLE based on record type and context,
    with fallback for w_id assignment to PIR/PRR/WRR.
    Ensures WIR/WRR do not have p_id key, and PTR/MPR/FTR do not have w_id key.
    Modifies current_entry_dict in place and returns it.
    """
    current_head_num = current_entry_dict.get('head_number')
    current_site_num = current_entry_dict.get('site_number')
    
    # Do NOT initialize keys here. Add them only when assigned.

    if record_type == 'WIR':
        counters['w_counter'] += 1
        current_entry_dict['w_id'] = counters['w_counter']
        # No p_id key added
        
    elif record_type == 'WRR':
        # Assign w_id from latest relevant WIR (with fallback)
        latest_wir = _find_latest_parent_record('WIR', all_processed_entries, current_head_num, current_site_num)
        if not latest_wir: # Fallback if context-specific fails
             latest_wir = _find_latest_parent_record('WIR', all_processed_entries, None, None) # Find absolute latest
             
        if latest_wir and 'w_id' in latest_wir:
            current_entry_dict['w_id'] = latest_wir['w_id'] # Add w_id key
        else:
            logger.debug(f"WRR record could not find any WIR for w_id. Head: {current_head_num}, Site: {current_site_num}")
        # No p_id key added

    elif record_type == 'PIR':
        counters['p_counter'] += 1
        current_entry_dict['p_id'] = counters['p_counter'] # Add p_id key
        # Assign w_id from latest relevant WIR (with fallback)
        latest_wir = _find_latest_parent_record('WIR', all_processed_entries, current_head_num, current_site_num)
        if not latest_wir: # Fallback if context-specific fails
             latest_wir = _find_latest_parent_record('WIR', all_processed_entries, None, None) # Find absolute latest
             
        if latest_wir and 'w_id' in latest_wir:
            current_entry_dict['w_id'] = latest_wir['w_id'] # Add w_id key
        else:
            logger.debug(f"PIR record could not find any WIR for w_id. Head: {current_head_num}, Site: {current_site_num}")

    elif record_type == 'PRR':
        # Assign p_id from latest relevant PIR
        latest_pir = _find_latest_parent_record('PIR', all_processed_entries, current_head_num, current_site_num)
        if latest_pir and 'p_id' in latest_pir:
            current_entry_dict['p_id'] = latest_pir['p_id'] # Add p_id key
        else:
            logger.debug(f"PRR record could not find a PIR for p_id. Head: {current_head_num}, Site: {current_site_num}")
            
        # Assign w_id from latest relevant WIR (with fallback)
        latest_wir = _find_latest_parent_record('WIR', all_processed_entries, current_head_num, current_site_num)
        if not latest_wir: # Fallback if context-specific fails
             latest_wir = _find_latest_parent_record('WIR', all_processed_entries, None, None) # Find absolute latest
             
        if latest_wir and 'w_id' in latest_wir:
            current_entry_dict['w_id'] = latest_wir['w_id'] # Add w_id key
        else:
            logger.debug(f"PRR record could not find any WIR for w_id. Head: {current_head_num}, Site: {current_site_num}")

    elif record_type in ['PTR', 'MPR', 'FTR']:
        # Assign p_id from latest relevant PIR
        latest_pir = _find_latest_parent_record('PIR', all_processed_entries, current_head_num, current_site_num)
        if latest_pir and 'p_id' in latest_pir:
            current_entry_dict['p_id'] = latest_pir['p_id'] # Add p_id key
        else:
            logger.debug(f"{record_type} record could not find a PIR for p_id. Head: {current_head_num}, Site: {current_site_num}")
        # No w_id key added
            
    return current_entry_dict