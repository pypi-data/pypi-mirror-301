import pytest
from prompt_toolkit.application import create_app_session
from prompt_toolkit.input import create_pipe_input
from prompt_toolkit.output import DummyOutput

from promptforge import (
    get_current_symbols,
    get_current_theme,
    prompt_pipeline,
    set_symbols,
    set_theme,
)
from promptforge.factory import PromptFactory
from promptforge.prompts.base import Prompt
from promptforge.renderers.base import PromptRenderer
from promptforge.utils.exceptions import PromptCancelledException
from promptforge.utils.validators import (
    DateValidator,
    EmailValidator,
    LengthValidator,
    NonEmptyValidator,
)


@pytest.fixture(autouse=True, scope="function")
def mock_input():
    with create_pipe_input() as pipe_input:
        with create_app_session(input=pipe_input, output=DummyOutput()):
            yield pipe_input


@pytest.fixture(scope="function")
def reset_theme_and_symbols():
    original_theme = get_current_theme()
    original_symbols = get_current_symbols()
    yield
    set_theme(original_theme)
    set_symbols(original_symbols)


def test_text_input_prompt(mock_input):
    mock_input.send_text("John Doe\r")
    result = prompt_pipeline(
        [
            {
                "name": "username",
                "type": "text_input",
                "message": "Enter your username:",
            }
        ]
    )
    assert result["username"] == "John Doe"


def test_select_prompt(mock_input):
    mock_input.send_text("\r")
    result = prompt_pipeline(
        [
            {
                "name": "color",
                "type": "select",
                "message": "Choose a color:",
                "choices": ["Red", "Green", "Blue"],
            }
        ]
    )
    assert result["color"] == "Red"


def test_multiselect_prompt(mock_input):
    mock_input.send_text(" \r")
    result = prompt_pipeline(
        [
            {
                "name": "fruits",
                "type": "multiselect",
                "message": "Choose fruits:",
                "choices": ["Apple", "Banana", "Cherry"],
            }
        ]
    )
    assert result["fruits"] == ["Apple"]


def test_confirm_prompt(mock_input):
    mock_input.send_text("\r")
    result = prompt_pipeline(
        [
            {
                "name": "agree",
                "type": "confirm",
                "message": "Do you agree?",
            }
        ]
    )
    assert result["agree"] is True


def test_cascading_select_prompt(mock_input):
    mock_input.send_text("\r\r")
    result = prompt_pipeline(
        [
            {
                "name": "location",
                "type": "cascading_select",
                "message1": "Select country:",
                "choices1": ["USA", "Canada"],
                "message2": "Select city:",
                "choices2_dict": {
                    "USA": ["New York", "Los Angeles"],
                    "Canada": ["Toronto", "Vancouver"],
                },
            }
        ]
    )
    assert result["location"] == ("USA", "New York")


def test_prompt_cancellation(mock_input):
    mock_input.send_text("\x03")
    with pytest.raises(PromptCancelledException):
        prompt_pipeline(
            [
                {
                    "name": "username",
                    "type": "text_input",
                    "message": "Enter your username:",
                }
            ]
        )


def test_set_and_get_theme():
    custom_theme = {
        "prompt": "fg:#00ff00 bold",
        "input": "fg:#ffffff bg:#333333",
    }
    set_theme(custom_theme)
    current_theme = get_current_theme()
    assert current_theme["prompt"] == custom_theme["prompt"]
    assert current_theme["input"] == custom_theme["input"]


def test_set_and_get_symbols():
    custom_symbols = {
        "pointer": "►",
        "selected_checkbox": "☑",
    }
    set_symbols(custom_symbols)
    current_symbols = get_current_symbols()
    assert current_symbols["pointer"] == custom_symbols["pointer"]
    assert current_symbols["selected_checkbox"] == custom_symbols["selected_checkbox"]


def test_multiple_prompts(mock_input):
    mock_input.send_text("John Doe\r\r\r")
    result = prompt_pipeline(
        [
            {
                "name": "username",
                "type": "text_input",
                "message": "Enter your username:",
            },
            {
                "name": "color",
                "type": "select",
                "message": "Choose a color:",
                "choices": ["Red", "Green", "Blue"],
            },
            {
                "name": "agree",
                "type": "confirm",
                "message": "Do you agree?",
            },
        ]
    )
    assert result["username"] == "John Doe"
    assert result["color"] == "Red"
    assert result["agree"] is True


def test_text_input_prompt_empty(mock_input):
    mock_input.send_text("\r")
    result = prompt_pipeline(
        [
            {
                "name": "username",
                "type": "text_input",
                "message": "Enter your username:",
            }
        ]
    )
    assert result["username"] == ""


def test_select_prompt_last_option(mock_input):
    mock_input.send_text("\x1B[B\x1B[B\r")
    result = prompt_pipeline(
        [
            {
                "name": "color",
                "type": "select",
                "message": "Choose a color:",
                "choices": ["Red", "Green", "Blue"],
            }
        ]
    )
    assert result["color"] == "Blue"


def test_select_prompt_wrap_around(mock_input):
    mock_input.send_text("\x1B[A\r")
    result = prompt_pipeline(
        [
            {
                "name": "color",
                "type": "select",
                "message": "Choose a color:",
                "choices": ["Red", "Green", "Blue"],
            }
        ]
    )
    assert result["color"] == "Blue"


def test_multiselect_prompt_all_options(mock_input):
    mock_input.send_text(" \x1B[B \x1B[B \r")
    result = prompt_pipeline(
        [
            {
                "name": "fruits",
                "type": "multiselect",
                "message": "Choose fruits:",
                "choices": ["Apple", "Banana", "Cherry"],
            }
        ]
    )
    assert set(result["fruits"]) == {"Apple", "Banana", "Cherry"}


def test_multiselect_prompt_min_selection(mock_input):
    mock_input.send_text("\r \r")
    result = prompt_pipeline(
        [
            {
                "name": "fruits",
                "type": "multiselect",
                "message": "Choose fruits:",
                "choices": ["Apple", "Banana", "Cherry"],
                "min_selection": 1,
            }
        ]
    )
    assert result["fruits"] == ["Apple"]


def test_multiselect_prompt_max_selection(mock_input):
    mock_input.send_text(" \x1B[B \x1B[B \r")
    result = prompt_pipeline(
        [
            {
                "name": "fruits",
                "type": "multiselect",
                "message": "Choose fruits:",
                "choices": ["Apple", "Banana", "Cherry"],
                "max_selection": 2,
            }
        ]
    )
    assert set(result["fruits"]) == {"Apple", "Banana"}


def test_confirm_prompt_toggle(mock_input):
    mock_input.send_text("\x1B[D\r")
    result = prompt_pipeline(
        [
            {
                "name": "agree",
                "type": "confirm",
                "message": "Do you agree?",
            }
        ]
    )
    assert result["agree"] is False


@pytest.mark.parametrize(
    "email",
    [
        "test.name+alias@example.co.uk",
        "invalid-email",
        "@example.com",
        "test@.com",
        "test@example.",
        "",
    ],
)
def test_email_validator(email):
    validator = EmailValidator()
    assert validator.validate(email) == "Please enter a valid email address."


@pytest.mark.parametrize(
    "input_str,min_length,max_length,is_valid",
    [
        ("abc", 3, 5, True),
        ("abcde", 3, 5, True),
        ("ab", 3, 5, False),
        ("abcdef", 3, 5, False),
        ("", 0, 5, True),
        ("abc", 0, None, True),
    ],
)
def test_length_validator(input_str, min_length, max_length, is_valid):
    validator = LengthValidator(min_length=min_length, max_length=max_length)
    assert (validator.validate(input_str) is None) == is_valid


@pytest.mark.parametrize(
    "input_str,is_valid",
    [
        ("abc", True),
        (" abc ", True),
        ("", False),
        ("  ", False),
        ("\t\r", False),
    ],
)
def test_non_empty_validator(input_str, is_valid):
    validator = NonEmptyValidator()
    assert (validator.validate(input_str) is None) == is_valid


@pytest.mark.parametrize(
    "date_str,is_valid",
    [
        ("2023-01-01", True),
        ("2023-12-31", True),
        ("2023-02-29", False),
        ("2024-02-29", True),
        ("2023-13-01", False),
        ("2023-01-32", False),
        ("01-01-2023", False),
        ("2023/01/01", False),
        ("invalid-date", False),
        ("", False),
    ],
)
def test_date_validator(date_str, is_valid):
    validator = DateValidator()
    assert (validator.validate(date_str) is None) == is_valid


def test_prompt_cancellation_middle_of_input(mock_input):
    mock_input.send_text("abc\x03")
    with pytest.raises(PromptCancelledException):
        prompt_pipeline(
            [
                {
                    "name": "username",
                    "type": "text_input",
                    "message": "Enter your username:",
                }
            ]
        )


def test_set_invalid_theme(reset_theme_and_symbols):
    with pytest.raises(ValueError):
        set_theme({"invalid_key": "some_value"})


def test_set_invalid_symbols(reset_theme_and_symbols):
    with pytest.raises(ValueError):
        set_symbols({"invalid_key": "some_value"})


def test_prompt_factory_unknown_type():
    with pytest.raises(ValueError):
        PromptFactory.create_prompt("unknown_type")


def test_custom_prompt_and_renderer():
    class CustomPrompt(Prompt):
        def _register_key_bindings(self):
            """"""
            pass

    class CustomRenderer(PromptRenderer):
        def create_layout(self):
            """"""
            pass

        def get_formatted_text(self):
            """"""
            pass

        def get_instructions(self):
            return "Custom instructions"

    PromptFactory._prompt_classes["custom"] = (CustomPrompt, CustomRenderer)

    prompt = PromptFactory.create_prompt("custom")
    assert isinstance(prompt, CustomPrompt)
    assert isinstance(prompt.renderer, CustomRenderer)
    assert prompt.get_instructions() == "Custom instructions"


def test_prompt_pipeline_empty_definitions():
    result = prompt_pipeline([])
    assert result == {}


# def test_prompt_pipeline_with_default_values(mock_input):
#     mock_input.send_text("\r\r")  # Accept default values
#     result = prompt_pipeline(
#         [
#             {
#                 "name": "username",
#                 "type": "text_input",
#                 "message": "Enter your username:",
#                 "default": "default_user",
#             },
#             {
#                 "name": "age",
#                 "type": "text_input",
#                 "message": "Enter your age:",
#                 "default": "30",
#             },
#         ]
#     )
#     assert result["username"] == "default_user"
#     assert result["age"] == "30"

# def test_prompt_navigation_multiple_prompts(mock_input):
#     mock_input.send_text("John\r/back\rJane\r")
#     result = prompt_pipeline(
#         [
#             {
#                 "name": "first_name",
#                 "type": "text_input",
#                 "message": "Enter your first name:",
#             },
#             {
#                 "name": "last_name",
#                 "type": "text_input",
#                 "message": "Enter your last name:",
#             },
#         ]
#     )
#     assert result["first_name"] == "Jane"
#     assert "last_name" not in result

# def test_cascading_select_prompt_no_second_level(mock_input):
#     mock_input.send_text(
#         "\x1B[B\r\r"
#     )  # Down arrow, Enter (select "Canada"), Enter (accept empty second level)
#     result = prompt_pipeline(
#         [
#             {
#                 "name": "location",
#                 "type": "cascading_select",
#                 "message1": "Select country:",
#                 "choices1": ["USA", "Canada"],
#                 "message2": "Select city:",
#                 "choices2_dict": {
#                     "USA": ["New York", "Los Angeles"],
#                     "Canada": [],
#                 },
#             }
#         ]
#     )
#     assert result["location"] == ("Canada", None)

# def test_prompt_navigation(mock_input):
#     mock_input.send_text("/back\r")
#     with pytest.raises(PromptNavigationException):
#         prompt_pipeline(
#             [
#                 {
#                     "name": "username",
#                     "type": "text_input",
#                     "message": "Enter your username:",
#                 }
#             ]
#         )
