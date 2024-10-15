import os
import sys


def is_unicode_supported() -> bool:
    """
    Determine if the system supports Unicode characters.

    Returns
    -------
    bool
        True if Unicode is supported, False otherwise.
    """
    return sys.platform != "win32" or "WT_SESSION" in os.environ


UNICODE_SUPPORTED = is_unicode_supported()

SYMBOLS = {
    "pointer": "❯" if UNICODE_SUPPORTED else ">",
    "selected_checkbox": "✔" if UNICODE_SUPPORTED else "[x]",
    "unselected_checkbox": "✖" if UNICODE_SUPPORTED else "[ ]",
    "selected": "◉" if UNICODE_SUPPORTED else "(*)",
    "unselected": "◯" if UNICODE_SUPPORTED else "( )",
    "line": "│" if UNICODE_SUPPORTED else "|",
    "horizontal_line": "─" if UNICODE_SUPPORTED else "-",
    "error": "✖" if UNICODE_SUPPORTED else "X",
    "input_prompt": "➤" if UNICODE_SUPPORTED else ">",
    "spinner_name": "dots",
}
