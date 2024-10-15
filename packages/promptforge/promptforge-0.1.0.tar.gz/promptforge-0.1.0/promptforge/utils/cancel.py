from typing import Any

from rich.console import Console


class _Cancel:
    def __repr__(self):
        return "Cancelled"


Cancelled = _Cancel()


def is_cancel(value: Any) -> bool:
    """
    Determines if the given value indicates a cancellation.
    """
    return value is Cancelled


def cancel(message: str = "Operation cancelled by user."):
    """
    Prints a cancellation message using the console.

    Parameters
    ----------
    message : str, optional
        The cancellation message to display (default is "Operation cancelled by user.").
    """
    console = Console()
    console.print(f"\n[bold red]{message}[/bold red]")
