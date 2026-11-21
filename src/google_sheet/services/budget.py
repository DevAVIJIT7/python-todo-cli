
from decimal import Decimal, InvalidOperation
from typing import cast
import gspread

def normalize(value: str) -> str:
    return " ".join(value.strip().casefold().split())

def normalize_month(value: str) -> str:
    return normalize(value)[:3]

def get_worksheet_values(
    worksheet: gspread.Worksheet,
) -> list[list[str]]:
    return cast(list[list[str]], worksheet.get_all_values())

def find_budget_cell(
    worksheet: gspread.Worksheet,
    month: str,
    entry_type: str,
    item: str,
) -> tuple[int, int]:
    """
    Find the Google Sheets row and column for a budget item.

    Assumptions:
    Row 1: Month names
    Row 2: Planned / Spent
    Column A: Budget item names
    Row 3 onwards: Budget data
    """

    values: list[list[str]] = get_worksheet_values(worksheet)

    if len(values) < 2:
        raise ValueError("Worksheet does not contain the required headers.")

    month_row: list[str] = values[0]
    type_row: list[str] = values[1]

    requested_month = normalize_month(month)
    requested_type = normalize(entry_type)
    requested_item = normalize(item)

    if requested_type not in ("planned", "spent"):
        raise ValueError("Type must be Planned or Spent.")

    # Find month and its corresponding Planned/Spent column.
    current_month = ""

    column_index = None

    for index in range(1, max(len(month_row), len(type_row))):
        month_value = month_row[index] if index < len(month_row) else ""
        type_value = type_row[index] if index < len(type_row) else ""

        # Merged month cells have a value only in the first column.
        if month_value.strip():
            current_month = normalize_month(month_value)

        if (
            current_month == requested_month
            and normalize(type_value) == requested_type
        ):
            column_index = index + 1  # Google Sheets is 1-indexed.
            break

    if column_index is None:
        raise ValueError(
            f"Could not find {month} / {entry_type} column."
        )

    # Find the budget item in column A.
    matching_rows = [
        row_number
        for row_number, row in enumerate(values[2:], start=3)
        if row and normalize(row[0]) == requested_item
    ]

    if not matching_rows:
        raise ValueError(f"Budget item '{item}' was not found.")

    if len(matching_rows) > 1:
        raise ValueError(f"Duplicate budget item found: '{item}'.")

    return matching_rows[0], column_index


def validate_amount(amount: str) -> str:
    try:
        value = Decimal(amount.replace(",", "").strip())
    except InvalidOperation:
        raise ValueError("Amount must be a valid number.")

    if not value.is_finite() or value < 0:
        raise ValueError("Amount must be a non-negative finite number.")

    return str(value)


def add_budget_amount(
    worksheet: gspread.Worksheet,
    month: str,
    entry_type: str,
    item: str,
    amount: str,
) -> str:
    row, column = find_budget_cell(
        worksheet, month, entry_type, item
    )

    current_value = worksheet.cell(row, column).value

    if current_value not in (None, ""):
        raise ValueError(
            f"Cell already contains {current_value}. Use update instead."
        )

    amount = validate_amount(amount)

    worksheet.update_cell(row, column, amount)

    return worksheet.cell(row, column).address


def update_budget_amount(
    worksheet: gspread.Worksheet,
    month: str,
    entry_type: str,
    item: str,
    amount: str,
) -> str:
    row, column = find_budget_cell(
        worksheet, month, entry_type, item
    )

    current_value = worksheet.cell(row, column).value

    if current_value in (None, ""):
        raise ValueError(
            "Cell is empty. Use add instead."
        )

    amount = validate_amount(amount)

    worksheet.update_cell(row, column, amount)

    return worksheet.cell(row, column).address


def get_budget_amount(
    worksheet: gspread.Worksheet,
    month: str,
    entry_type: str,
    item: str,
) -> str | None:
    row, column = find_budget_cell(
        worksheet, month, entry_type, item
    )

    return worksheet.cell(row, column).value

def get_month_budget(
    worksheet: gspread.Worksheet,
    month: str,
    entry_type: str | None = None,
    item: str | None = None,
) -> list[dict[str, str]]:
    values: list[list[str]] = get_worksheet_values(worksheet)

    if len(values) < 2:
        raise ValueError("Worksheet does not contain the required headers.")

    month_row: list[str] = values[0]
    type_row: list[str] = values[1]

    requested_month: str = normalize_month(month)
    requested_type: str | None = (
        normalize(entry_type) if entry_type else None
    )
    requested_item: str | None = normalize(item) if item else None

    if requested_type is not None and requested_type not in ("planned", "spent"):
        raise ValueError("Type must be Planned or Spent.")

    month_columns: dict[str, int] = {}
    current_month: str = ""

    for index in range(1, max(len(month_row), len(type_row))):
        month_value: str = (
            month_row[index] if index < len(month_row) else ""
        )
        type_value: str = (
            type_row[index] if index < len(type_row) else ""
        )

        if month_value.strip():
            current_month = normalize_month(month_value)

        if current_month == requested_month:
            normalized_type: str = normalize(type_value)

            if normalized_type in ("planned", "spent"):
                month_columns[normalized_type] = index

    if not month_columns:
        raise ValueError(f"Month '{month}' was not found.")

    if requested_type is not None:
        selected_types: list[str] = [requested_type]
    else:
        selected_types = ["planned", "spent"]

    results: list[dict[str, str]] = []

    for row in values[2:]:
        if not row or not row[0].strip():
            continue

        item_name: str = row[0]

        if requested_item and normalize(item_name) != requested_item:
            continue

        result: dict[str, str] = {"item": item_name}

        for selected_type in selected_types:
            column_index: int | None = month_columns.get(selected_type)

            if column_index is None:
                continue

            amount: str = (
                row[column_index] if column_index < len(row) else ""
            )

            result[selected_type] = amount

        results.append(result)

    if requested_item and not results:
        raise ValueError(f"Budget item '{item}' was not found.")

    return results