
import typer

from rich.console import Console
from rich.table import Table
from typing import cast
from gspread.exceptions import GSpreadException

from google_sheet.services.spreadsheet import get_worksheet
from google_sheet.services.budget import (
    add_budget_amount,
    get_month_budget,
    normalize,
    update_budget_amount,
)

app = typer.Typer(help="Personal Budget CLI")
budget_app = typer.Typer(help="Budget management")

app.add_typer(budget_app, name="budget")

console = Console()


def handle_error(error: Exception) -> None:
    console.print(f"[bold red]Error:[/bold red] {error}")
    raise typer.Exit(code=1)


@budget_app.command("inspect")
def inspect_budget() -> None:
    """Display budget worksheet data."""

    try:
        worksheet = get_worksheet()
        values = cast(list[list[str]], worksheet.get_all_values())

        if not values:
            console.print("[yellow]Worksheet is empty[/yellow]")
            return

        table = Table(title="Budget Data")

        headers = values[0]

        for header in headers:
            table.add_column(header or "(empty)")

        for row in values[1:21]:
            padded_row = row + [""] * (len(headers) - len(row))
            table.add_row(*padded_row[:len(headers)])

        console.print(table)

    except Exception as error:
        handle_error(error)


@budget_app.command("headers")
def show_headers() -> None:
    """Display month and Planned/Spent headers."""

    try:
        worksheet = get_worksheet()

        values: list[list[str]] = cast(list[list[str]], worksheet.get_all_values())

        for row_number, row in enumerate(values[:2], start=1):
            console.print(
                f"[cyan]Row {row_number}:[/cyan] {row}"
            )

    except Exception as error:
        handle_error(error)


@budget_app.command("add")
def add(
    month: str = typer.Option(..., help="Month, e.g. Jan"),
    entry_type: str = typer.Option(
        ...,
        "--type",
        help="Planned or Spent",
    ),
    item: str = typer.Option(..., help="Budget item name"),
    amount: str = typer.Option(..., help="Amount to add"),
) -> None:
    """Add an amount to an empty budget cell."""

    try:
        worksheet = get_worksheet()

        cell = add_budget_amount(
            worksheet,
            month,
            entry_type,
            item,
            amount,
        )

        console.print(
            f"[green]Added successfully![/green] "
            f"{item} - {month} - {entry_type}: {amount} "
            f"(Cell: {cell})"
        )

    except Exception as error:
        handle_error(error)


@budget_app.command("update")
def update(
    month: str = typer.Option(..., help="Month, e.g. Jan"),
    entry_type: str = typer.Option(
        ...,
        "--type",
        help="Planned or Spent",
    ),
    item: str = typer.Option(..., help="Budget item name"),
    amount: str = typer.Option(..., help="New amount"),
) -> None:
    """Update an existing budget amount."""

    try:
        worksheet = get_worksheet()

        cell = update_budget_amount(
            worksheet,
            month,
            entry_type,
            item,
            amount,
        )

        console.print(
            f"[green]Updated successfully![/green] "
            f"{item} - {month} - {entry_type}: {amount} "
            f"(Cell: {cell})"
        )

    except Exception as error:
        handle_error(error)



@budget_app.command("show")
def show(
    month: str = typer.Option(
        ...,
        "--month",
        help="Month to display, e.g. Jan or January.",
    ),
    entry_type: str | None = typer.Option(
        None,
        "--type",
        help="Filter by Planned or Spent.",
    ),
    item: str | None = typer.Option(
        None,
        "--item",
        help="Filter by budget item.",
    ),
) -> None:
    """Display monthly budget details."""

    try:
        worksheet = get_worksheet()

        results: list[dict[str, str]] = get_month_budget(
            worksheet=worksheet,
            month=month,
            entry_type=entry_type,
            item=item,
        )

        if not results:
            console.print("[yellow]No budget records found.[/yellow]")
            return

        normalized_type: str | None = (
            normalize(entry_type) if entry_type else None
        )

        table = Table(title=f"{month.title()} Budget")
        table.add_column("Budget Item", style="cyan")

        if normalized_type is not None:
            table.add_column(normalized_type.title(), justify="right")
        else:
            table.add_column("Planned", justify="right")
            table.add_column("Spent", justify="right")

        for result in results:
            item_name: str = result["item"]

            if normalized_type is not None:
                amount: str = result.get(normalized_type, "")

                table.add_row(
                    item_name,
                    amount or "-",
                )
            else:
                planned: str = result.get("planned", "")
                spent: str = result.get("spent", "")

                table.add_row(
                    item_name,
                    planned or "-",
                    spent or "-",
                )

        console.print(table)

    except (ValueError, GSpreadException) as error:
        handle_error(error)


if __name__ == "__main__":
    app()
