# STDF to ATDF Converter

A command-line tool for converting semiconductor test data from Standard Test Data Format (STDF) to ASCII Test Data Format (ATDF).

## Features

- Convert STDF files to ATDF format.
- Support for different equipment manufacturers (Advantest, Teradyne, Eagle) via record modifiers.
- Filter processing by specific record types.
- Comprehensive logging to `conversion.log`.
- Temporary verification step to display processed data in tabular format (for development).

## Installation

### Requirements

- Python 3.8+
- Dependencies listed in `requirements.txt`

```bash
# Create and activate a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Basic Usage

```bash
# Convert a single STDF file to ATDF
python -m src input.stdf --output

# Process a single STDF file, specifying a record modifier
python -m src input.stdf --output --modifier advantest

# Process only specific record types (e.g., MIR, PTR, PRR)
python -m src input.stdf --output --records MIR PTR PRR
```

### Command Line Arguments

| Argument | Short | Description |
|----------|-------|-------------|
| `input` | | Input STDF file path (must be a single file). |
| `--output` | `-o` | Generate ATDF output file (using input filename with .atdf extension). If not specified, ATDF data is processed but not written to a file. |
| `--records` | `-r` | Specific record types to process (e.g., MIR PTR PRR). If not specified, all supported records are processed. |
| `--modifier` | `-m` | Specify the record modifier to use (`advantest`, `teradyne`, `eagle`). Applies manufacturer-specific transformations. |

## Project Structure

```
stdf2atdf/
├── src/                       # Main source code
│   ├── __main__.py            # Main entry point for the application
│   ├── cli.py                 # Handles command-line argument parsing and main workflow
│   ├── converter.py           # Core STDF to ATDF conversion logic
│   ├── __init__.py
│   ├── core/                  # Core processing modules
│   │   ├── stdf_parser/       # Handles parsing of STDF files
│   │   │   ├── handler.py     # Reads STDF records, determines endianness, unpacks data
│   │   │   ├── templates.py   # Defines STDF record structures (templates)
│   │   │   └── unpackers.py   # Functions for unpacking various STDF data types
│   │   ├── atdf_generator/    # Handles generation of ATDF output
│   │   │   ├── handler.py     # Maps STDF data to ATDF format and writes ATDF files
│   │   │   ├── formatters.py  # Functions to format STDF data into ATDF fields
│   │   │   └── templates.py   # Defines ATDF record structures and output format
│   │   ├── data_transformers/ # Modules for transforming and enriching data
│   │   │   ├── id_enricher.py # Adds hierarchical wafer (w_id) and part (p_id) identifiers
│   │   │   └── record_modifiers/ # Applies manufacturer-specific data modifications
│   │   │       ├── base.py              # Base modifier logic and factory
│   │   │       ├── advantest_modifier.py # Advantest-specific modifications
│   │   │       ├── teradyne_modifier.py # Teradyne-specific modifications
│   │   │       └── eagle_modifier.py    # Eagle-specific modifications
│   │   └── __init__.py
│   └── utils/                 # Utility functions
│       ├── files.py           # File handling utilities (e.g., managed_files context manager)
│       ├── epoch.py           # (Currently contains only comments, epoch conversion moved)
│       ├── decorators.py      # Decorators, e.g., for timing function execution
│       └── __init__.py
├── requirements.txt           # Python dependencies
├── conversion.log             # Log file generated during conversion
└── README.md                  # This file
```

## Workflow Overview

1.  **CLI Parsing (`cli.py`):**
    *   Parses command-line arguments (`input` file, `--output` flag, `--records` filter, `--modifier` type).
    *   Sets up logging.
    *   Calls `run_conversion` from `converter.py`.

2.  **Conversion (`converter.py`):**
    *   `run_conversion` is the main orchestrator.
    *   Validates the input STDF file.
    *   Uses `managed_files` (from `utils/files.py`) to handle STDF input and optional ATDF output files.
    *   Determines STDF file parameters (e.g., endianness) using `stdf_parser/handler.py`.
    *   Iteratively reads STDF records:
        *   Reads record header (`stdf_parser/handler.py`).
        *   Retrieves STDF and ATDF record templates (`stdf_parser/templates.py`, `atdf_generator/templates.py`).
        *   Processes each record in `process_record`:
            *   Parses STDF data using `stdf_parser/handler.py::handle_stdf_entry` (which uses `stdf_parser/unpackers.py`).
            *   Generates a base ATDF dictionary using `atdf_generator/handler.py::handle_atdf_entry` (which uses `atdf_generator/formatters.py`).
            *   Applies record modification (if a `--modifier` is specified) using `data_transformers/record_modifiers/base.py::modify_record`.
            *   If `--output` is specified, writes the modified ATDF entry to the output file using `atdf_generator/handler.py::write_atdf_file`.
            *   Enriches the ATDF entry with hierarchical IDs (`w_id`, `p_id`) using `data_transformers/id_enricher.py::add_hierarchical_ids`.
            *   Collects processed ATDF entries.
    *   Returns a dictionary of processed ATDF entries.
    *   `cli.py` then (temporarily) prints this data in a tabular format using `pandas` for verification.

## Key Modules and Functionality

*   **`src/converter.py`**: Central workflow for reading STDF, transforming data, and generating ATDF.
*   **`src/cli.py`**: Handles user interaction and orchestrates the conversion process based on inputs.
*   **`src/core/stdf_parser/`**:
    *   `handler.py`: Manages reading STDF records and unpacking raw byte data based on record templates.
    *   `templates.py`: Defines the structure (fields, data types) of all known STDF records.
    *   `unpackers.py`: Contains functions to convert STDF binary data types into Python types.
*   **`src/core/atdf_generator/`**:
    *   `handler.py`: Converts the parsed STDF data (now in Python dictionaries) into ATDF formatted strings and writes them to a file.
    *   `templates.py`: Defines the structure and field order for ATDF records.
    *   `formatters.py`: Provides functions to format individual STDF fields into their ATDF string representations, including complex transformations (e.g., bit flags to characters, epoch time to ATDF date strings).
*   **`src/core/data_transformers/`**:
    *   `id_enricher.py`: Adds `w_id` (wafer ID) and `p_id` (part ID) to relevant records, maintaining hierarchical context.
    *   `record_modifiers/`: Allows for tester-specific data adjustments. For example, `advantest_modifier.py` might alter specific fields or add new ones based on Advantest conventions.
*   **`src/utils/`**:
    *   `files.py`: Provides utilities like `managed_files` for robust file opening/closing and `validate_input_file`.
    *   `decorators.py`: Includes a `timing_decorator` for performance measurement.

## Logging

All operations, warnings, and errors are logged to `conversion.log` in the project root directory. The console also shows INFO level messages.

## Record Modifiers (formerly Preprocessors)

Use the `--modifier` option to apply manufacturer-specific data transformations:

- `advantest`: For Advantest tester data.
- `teradyne`: For Teradyne tester data.
- `eagle`: For Eagle tester data.

These modifiers are implemented in the `src/core/data_transformers/record_modifiers/` directory.

## License

This project is licensed under the terms included in the LICENSE file.
