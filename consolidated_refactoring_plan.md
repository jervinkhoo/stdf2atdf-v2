# Consolidated Refactoring and Analysis Plan

**Overall Goals:**
1.  Refactor the CLI to strictly accept only a single STDF file path as input.
2.  Streamline the call chain: `__main__.py` -> `cli.py` -> `converter.py`.
3.  Remove the intermediate `src/core/utils/services.py` layer.
4.  Ensure consistent logging setup by calling `setup_logging()` at the beginning of `cli.main()`.
5.  Analyze the codebase for unused functions, files, and obsolete artifacts post-refactoring.

**Detailed Steps:**

**Phase 1: Code Refactoring**

1.  **`src/utils/logging.py`:**
    *   No changes needed to the file itself. The existing `setup_logging()` function uses `logging.basicConfig()`, which is safe to call multiple times (it only configures if not already configured) and is suitable for our needs.

2.  **Modify `src/cli.py`:**
    *   **Imports:**
        *   **Remove:** `from .core.utils.services import process_files`
        *   **Remove:** `from .utils.files import find_stdf_files`
        *   **Ensure Present:** `from .utils.logging import setup_logging`
        *   **Ensure Present:** `from .converter import run_conversion`
        *   **Ensure Present:** `from pathlib import Path`
        *   **Ensure Present:** `from typing import Optional, List, Dict` (if not already for `file_processed_data` type hint)
    *   **`parse_arguments()` function:**
        *   Update `help` string for the `input` argument to: "Input STDF file path (must be a single file)."
    *   **`main()` function:**
        *   **Add at the very beginning:** `setup_logging()`
        *   **Input Handling (replace `find_stdf_files` logic):**
            ```python
            # args = parse_arguments() # Already exists
            input_path = Path(args.input)

            if not input_path.is_file():
                logger.error(f"Input path must be a file. Provided path '{input_path}' is invalid or a directory.")
                return 1 # Error exit code
            
            # validate_input_file() in converter.py will check if it's a valid STDF
            ```
        *   **Replace `process_files` call with direct `run_conversion` call (within the existing try-except block for general errors):**
            ```python
            # The existing try-except block in main() handles overall conversion failure.
            # The following logic replaces the call to process_files.
            
            stdf_input_str = str(input_path)
            atdf_output_str: Optional[str] = None
            if args.output:
                atdf_output_str = str(input_path.with_suffix('.atdf'))

            file_processed_data: Dict[str, List[Dict]] = run_conversion(
                stdf_input_file=stdf_input_str,
                atdf_output_file=atdf_output_str,
                records_to_process=args.records,
                preprocessor_type=args.preprocessor
            )
            # For the temporary verification step, wrap the single dict in a list
            processed_data_list = [file_processed_data] if file_processed_data else []
            logger.info("Conversion completed successfully for single file.") # Adjusted log message
            
            # The temporary verification part (lines 63-106) remains, operating on processed_data_list.
            # The outer try-except block in main() will catch exceptions from run_conversion.
            ```
    *   **`if __name__ == "__main__":` block:**
        *   **Remove:** `setup_logging()` (as `main()` now calls it).

3.  **Modify `src/__main__.py`:**
    *   **Remove:** `from .utils.logging import setup_logging` (if it's no longer used elsewhere in this file, which it shouldn't be after this change).
    *   **Remove:** `setup_logging()` call (as `cli.main()` now calls it).

4.  **Delete File:**
    *   `src/core/utils/services.py`

5.  **No Changes Needed For:**
    *   `run_conversion.py` (at the project root - will benefit from logging changes in `cli.main()`).
    *   `src/converter.py` (already handles single files and its logging will use the root config).

**Phase 2: Post-Refactoring Analysis**

1.  **Identify Unused Functions/Methods:**
    *   Specifically check `find_stdf_files()` in `src/utils/files.py`, as its primary caller (`cli.py`) will no longer use it.
    *   Scan other functions across the codebase for lack of calls.
2.  **Identify Unused Files/Modules:**
    *   Check if any `.py` files are no longer imported or executed by any active part of the application.
3.  **List Obsolete Files for Deletion:**
    *   Files with extensions like `.bak`, `.~`.
    *   Date-stamped files (e.g., `src/cli.py.20241209`, `src/converter_service.py.bak`, `src/core/atdf/parsers.py~`, `src/core/atdf/preprocessors/advantest.py~`, `src/core/stdf/preprocessing.py.20241208`, `src/core/utils/database.py.20241206`).

**Resulting Call Flow (Strict Single-File CLI with Centralized Logging):**

```mermaid
graph LR
    subgraph Entry Points
        direction LR
        EP1(python -m src) --> M(__main__.py);
        EP2(python src/cli.py) --> CLI_IF_MAIN(cli.py if __name__ == "__main__");
        EP3(python run_conversion.py) --> RC(run_conversion.py);
    end

    M --> CLI_MAIN(cli.py main());
    CLI_IF_MAIN --> CLI_MAIN;
    RC --> CLI_MAIN;

    CLI_MAIN -- Calls first --> SL(utils/logging.py setup_logging);
    CLI_MAIN -- Then validates single file & Calls --> CONV(converter.py run_conversion);
    
    CONV --> SP(stdf_parser handler);
    CONV --> AG(atdf_generator handler);
    CONV --> PRE(preprocessors);
    CONV --> UF(utils/files.py <br> managed_files <br> validate_input_file);
```

This plan aims to simplify the architecture, enforce single-file processing at the CLI level, ensure consistent logging, and prepare for cleanup of unused code.