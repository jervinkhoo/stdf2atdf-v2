# Refactoring Plan: Epoch to ATDF Datetime Conversion

## 1. Objective

To improve code organization and consistency by relocating and renaming the function responsible for converting epoch timestamps to ATDF-specific formatted datetime strings.

## 2. Current Situation

-   The function `get_datetime_from_epoch` is currently located in `src/utils/epoch.py`.
-   It converts an epoch time to an ATDF-specific string format (`HH:MM:SS DD-MMM-YYYY`) and handles timezone conversions using `pytz`.
-   Search results indicate its sole usage is within `src/core/atdf_generator/handler.py`.
-   Its current location in a generic `utils` directory is not ideal given its ATDF-specific output and usage.

## 3. Proposed Changes

The refactoring will be implemented in "Code" mode and involves the following steps:

### 3.1. Function Relocation and Renaming
-   **Function to move:** `get_datetime_from_epoch`
-   **Source File:** `src/utils/epoch.py`
-   **Destination File:** `src/core/atdf_generator/formatters.py`
-   **New Function Name:** `format_atdf_datetime_from_epoch` (to align with naming conventions in `formatters.py`)

### 3.2. Modifications to `src/core/atdf_generator/formatters.py`
-   The `format_atdf_datetime_from_epoch` function (formerly `get_datetime_from_epoch`) will be added to this file.
-   Necessary imports (`datetime`, `logging`, `pytz`) will be included at the top of `formatters.py` if not already present, or ensured to be available for the function. The `logging.getLogger(__name__)` specific to the function will also be included.

### 3.3. Modifications to `src/core/atdf_generator/handler.py`
-   The import statement for `get_datetime_from_epoch` (currently `from ...utils.epoch import get_datetime_from_epoch`) will be changed to import the renamed function from its new location: `from .formatters import format_atdf_datetime_from_epoch`.
-   All call sites of `get_datetime_from_epoch` within this file will be updated to use the new function name `format_atdf_datetime_from_epoch`.

### 3.4. Modifications to `src/utils/epoch.py`
-   The `get_datetime_from_epoch` function will be removed.
-   The `import pytz` statement, if solely used by the removed function, will also be removed.
-   The file `src/utils/epoch.py` will be kept if other utility functions exist or if the logger and basic `datetime`, `logging` imports are intended for future use in this module. If it becomes effectively empty, its deletion can be considered.

## 4. Reasoning for Changes
-   **Co-location:** Moves ATDF-specific formatting logic into the `atdf_generator` module, where it's exclusively used.
-   **Consistency:** Renames the function to match the `format_*` naming convention used in `src/core/atdf_generator/formatters.py`.
-   **Improved Modularity:** Makes the `src/utils` directory less coupled to ATDF-specific concerns.

## 5. Next Steps
1.  User approval of this plan.
2.  Write this plan to `epoch_refactor_plan.md`.
3.  Switch to "Code" mode to implement the changes detailed above.