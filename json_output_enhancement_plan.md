# Plan: Enhance STDF-to-ATDF Converter for JSON Output and Database Preparation

## 1. Objective

To modify the existing STDF-to-ATDF conversion process to:
1.  Produce a JSON output containing the processed data in a structured format (preserving data types like lists/arrays, numbers, booleans). This JSON will serve as input for a subsequent database insertion script.
2.  Ensure the existing ATDF text file generation remains correct.
3.  The `run_conversion` function in `src/converter.py` will be the main entry point returning the processed data and optionally writing the ATDF text and JSON files.

## 2. Overall Data Flow

The envisioned data flow is as follows:

```mermaid
graph LR
    A[STDF File (Bytes)] --> B{run_conversion in converter.py};
    B --> C{process_record / handle_stdf_entry in stdf_parser/handler.py};
    C --> D[STDF Record (Python Dict with Lists/Tuples)];
    D --> E{Phase A: Formatters in atdf_generator/formatters.py};
    E --> F[Pythonic ATDF Record (Lists, Lists-of-Lists, Native Types)];
    F --> G{modify_record / add_hierarchical_ids};
    G --> H[Enriched Pythonic ATDF Record];
    H --> I[atdf_processed_entries (Collection of Enriched Pythonic Dicts)];
    
    subgraph Phase C [write_atdf_file in atdf_generator/handler.py]
        direction LR
        I -- For ATDF Text --> X{Field-specific Stringification Logic (Helper Function)};
        X --> J((Optional ATDF Text File));
    end

    subgraph Phase D [run_conversion in converter.py]
        direction LR
        I -- For JSON --> K((Optional JSON File));
        I --> L[Return atdf_processed_entries];
    end
```

## 3. Detailed Implementation Phases

### Phase A: Modify Formatters (`src/core/atdf_generator/formatters.py`)

**Goal:** Ensure formatters return rich Python data structures suitable for JSON serialization, rather than pre-formatted strings for ATDF.

**Actions:**
1.  **Review all formatter functions** (e.g., `format_pass_fail_flag`, `format_alarm_flags`, `format_mode_array`, `format_radix_array`, `format_states_array`, `format_generic_data`, `format_default_value`, etc.).
2.  **For array-like STDF fields:**
    *   Modify formatters to return Python **lists** of appropriately typed elements (e.g., list of strings, list of numbers).
    *   Example for `format_mode_array(stdf_value)`:
        *   Change from: `return ','.join(hex(num)[2:] for num in stdf_value)`
        *   To: `return [hex(num)[2:] for num in stdf_value]`
    *   Example for `format_radix_array(stdf_value)`:
        *   Change from: `return ','.join(mapping[element] for element in stdf_value)`
        *   To: `return [mapping[element] for element in stdf_value]`
3.  **For `format_state_field(stdf_values)`:**
    *   Modify to return a Python **list of lists of strings**.
    *   Example: Input `chal = [['P', 'A'], ['S', 'S']]`, `char = None` should result in output `[['P', 'A'], ['S', 'S']]`.
    *   The inner lambda/formatting logic should produce the inner lists, and these should be collected into an outer list.
4.  **For scalar STDF fields:**
    *   Ensure formatters return native Python types (`int`, `float`, `bool`, `str`, or `None`) where appropriate. Avoid premature conversion to strings if the underlying data is not inherently a string.
5.  **List vs. Tuple:** Prefer returning **lists** from formatters for sequences that represent arrays, as this is idiomatic for collections that will be serialized to JSON arrays.

### Phase C: Modify ATDF File Writer (`src/core/atdf_generator/handler.py` - `write_atdf_file` function)

**Goal:** Adapt `write_atdf_file` to correctly convert the rich Python data structures (now produced by formatters) into the specific string representations required by the ATDF text file format. This logic will be hardcoded within `write_atdf_file` or a dedicated helper function.

**Actions:**
1.  **Create a Helper Function (Recommended):**
    *   Define a new private helper function within `handler.py`, e.g., `_format_value_for_atdf_text(field_name: str, value: Any, record_type: str) -> str`.
    *   This function will contain the `if/elif` logic to handle stringification based on `field_name` (and potentially `record_type`).
2.  **Implement Stringification Logic in Helper Function:**
    *   **For simple lists (e.g., from `format_mode_array`):**
        If `field_name` is 'MODE_ARRAY' and `value` is `['C0', '1A', '3']`, return `"C0,1A,3"`.
        (`','.join(map(str, value))`)
    *   **For lists of lists (e.g., from `format_state_field`):**
        If `field_name` is 'PROGRAMMED_STATE' and `value` is `[['P', 'A'], ['S', 'S']]`, return `"P,A/S,S"`.
        (`'/'.join([','.join(map(str, group)) for group in value])`)
    *   **For `format_generic_data`:**
        If `field_name` is 'GENERIC_DATA' and `value` is `['item1', 'item2']`, return `"item1|item2"`.
        (`'|'.join(map(str, value))`)
    *   **Handle other specific array types** as needed, using their defined ATDF string formats.
    *   **Scalar Types:** For `int`, `float`, `bool`, convert using `str(value)`.
    *   **None Values:** Convert to an empty string `""`.
    *   **Timestamps:** The existing timestamp formatting logic in `write_atdf_file` should be integrated or called appropriately, likely before the general helper.
3.  **Integrate Helper in `write_atdf_file`:**
    *   Inside the field loop in `write_atdf_file`, after retrieving `value = atdf_processed_entry.get(field_name)`:
        *   First, handle timestamps as currently done.
        *   For other fields, call the helper: `value_str = _format_value_for_atdf_text(field_name, value, record_type)`.
        *   Then, `atdf_file.write(value_str)`.

### Phase D: Modify Main Converter (`src/converter.py` - `run_conversion` function)

**Goal:** Enable `run_conversion` to optionally write the processed data to a JSON file. The data written will be the `atdf_processed_entries` dictionary, which now contains richer Python types due to Phase A changes.

**Actions:**
1.  **Import `json` Module:**
    *   Add `import json` at the top of `src/converter.py`.
2.  **Update `run_conversion` Signature:**
    *   Add a new optional parameter: `json_output_file: Optional[str] = None`.
    *   Signature:
        ```python
        def run_conversion(
                stdf_input_file: str,
                atdf_output_file: Optional[str] = None,
                json_output_file: Optional[str] = None, # New
                records_to_process: Optional[List[str]] = None,
                modifier_type: Optional[str] = None
        ) -> Dict[str, List[Dict]]:
            # function body
        ```
3.  **Add JSON Writing Logic:**
    *   Inside `run_conversion`, before the final `return atdf_processed_entries` statement:
        ```python
        # after main processing loop
        logger.info(f"Successfully processed {stdf_input_file}")

        if json_output_file:
            logger.info(f"Writing processed ATDF data to JSON file: {json_output_file}")
            try:
                with open(json_output_file, 'w') as f_json:
                    json.dump(atdf_processed_entries, f_json, indent=4) # indent=4 for readability
                logger.info(f"Successfully wrote JSON to {json_output_file}")
            except IOError as e:
                logger.error(f"Error writing JSON to {json_output_file}: {e}")
            except TypeError as e:
                logger.error(f"Error serializing data to JSON for {json_output_file}: {e}. Ensure all data is JSON serializable.")
        
        return atdf_processed_entries
        ```

## 4. Next Steps (Post-Implementation)

*   The calling orchestrator script will receive the `atdf_processed_entries` dictionary from `run_conversion`.
*   This dictionary (or the generated JSON file) can then be used by another script (e.g., using SQLAlchemy or another ORM) to insert data into a database.
*   The structure of the database (e.g., one table per ATDF record type, or a more relational model) will guide the design of this database insertion script.

This plan provides a clear path to achieving the desired JSON output while maintaining correct ATDF text generation.