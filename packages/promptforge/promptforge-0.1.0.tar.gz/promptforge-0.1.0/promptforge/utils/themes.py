import os

RED_BOLD = "fg:#ff0000 bold"  # Errors, critical messages
GREEN_BOLD = "fg:#00ff00 bold"  # Success messages, selections
YELLOW_BOLD = "fg:#ffff00 bold"  # Warnings, caution
BLUE_BOLD = "fg:#00afff bold"  # Prompts, information
GREY = "fg:#888888"  # Instructions, less important text
WHITE_BOLD = "fg:#ffffff bold"  # Important highlights on dark backgrounds

THEME = {
    "prompt": BLUE_BOLD,
    "pointer": BLUE_BOLD,
    "selected": GREEN_BOLD,
    "unselected": GREY,
    "highlight": "fg:#ffffff bg:#444444",  # High contrast for selected items
    "error": RED_BOLD,
    "instruction": GREY + " italic",
    "input": WHITE_BOLD,
    "spinner": BLUE_BOLD,
    "cancel": RED_BOLD,
}

# Disable colors if NO_COLOR is set
if "NO_COLOR" in os.environ:
    for key in THEME:
        THEME[key] = ""
