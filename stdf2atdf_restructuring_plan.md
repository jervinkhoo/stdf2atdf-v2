# STDF to ATDF Converter: Restructuring Plan

## 1. Overall Goal
Restructure the `stdf2atdf` project to achieve clearer separation of concerns, higher cohesion within modules, lower coupling between them, and improved maintainability and testability for long-term development and understanding.

## 2. Key Architectural Changes
The restructuring will focus on the following key architectural improvements:

1.  **Modular Core Components:** The core conversion logic will be broken down into distinct, staged components:
    *   **STDF Parser (`core/stdf_parser/`):** Responsible for reading STDF files and parsing them into raw Python data structures (list of dictionaries).
    *   **Data Transformers (`core/data_transformers/`):** Responsible for modifying and enriching the parsed data. This includes:
        *   `record_modifiers/` (formerly preprocessors) for applying manufacturer-specific or other domain-specific data transformations.
        *   `id_enricher.py` for adding hierarchical `w_id` (wafer ID) and `p_id` (part ID) to records for the programmatic output.
    *   **ATDF Generator (`core/atdf_generator/`):** Responsible for taking the processed data and formatting it into the ATDF file output, ensuring `w_id`/`p_id` are not included in the file.
2.  **Orchestration Layer (`src/converter_service.py`):** A new service layer will be introduced to manage the flow of data through the core components for each input file. The existing `src/cli.py` will interact with this service.
3.  **Refined Utilities Directory (`src/utils/`):** A new top-level `src/utils/` directory will be established to house *only* truly generic, application-agnostic helper functions and classes. Domain-specific utilities previously in `src/core/utils/` will be moved into their respective domain modules or the `converter_service.py`.

## 3. Final Proposed Folder Structure

```
.
├── .gitignore
├── a595.atdf
├── a595.stdf
├── ... (other project files)
├── README.md
├── requirements.txt
├── run_conversion.py
├── stdf2atdf_final_summary.md
├── stdf2atdf_refactor_and_enrich_plan.md
├── stdf2atdf_restructuring_plan.md  (This file)
│
└── src/
    ├── __init__.py
    ├── __main__.py
    ├── cli.py                     (Handles CLI arguments, calls converter_service)
    ├── converter_service.py       (Orchestrates conversion stages, manages file handles)
    │
    ├── core/
    │   ├── __init__.py
    │   │
    │   ├── stdf_parser/
    │   │   ├── __init__.py
    │   │   ├── handler.py         (Orchestrates STDF parsing, uses unpackers, incorporates STDF-specific setup)
    │   │   ├── unpackers.py       (Low-level STDF binary record unpacking functions)
    │   │   └── templates.py       (STDF-specific templates/constants for parsing, e.g., get_record_types())
    │   │
    │   ├── data_transformers/
    │   │   ├── __init__.py
    │   │   ├── id_enricher.py     (Adds w_id, p_id to create "Enriched Records")
    │   │   │
    │   │   └── record_modifiers/  (Formerly preprocessors)
    │   │       ├── __init__.py
    │   │       ├── base.py
    │   │       ├── advantest_modifier.py
    │   │       ├── eagle_modifier.py
    │   │       └── teradyne_modifier.py
    │   │
    │   └── atdf_generator/
    │       ├── __init__.py
    │       ├── handler.py         (Orchestrates ATDF file writing, uses formatters)
    │       ├── formatters.py      (Functions to format record dicts into ATDF strings)
    │       └── templates.py       (ATDF string formatting templates/constants)
    │
    └── utils/  (Contains only truly generic, reusable utilities)
        ├── __init__.py
        ├── decorators.py      (e.g., timing_decorator)
        ├── epoch.py           (Generic epoch/datetime conversions)
        ├── files.py           (Generic file operations: get_file_handle, is_file, find_stdf_files, validate_input_file)
        └── logging.py         (Application-wide logging setup)
```

## 4. Component Responsibilities and Data Flow

### 4.1. Data Flow Diagram

```mermaid
graph TD
    A[STDF File Input] --> B{Stage 1: STDF Parsing};
    B -- "Raw STDF Records" (List of Dictionaries) --> C{Stage 2a: Record Modification};
    C -- "Modified Records" (List of Dictionaries) --> D{Stage 3: ATDF File Generation};
    D --> E[ATDF File Output (No w_id/p_id)];
    C -- "Modified Records" (List of Dictionaries) --> F{Stage 2b: ID Enrichment};
    F -- "Enriched Records" (List of Dictionaries with w_id/p_id) --> G[Final In-Memory "List of Dicts" (Programmatic Output)];

    subgraph Orchestration [src/converter_service.py]
        direction LR
        subgraph Stage1 [core/stdf_parser/]
            B_handler["handler.py (uses unpackers.py, templates.py)"]
        end
        subgraph Stage2_DataTransformers [core/data_transformers/]
            C_modifiers["record_modifiers/*.py"]
            F_enricher["id_enricher.py"]
        end
        subgraph Stage3_ATDFGen [core/atdf_generator/]
            D_handler["handler.py (uses formatters.py, templates.py)"]
        end
        B_handler --> C_modifiers;
        C_modifiers --> F_enricher;
        C_modifiers --> D_handler;
    end

    H[src/cli.py] --> Orchestration;
    Orchestration -- Returns Programmatic Output --> H;
```

### 4.2. Component Details:

*   **`src/cli.py`**:
    *   **Input:** Command-line arguments (input path, output flag, record filter, modifier choice).
    *   **Responsibilities:** Parses arguments, discovers STDF files (using `utils/files.py:find_stdf_files`), validates input file (using `utils/files.py:validate_input_file`), instantiates and calls `converter_service.py`, handles the final programmatic output (e.g., for verification or return to a calling library).
    *   **Output:** Programmatic "Enriched Records" (list of dicts) or writes to console.
*   **`src/converter_service.py`**:
    *   **Input:** List of STDF file paths, output ATDF path (optional), record filter (optional), modifier choice (optional).
    *   **Responsibilities:**
        *   Manages the overall conversion process for one or more files sequentially.
        *   Handles file opening/closing safely (incorporates logic from old `utils/files.py:managed_files` and `reset_and_check_binary`).
        *   For each file:
            1.  Calls `core/stdf_parser/handler.py` to get "Raw STDF Records."
            2.  Calls the appropriate `core/data_transformers/record_modifiers/*.py` with "Raw STDF Records" to get "Modified Records."
            3.  If ATDF file output is requested: Calls `core/atdf_generator/handler.py` with "Modified Records."
            4.  Calls `core/data_transformers/id_enricher.py` with "Modified Records" to produce "Enriched Records."
    *   **Output:** Returns a list of "Enriched Records" (one item per processed file, typically `List[Dict[str, List[Dict[str, Any]]]]`).
*   **`core/stdf_parser/handler.py`**:
    *   **Input:** STDF file path/handle, record processing flags.
    *   **Responsibilities:** Orchestrates STDF parsing. Reads STDF file record by record, determines endianness, reads record headers (incorporates logic from old `utils/setup.py`), calls appropriate functions from `unpackers.py` to decode binary data, uses `templates.py` for record type definitions, initializes data structures for collecting records (incorporates logic from old `utils/setup.py`).
    *   **Output:** "Raw STDF Records" (a list of Python dictionaries, one per STDF record).
*   **`core/stdf_parser/unpackers.py`**:
    *   **Input:** Raw binary data for a specific STDF record, endianness.
    *   **Responsibilities:** Contains low-level functions (e.g., `unpack_mir`, `unpack_pir`) to decode specific STDF record types from binary to Python native types.
    *   **Output:** A Python dictionary representing the unpacked STDF record.
*   **`core/stdf_parser/templates.py`**:
    *   **Responsibilities:** Stores STDF-specific definitions, e.g., a list/enum of all known STDF record types (`get_record_types()` from old `utils/templates.py`), constants related to STDF structure.
*   **`core/data_transformers/record_modifiers/*.py` (e.g., `advantest_modifier.py`)**:
    *   **Input:** "Raw STDF Records" (list of dictionaries).
    *   **Responsibilities:** Applies manufacturer-specific or other domain-specific transformations/modifications to the records. Each modifier implements a common interface (defined in `base.py`).
    *   **Output:** "Modified Records" (list of dictionaries).
*   **`core/data_transformers/id_enricher.py`**:
    *   **Input:** "Modified Records" (list of dictionaries).
    *   **Responsibilities:** Implements the logic to add `w_id` and `p_id` hierarchically to the records.
    *   **Output:** "Enriched Records" (list of dictionaries with `w_id`/`p_id`).
*   **`core/atdf_generator/handler.py`**:
    *   **Input:** "Modified Records" (list of dictionaries), output ATDF file handle.
    *   **Responsibilities:** Orchestrates ATDF file generation. Iterates through "Modified Records," calls functions from `formatters.py` to get the ATDF string for each record, and writes these strings to the output file.
    *   **Output:** Writes to ATDF file.
*   **`core/atdf_generator/formatters.py`**:
    *   **Input:** A single "Modified Record" (dictionary).
    *   **Responsibilities:** Contains functions (e.g., `format_mir`, `format_pir`, renamed from old `atdf/parsers.py:parse_xxx`) to convert a record dictionary into its ATDF string representation. Uses `templates.py` for formatting rules, separators, and ATDF-specific date formatting (from old `utils/epoch.py`).
    *   **Output:** An ATDF formatted string for a single record.
*   **`core/atdf_generator/templates.py`**:
    *   **Responsibilities:** Stores ATDF-specific string formatting templates, constants (field separators, record terminators), field order definitions, etc.
*   **`src/utils/*.py` files**:
    *   **`decorators.py`**: Contains generic decorators like `timing_decorator`.
    *   **`epoch.py`**: Contains generic epoch/datetime conversion functions (Django/SQLite specifics removed).
    *   **`files.py`**: Contains generic file system utilities (`get_file_handle`, `is_file`, `find_stdf_files`, `validate_input_file`).
    *   **`logging.py`**: Handles application-wide logging setup (assuming generic).

## 5. Summary of Refactoring Tasks for `utils`
The existing `src/core/utils/` directory will be refactored as follows:

*   A new top-level `src/utils/` directory will be created for truly generic utilities.
*   **`src/core/utils/setup.py`**: Eliminated.
    *   `validate_input_file` -> to new `src/utils/files.py`.
    *   STDF parsing specific setup functions (`initialize_record_entries`, `setup_record_flags`, `determine_endianness`, `determine_file_params`, `read_record_header`) -> to `src/core/stdf_parser/handler.py`.
*   **`src/core/utils/files.py`**: Its generic content moves to the new `src/utils/files.py`.
    *   Generic: `get_file_handle`, `is_binary` (if deemed generic), `is_file`, `find_stdf_files`.
    *   Process-specific: `managed_files`, `reset_and_check_binary` -> to `src/converter_service.py`.
*   **`src/core/utils/epoch.py`**: Its generic content moves to the new `src/utils/epoch.py`.
    *   Generic epoch-to-datetime/string conversion (Django dependency and SQLite format removed).
    *   ATDF-specific date formatting logic -> to `src/core/atdf_generator/formatters.py`.
*   **`src/core/utils/decorators.py`**: Moves to new `src/utils/decorators.py` (e.g., `timing_decorator`).
*   **`src/core/utils/logging.py`**: Moves to new `src/utils/logging.py` (assuming generic).
*   **`src/core/utils/database.py`**: Eliminated (functionality removed in prior refactoring).
*   **`src/core/utils/services.py`**: Eliminated (orchestration logic moves to `src/converter_service.py`).
*   **`src/core/utils/templates.py`**: Eliminated.
    *   STDF record type definitions (e.g., `get_record_types()`) -> to `src/core/stdf_parser/templates.py`.
    *   Any ATDF-specific formatting templates -> to `src/core/atdf_generator/templates.py`.

## 6. Implementation Steps Overview
1.  Create the new directory structure.
2.  Develop the initial `src/converter_service.py` with high-level orchestration logic.
3.  Refactor `src/cli.py` to use `converter_service.py`.
4.  Systematically refactor each `core` module (`stdf_parser`, `data_transformers`, `atdf_generator`), moving code from old locations, creating new files (`formatters.py`, etc.), and adjusting internal logic.
5.  Concurrently, refactor the `utils` modules, populating `src/utils/` and ensuring domain-specific utilities are moved appropriately.
6.  Update all import statements across the codebase.
7.  Thoroughly test each component and the end-to-end application.

This plan provides a clear roadmap for restructuring the application.