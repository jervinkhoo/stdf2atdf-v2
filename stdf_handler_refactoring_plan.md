# Refactoring Plan: Parallelize STDF/ATDF Handler Structure

**Goal:** To make the STDF and ATDF handlers more symmetrical by having both primarily focus on processing a single record. The logic for collecting STDF processed records will be moved from `src/core/stdf_parser/handler.py` into the `process_record` function in `src/converter.py`.

**Phase 1: Modify `src/core/stdf_parser/handler.py`**

1.  **Review `handle_stdf_entry(stdf_template: Dict, data: bytes, endianness: str) -> Dict`:**
    *   **Action:** Confirm that this function correctly parses the raw `data` based on `stdf_template` and `endianness`, and returns a dictionary (`stdf_processed_entry`) representing the single parsed STDF record.
    *   **Crucial Check:** Ensure that this function updates the `stdf_template` dictionary (specifically, the `['fields'][field_name]['value']` for each field) with the parsed values. This is critical because `src/converter.py` later passes this `stdf_template` (now populated with values) to the ATDF `handle_atdf_entry` function.
        *   Lines `124-125` (`stdf_info['value'] = value` and `stdf_processed_entry[stdf_field] = value`) and lines `129-131` in `src/core/stdf_parser/handler.py` suggest this is already happening correctly.

2.  **Remove or Deprecate `handle_stdf_entries(params: Dict)`:**
    *   **Action:** Delete the `handle_stdf_entries` function from `src/core/stdf_parser/handler.py` (currently around line 149).
    *   **Reasoning:** Its responsibilities (calling `handle_stdf_entry` and appending to a collection) will be absorbed by `process_record` in `src/converter.py`.

**Phase 2: Modify `src/converter.py`**

1.  **Update Imports:**
    *   **Action:** In `src/converter.py`, modify the import from `src.core.stdf_parser.handler`. Remove `handle_stdf_entries` from the import list and ensure `handle_stdf_entry` is imported.
    *   Current import (around line 9): `... handle_stdf_entries ...`
    *   Proposed: `... handle_stdf_entry ...`

2.  **Refactor `process_record(params: Dict)` function:**
    *   **Locate STDF Processing Block:** Identify lines around 44-45 where `handle_stdf_entries(params)` is called.
    *   **Replace `handle_stdf_entries` call:**
        *   Remove: `handle_stdf_entries(params)`
        *   Add: Call `handle_stdf_entry` directly. The necessary arguments are:
            *   `stdf_template`: `params['stdf_template']`
            *   `data`: `params['data']` (which is the raw record data read from the file)
            *   `endianness`: `params['endianness']`
        *   Example: `parsed_stdf_record = handle_stdf_entry(params['stdf_template'], params['data'], params['endianness'])`
    *   **Append to `stdf_processed_entries`:**
        *   After the call to `handle_stdf_entry`, add logic to append the `parsed_stdf_record` to the `stdf_processed_entries` collection.
        *   The `record_type` can be obtained from `params['stdf_template']['record_type']`.
        *   Example:
            ```python
            record_type = params['stdf_template']['record_type']
            # Ensure the list for this record type exists
            if record_type not in params['stdf_processed_entries']:
                params['stdf_processed_entries'][record_type] = []
            params['stdf_processed_entries'][record_type].append(parsed_stdf_record)
            ```
    *   **Verify `stdf_template` Population:** Double-check that `params['stdf_template']` (which is passed to `handle_stdf_entry`) is indeed modified in-place by `handle_stdf_entry` to contain the parsed values. This is essential for the subsequent call to the ATDF `handle_atdf_entry` (line `49` in `src/converter.py`), which expects `params['stdf_template']` to have these values.

**Phase 3: Review and Testing**

1.  **Code Review:** Review the changes for correctness, clarity, and adherence to the plan.
2.  **Testing:** Thoroughly test the STDF to ATDF conversion process with various STDF files (including those with different record types and edge cases) to ensure:
    *   No regressions in parsing STDF data.
    *   The `stdf_processed_entries` collection is populated correctly.
    *   The ATDF generation (which relies on the populated `stdf_template`) remains correct.
    *   The final `atdf_processed_entries` collection is correct.

**Mermaid Diagram of the Refactored Structure:**
```mermaid
graph LR
    subgraph Converter [src/converter.py]
        direction LR
        PR[process_record]
    end

    subgraph STDF_Parser [src/core/stdf_parser/handler.py]
        direction LR
        HSE[handle_stdf_entry]
    end

    subgraph ATDF_Generator [src/core/atdf_generator/handler.py]
        direction LR
        HAE[handle_atdf_entry]
    end

    RawDataStream --> PR
    PR -- Raw Record Data, STDF Template, Endianness --> HSE
    HSE -- Parsed STDF Record Dict (stdf_template is also updated) --> PR
    PR -- Appends Parsed STDF Record Dict to stdf_processed_entries --> PR
    PR -- Updated STDF Template (with values) --> HAE
    HAE -- Transformed ATDF Record Dict --> PR
    PR -- Enriches & Appends to atdf_processed_entries --> PR
    PR -- Writes to ATDF File (optional) --> OutputFile

    classDef handler fill:#D6EAF8,stroke:#3498DB
    classDef converter fill:#D5F5E3,stroke:#2ECC71
    class HSE,HAE handler
    class PR converter