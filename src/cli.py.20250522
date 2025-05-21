# src/cli.py
from pathlib import Path
import argparse
import logging
import pandas as pd # Added for temporary verification
import sys # Added for sys.exit in __main__
from typing import Optional, List, Dict # Added for type hints

# Removed: from .utils.files import find_stdf_files
# Removed: from .core.utils.services import process_files
from .converter import run_conversion # Added
def setup_logging():
    """Configure logging for the entire application."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('conversion.log'),
            logging.StreamHandler()
        ]
    )

logger = logging.getLogger(__name__)


def parse_arguments():
    parser = argparse.ArgumentParser(description='STDF to ATDF conversion tool')
    # Existing arguments
    parser.add_argument('input',
                        help='Input STDF file path (must be a single file).') # Updated help string
    parser.add_argument('--output', '-o',
                        action='store_true',
                        help='Generate ATDF output files (using input filename with .atdf extension)')
    parser.add_argument('--records', '-r',
                        nargs='*',
                        help='Specific record types to process')

    # Simplified modifier argument
    parser.add_argument('--modifier', '-m',  # Changed from --preprocessor, -p
                        choices=['advantest', 'teradyne', 'eagle'],
                        help='Specify the record modifier to use')  # Updated help text
    return parser.parse_args()


def main() -> int: # Explicitly indicate return type is exit code
    setup_logging() # Added logging setup call
    args = parse_arguments()
    input_path = Path(args.input)
    exit_code = 0 # Default success exit code

    try:
        if not input_path.is_file():
            logger.error(f"Input path must be a file. Provided path '{input_path}' is invalid or a directory.")
            return 1 # Error exit code
        
        # validate_input_file() in converter.py will check if it's a valid STDF

        # Call run_conversion directly for the single file
        stdf_input_str = str(input_path)
        atdf_output_str: Optional[str] = None
        if args.output:
            atdf_output_str = str(input_path.with_suffix('.atdf'))

        file_processed_data: Dict[str, List[Dict]] = run_conversion(
            stdf_input_file=stdf_input_str,
            atdf_output_file=atdf_output_str,
            records_to_process=args.records,
            modifier_type=args.modifier  # Changed from preprocessor_type and args.preprocessor
        )
        # For the temporary verification step, wrap the single dict in a list
        processed_data_list = [file_processed_data] if file_processed_data else []
        logger.info(f"Conversion completed successfully for {input_path}") # Adjusted log message

        # --- TEMPORARY VERIFICATION STEP ---
        # This section prints the enriched data as DataFrames for inspection.
        # It should be removed or commented out for production use.
        logger.info("\n--- TEMPORARY VERIFICATION OUTPUT ---")
        if not processed_data_list:
            logger.info("No data processed or returned by process_files.")
        
        for file_idx, file_data_dict in enumerate(processed_data_list): # This loop will run once or zero times
            if not isinstance(file_data_dict, dict):
                logger.warning(f"Data for file index {file_idx} is not a dictionary: {type(file_data_dict)}. Skipping.")
                continue

            # Since we process one file, input_path.name can be used directly
            # No need for input_files list or file_idx for filename
            print(f"\n\n--- Data for Input File: {input_path.name} ---")


            if not file_data_dict:
                print("  No records processed for this file.")
                continue

            for record_type, records_list in file_data_dict.items():
                print(f"\n-- Record Type: {record_type} --")
                if records_list:
                    try:
                        df = pd.DataFrame(records_list)
                        if len(df) > 10: # Only print head and tail if more than 10 rows
                            print("  First 5 rows:")
                            print(df.head(5).to_string())
                            print("\n  Last 5 rows:")
                            print(df.tail(5).to_string())
                        else: # Print all if 10 rows or less
                            print(df.to_string())
                    except Exception as df_e:
                        print(f"  Error creating/printing DataFrame for {record_type}: {df_e}")
                        print(f"  Raw records list (first 5 items): {records_list[:5]}") # Print first 5 items of raw list on error
                else:
                    print("  No records of this type.")
        logger.info("--- END OF TEMPORARY VERIFICATION OUTPUT ---\n")
        # --- END OF TEMPORARY VERIFICATION STEP ---

    except Exception as e:
        logger.error(f"Conversion failed for {input_path}: {str(e)}") # Adjusted error message
        exit_code = 1 # Indicate failure
        # Re-raise to ensure the main try-except catches it if not already caught.
        # The original structure already had a try-except that would set exit_code.
        # If run_conversion raises, this block catches it.
        # If we want to avoid re-raising, this block handles it.
        # For now, this is fine as the outer block in the original code would have caught it.
        # raise # Re-raising is fine if we want the main() caller to also see it.

    return exit_code # Return explicit exit code


if __name__ == "__main__":
    # setup_logging() # Removed, main() now calls it
    # Capture and exit with the code returned by main()
    sys.exit(main())
