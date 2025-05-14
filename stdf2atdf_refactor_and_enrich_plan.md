# STDF to ATDF Converter: Analysis, Refactoring, and Enrichment Plan

## 1. Initial Project Analysis

### 1.1. Project Overview
The project is a command-line tool designed to convert semiconductor test data from Standard Test Data Format (STDF) to ASCII Test Data Format (ATDF).
Initially, it also included features for:
- Storing test data into SQLite databases.
- Processing multiple files in parallel.
- Support for preprocessors for different equipment manufacturers (Advantest, Teradyne, Eagle).

### 1.2. Key Files and Structure (Original)

-   **`run_conversion.py`**: Alternative runner script, calls `src.cli.main()`.
-   **`src/__main__.py`**: Main entry point when using `python -m src`, calls `src.cli.main()` and sets up logging.
-   **`src/cli.py`**: Handles command-line argument parsing and orchestrates the file processing.
    -   Uses `src.core.utils.files.find_stdf_files()`.
    -   Originally called `src.core.utils.services.process_files()` for parallel execution.
-   **`src/core/utils/services.py`**: Originally managed parallel processing using `ProcessPoolExecutor` and `calculate_optimal_workers`. It called `process_single_file` for each input.
    -   `process_single_file` called `src.converter.run_conversion()`.
-   **`src/converter.py` (`run_conversion` function)**: Core logic for converting a single STDF file.
    -   Reads STDF records sequentially.
    -   Calls `process_record` for each STDF record.
-   **`src/converter.py` (`process_record` function)**:
    -   Calls `src.core.stdf.handler.handle_stdf_entries()` for STDF unpacking.
    -   Calls `src.core.atdf.handler.handle_atdf_entries()` for ATDF conversion and preprocessing.
-   **`src/core/stdf/handler.py`**: Unpacks raw STDF binary data into Python dictionaries using templates and `src.core.stdf.unpackers.py`.
-   **`src/core/stdf/unpackers.py`**: Contains functions to unpack various STDF data types (e.g., `unpack_Cn`, `unpack_U2`, `unpack_Vn`).
-   **`src/core/atdf/handler.py`**: Converts unpacked STDF data to ATDF format using templates and `src.core.atdf.parsers.py`.
    -   Applies manufacturer-specific preprocessors via `src.core.atdf.preprocessors.base.py`.
    -   Writes ATDF records to an output file if specified.
    -   (Contained commented-out `update_counters` logic for `w_id`/`p_id`).
-   **`src/core/atdf/parsers.py`**: Contains functions to format specific STDF fields into ATDF string representations.
-   **`src/core/atdf/preprocessors/`**:
    -   `base.py`: Dispatches to specific manufacturer preprocessors.
    -   `advantest.py`, `teradyne.py`, `eagle.py`: Implement manufacturer-specific data modifications.
-   **`src/core/utils/templates.py`**: Provides functions to create/get STDF and ATDF record template structures.
-   **`src/core/utils/database.py`**: Originally handled SQLite database creation from processed ATDF data using Pandas DataFrames. Included `transform_record_data` to prepare records for DB schema.
-   **`src/core/utils/epoch.py`**: Handles epoch timestamp conversions.
-   **`src/core/utils/logging.py`**: Sets up logging for the application.
-   **`src/core/utils/files.py`**: File utility functions (e.g., `find_stdf_files`, `managed_files`).

### 1.3. Original Data Flow (Conceptual)

```mermaid
graph TD
    A[CLI Invocation: run_conversion.py / src/__main__.py] --> B(src/cli.py: main);
    B --> C{Find STDF Files};
    C --> D(src/core/utils/services.py: process_files);
    D --> E{ProcessPoolExecutor};
    E -- For each file --> F(src/core/utils/services.py: process_single_file);
    F --> G(src/converter.py: run_conversion);
    G --> H{Loop: Read STDF Record};
    H --> I(src/converter.py: process_record);
    I --> J(src/core/stdf/handler.py: handle_stdf_entries);
    J --> K(src/core/stdf/unpackers.py: unpack_dtype);
    K --> L[Unpacked STDF Data (Python Dict)];
    I --> M{ATDF Output?};
    M -- Yes --> N(src/core/atdf/handler.py: handle_atdf_entries);
    N --> O(src/core/atdf/parsers.py);
    O --> P[Base ATDF Data (Python Dict)];
    N --> Q{Preprocessor Specified?};
    Q -- Yes --> R(src/core/atdf/preprocessors/base.py: preprocess_record);
    R --> S[Manufacturer Preprocessor (e.g., advantest.py)];
    S --> T[Modified ATDF Data];
    Q -- No --> P;
    P --> U{Write to ATDF File?};
    T --> U;
    U -- Yes --> V(src/core/atdf/handler.py: write_atdf_file);
    V --> W([ATDF File Output]);
    G --> X{Database Output?};
    X -- Yes --> Y(src/core/utils/database.py: create_database_from_atdf);
    Y --> Z([SQLite Database Output]);

    subgraph Utils
        Templates([src/core/utils/templates.py])
        Epoch([src/core/utils/epoch.py])
        Logging([src/core/utils/logging.py])
    end

    J --> Templates;
    N --> Templates;
    V --> Epoch;
```

## 2. Refactoring and Enrichment Plan

The goal is to streamline the project into a more focused converter: STDF in, ATDF file out (optional), and/or an enriched list of dictionaries out (for an orchestrator).
Key features to remove: built-in database creation and parallel processing.
Key feature to add: `w_id`/`p_id` enrichment for the list of dictionaries output, while ensuring ATDF file output remains unchanged.

### 2.1. Core Refactoring: Removing Parallel Processing and Database Output

1.  **Simplify Command-Line Interface (`src/cli.py`):**
    *   Remove `--workers` and `--database` arguments.
    *   `main()` will orchestrate sequential processing of input files.

2.  **Overhaul Service Layer (`src/core/utils/services.py`):**
    *   Remove `calculate_optimal_workers` and `ProcessPoolExecutor` logic from `process_files`.
    *   `process_files` will iterate through `input_paths` sequentially, calling `process_single_file` for each.
    *   `process_single_file` will be simplified (remove `database` parameter), call `run_conversion`, and return its result.
    *   `process_files` returns a list of results (one per input file).

3.  **Streamline Converter (`src/converter.py` - `run_conversion` function):**
    *   Remove `output_atdf_database` parameter.
    *   Remove all logic related to `create_database_from_atdf`.
    *   The function will return the `atdf_processed_entries` dictionary (which will be enriched).

4.  **Deprecate/Remove Database Utilities (`src/core/utils/database.py`):**
    *   The entire `database.py` module will be removed.
    *   Remove `pandas` from `requirements.txt` if it was solely for this.

### 2.2. Implementing `w_id` and `p_id` Enrichment

This enrichment applies to the in-memory list of dictionaries returned by the converter.

5.  **Pass `counters` (in `src/converter.py`):**
    *   `run_conversion`: Initialize `counters = {'w_counter': 0, 'p_counter': 0}`. This resets for each file.
    *   Pass `counters` to `process_record`.
    *   `process_record`: Accept `counters` and pass it in `params` to `handle_atdf_entries`.

6.  **Create `add_hierarchical_ids` function (in `src/core/atdf/handler.py`):**
    *   **Signature:** `def add_hierarchical_ids(record_type, current_entry_dict, all_processed_entries_for_current_file, counters):`
    *   **Internal Helper (`find_latest_parent_record`):**
        *   Searches `all_processed_entries_for_current_file` for the most recent record of a specified `parent_record_type` (e.g., 'WIR' or 'PIR').
        *   Matches on `head_number` and `site_number` if present for contextual correctness.
    *   **Logic for `w_id`:**
        *   If `record_type == 'WIR'`: Increment `counters['w_counter']`, `current_entry_dict['w_id'] = counters['w_counter']`.
        *   If `record_type in ['PIR', 'PRR']` (and optionally `PTR`, `MPR`, `FTR`): Lookup `w_id` from the latest relevant `WIR`.
    *   **Logic for `p_id`:**
        *   If `record_type == 'PIR'`: Increment `counters['p_counter']`, `current_entry_dict['p_id'] = counters['p_counter']`.
        *   If `record_type in ['PTR', 'MPR', 'FTR', 'PRR']`: Lookup `p_id` from the latest relevant `PIR`.
    *   **Return:** The modified `current_entry_dict`.

7.  **Integrate into `src/core/atdf/handler.py` (`handle_atdf_entries`):**
    *   Extract `counters` from `params`.
    *   Sequence of operations:
        1.  `base_atdf_entry = handle_atdf_entry(...)` (Get initial ATDF dict).
        2.  `entry_for_processing_and_file = base_atdf_entry.copy()`.
        3.  If `preprocessor_type`, apply `preprocess_record` to `entry_for_processing_and_file`.
        4.  **If `params['atdf_file']` (ATDF file output enabled):**
            *   `write_atdf_file(params['atdf_file'], entry_for_processing_and_file, atdf_template)`
                *   Writes record to ATDF file *before* `w_id`/`p_id` are added.
        5.  **Enrich the dictionary for the in-memory list:**
            *   `enriched_entry = add_hierarchical_ids(record_type, entry_for_processing_and_file, atdf_processed_entries, counters)`.
        6.  `atdf_processed_entries[record_type].append(enriched_entry)`.

### 2.3. Outputs (Post-Refactoring)

8.  **ATDF File Output:** Optional, controlled by `--output` flag. Will *not* contain the `w_id`/`p_id` fields.
9.  **List of Dictionaries Output:** `run_conversion` returns `atdf_processed_entries` for the file, with records enriched with `w_id`/`p_id`. `src/cli.py` (if processing multiple files) will return a list of these dictionaries.

This refactoring will result in a more focused, componentized converter suitable for integration into larger data processing workflows.