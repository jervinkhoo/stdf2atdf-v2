# Plan to Enhance `cli.py` for Flexible Output Formats

This document outlines the plan to modify `src/cli.py` to allow the `--output` argument to accept multiple values (`atdf`, `json`) for generating different output file formats.

## 1. Modify Argument Parsing (`parse_arguments` function)

The existing `--output` / `-o` argument in the `parse_arguments()` function within `src/cli.py` needs to be updated.

*   **Current definition:**
    ```python
    # src/cli.py
    parser.add_argument('--output', '-o',
                        action='store_true',
                        help='Generate ATDF output files (using input filename with .atdf extension)')
    ```

*   **New definition:**
    *   Change `action='store_true'` to `nargs='+'` to allow one or more values.
    *   Add `choices=['atdf', 'json']` to specify the allowed output types.
    *   Update the `help` string to: `"Specify output formats. Choose 'atdf', 'json', or both. Files will be named based on the input file."`
    *   The updated argument definition will look like this:
    ```python
    # src/cli.py
    parser.add_argument('--output', '-o',
                        nargs='+',
                        choices=['atdf', 'json'],
                        help="Specify output formats. Choose 'atdf', 'json', or both. Files will be named based on the input file.")
    ```

## 2. Update Main Logic (`main` function)

In the `main()` function in `src/cli.py`, after `args = parse_arguments()`, the logic for determining output file paths needs to be adjusted.

*   **Current logic for `atdf_output_str`:**
    ```python
    # src/cli.py lines 60-62
    atdf_output_str: Optional[str] = None
    if args.output: # This will change based on the new args.output structure
        atdf_output_str = str(input_path.with_suffix('.atdf'))
    ```

*   **New logic for output strings:**
    *   Initialize `atdf_output_str: Optional[str] = None` and `json_output_str: Optional[str] = None`.
    *   Check the content of `args.output` (which will now be a list of strings like `['atdf', 'json']`, `['atdf']`, `['json']`, or `None` if not provided).
    *   If `args.output` is not `None`:
        *   If `'atdf'` is in `args.output`, set `atdf_output_str = str(input_path.with_suffix('.atdf'))`.
        *   If `'json'` is in `args.output`, set `json_output_str = str(input_path.with_suffix('.json'))`.
    *   This can be implemented as:
    ```python
    # src/cli.py
    atdf_output_str: Optional[str] = None
    json_output_str: Optional[str] = None

    if args.output: # args.output is now a list or None
        if 'atdf' in args.output:
            atdf_output_str = str(input_path.with_suffix('.atdf'))
        if 'json' in args.output:
            json_output_str = str(input_path.with_suffix('.json'))
    ```

*   The call to `run_conversion()` needs to be updated to pass the new `json_output_str`.
    *   **Current call:**
        ```python
        # src/cli.py lines 64-69
        file_processed_data: Dict[str, List[Dict]] = run_conversion(
            stdf_input_file=stdf_input_str,
            atdf_output_file=atdf_output_str,
            records_to_process=args.records,
            modifier_type=args.modifier
        )
        ```
    *   **New call:**
        *   Add the `json_output_file` argument:
        ```python
        # src/cli.py
        file_processed_data: Dict[str, List[Dict]] = run_conversion(
            stdf_input_file=stdf_input_str,
            atdf_output_file=atdf_output_str,
            json_output_file=json_output_str, # New argument
            records_to_process=args.records,
            modifier_type=args.modifier
        )
        ```

## 3. Visual Representation (Mermaid Diagram)

```mermaid
graph TD
    A[Start: User runs cli.py with --output] --> B{Parse Arguments};
    B -- '--output atdf json' --> C[args.output = ['atdf', 'json']];
    B -- '--output atdf' --> D[args.output = ['atdf']];
    B -- '--output json' --> E[args.output = ['json']];
    B -- No --output --> F[args.output = None];

    C --> G{Check 'atdf' in args.output};
    G -- Yes --> H[atdf_output_str = 'input.atdf'];
    H --> I{Check 'json' in args.output};
    I -- Yes --> J[json_output_str = 'input.json'];
    J --> K[Call run_conversion(..., atdf_output_file='input.atdf', json_output_file='input.json')];

    D --> L{Check 'atdf' in args.output};
    L -- Yes --> M[atdf_output_str = 'input.atdf'];
    M --> N{Check 'json' in args.output};
    N -- No --> O[json_output_str = None];
    O --> P[Call run_conversion(..., atdf_output_file='input.atdf', json_output_file=None)];

    E --> Q{Check 'atdf' in args.output};
    Q -- No --> R[atdf_output_str = None];
    R --> S{Check 'json' in args.output};
    S -- Yes --> T[json_output_str = 'input.json'];
    T --> U[Call run_conversion(..., atdf_output_file=None, json_output_file='input.json')];

    F --> V[atdf_output_str = None];
    V --> W[json_output_str = None];
    W --> X[Call run_conversion(..., atdf_output_file=None, json_output_file=None)];

    K --> Y[End];
    P --> Y;
    U --> Y;
    X --> Y;