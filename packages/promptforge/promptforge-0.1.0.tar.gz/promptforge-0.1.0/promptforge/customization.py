from typing import Dict

from promptforge.utils.symbols import SYMBOLS
from promptforge.utils.themes import THEME


def set_theme(custom_theme: Dict[str, str]) -> None:
    """
    Set a custom theme for PromptForge.

    Parameters
    ----------
    custom_theme : Dict[str, str]
        A dictionary containing theme keys and their corresponding style strings.

    Example
    -------
    set_theme({
        "prompt": "fg:#00ff00 bold",
        "input": "fg:#ffffff bg:#333333",
    })
    """
    for key, value in custom_theme.items():
        if key in THEME:
            THEME[key] = value
        else:
            raise ValueError(f"Invalid theme key: {key}")


def set_symbols(custom_symbols: Dict[str, str]) -> None:
    """
    Set custom symbols for PromptForge.

    Parameters
    ----------
    custom_symbols : Dict[str, str]
        A dictionary containing symbol keys and their corresponding Unicode characters or ASCII alternatives.

    Example
    -------
    set_symbols({
        "pointer": "►",
        "selected_checkbox": "☑",
        "unselected_checkbox": "☐",
    })
    """
    for key, value in custom_symbols.items():
        if key in SYMBOLS:
            SYMBOLS[key] = value
        else:
            raise ValueError(f"Invalid symbol key: {key}")


def get_current_theme() -> Dict[str, str]:
    """
    Get the current theme settings.

    Returns
    -------
    Dict[str, str]
        A dictionary containing the current theme settings.
    """
    return THEME.copy()


def get_current_symbols() -> Dict[str, str]:
    """
    Get the current symbol settings.

    Returns
    -------
    Dict[str, str]
        A dictionary containing the current symbol settings.
    """
    return SYMBOLS.copy()
