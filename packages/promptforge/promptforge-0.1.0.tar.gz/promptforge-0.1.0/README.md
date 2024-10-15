# PromptForge

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Versions](https://img.shields.io/pypi/pyversions/promptforge.svg)](https://pypi.org/project/promptforge/)

PromptForge is a powerful and flexible Python library for creating interactive command-line interfaces (CLIs) with rich, customizable prompts.

## Features

- Multiple prompt types: text input, select, multi-select, confirm, and cascading select
- Customizable styling and theming
- Input validation
- Easy integration with popular CLI frameworks like Typer and argparse
- Extensible architecture for creating custom prompt types
- Unicode support (when available)

## Installation

Install PromptForge using pip:

```bash
pip install promptforge
```

## Quick Start

Here's a simple example of how to use PromptForge:

```python
from promptforge import prompt_pipeline

prompt_definitions = [
    {
        "name": "username",
        "type": "text_input",
        "message": "Enter your username:",
    },
    {
        "name": "favorite_color",
        "type": "select",
        "message": "Choose your favorite color:",
        "choices": ["Red", "Green", "Blue", "Yellow"],
    },
    {
        "name": "confirm",
        "type": "confirm",
        "message": "Are you sure you want to proceed?",
    },
]

results = prompt_pipeline(prompt_definitions)
print(results)
```

## Prompt Types

PromptForge supports the following prompt types:

1. `text_input`: For free-form text input
2. `select`: For selecting a single option from a list
3. `multiselect`: For selecting multiple options from a list
4. `confirm`: For yes/no questions
5. `cascading_select`: For hierarchical selections

## Validation

You can add validation to your prompts:

```python
from promptforge import prompt_pipeline
from promptforge.utils.validators import EmailValidator, LengthValidator

prompt_definitions = [
    {
        "name": "email",
        "type": "text_input",
        "message": "Enter your email:",
        "validate": EmailValidator(),
    },
    {
        "name": "password",
        "type": "text_input",
        "message": "Enter your password:",
        "validate": LengthValidator(min_length=8),
    },
]

results = prompt_pipeline(prompt_definitions)
```

## Integration with Typer

PromptForge can be easily integrated with Typer:

```python
import typer
from promptforge import prompt_pipeline

app = typer.Typer()

@app.command()
def register():
    prompt_definitions = [
        {
            "name": "username",
            "type": "text_input",
            "message": "Enter your username:",
        },
        {
            "name": "password",
            "type": "text_input",
            "message": "Enter your password:",
        },
    ]
    
    results = prompt_pipeline(prompt_definitions)
    typer.echo(f"Registered user: {results['username']}")

if __name__ == "__main__":
    app()
```
## Customization

PromptForge offers flexible customization options, allowing you to tailor the appearance of your prompts to match your application's style.

### Custom Themes

You can set a custom theme using the `set_theme()` function. This allows you to modify the colors and styles of various prompt elements:

```python
from promptforge import set_theme

set_theme({
    "prompt": "fg:#00ff00 bold",
    "input": "fg:#ffffff bg:#333333",
    "selected": "fg:#ffff00 bold",
    "unselected": "fg:#888888",
    "highlight": "fg:#ffffff bg:#444444",
    "error": "fg:#ff0000 bold",
    "instruction": "fg:#888888 italic",
})
```

### Custom Symbols

Customize the symbols used in prompts with the `set_symbols()` function:

```python
from promptforge import set_symbols

set_symbols({
    "pointer": "►",
    "selected_checkbox": "☑",
    "unselected_checkbox": "☐",
    "horizontal_line": "─",
    "error": "✗",
    "input_prompt": "❯",
})
```

### Retrieving Current Settings

You can get the current theme and symbol settings using `get_current_theme()` and `get_current_symbols()` respectively:

```python
from promptforge import get_current_theme, get_current_symbols

current_theme = get_current_theme()
current_symbols = get_current_symbols()

print("Current theme:", current_theme)
print("Current symbols:", current_symbols)
```

### Applying Customizations

After setting your custom theme and symbols, they will be automatically applied to all subsequent prompts:

```python
from promptforge import prompt_pipeline, set_theme, set_symbols

# Set custom theme and symbols
set_theme({"prompt": "fg:#00ff00 bold", "selected": "fg:#ffff00 bold"})
set_symbols({"pointer": "►", "selected_checkbox": "☑"})

# Use customized prompts
prompt_definitions = [
    {
        "name": "username",
        "type": "text_input",
        "message": "Enter your username:",
    },
    {
        "name": "options",
        "type": "multiselect",
        "message": "Select options:",
        "choices": ["Option 1", "Option 2", "Option 3"],
    },
]

results = prompt_pipeline(prompt_definitions)
print(results)
```

These customization options allow you to create a unique and cohesive look for your command-line interface, enhancing the user experience of your application.

Note: When using custom symbols, be mindful of terminal compatibility. Some terminals may not support certain Unicode characters. PromptForge will fall back to ASCII alternatives when Unicode is not supported.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Typer](https://typer.tiangolo.com/) for CLI creation
- [Rich](https://rich.readthedocs.io/en/latest/) for terminal formatting
- [Prompt Toolkit](https://python-prompt-toolkit.readthedocs.io/en/master/) for interactive prompts

## Contact

If you have any questions or feedback, please open an issue on the [GitHub repository](https://github.com/victor-mariano-leite/promptforge).