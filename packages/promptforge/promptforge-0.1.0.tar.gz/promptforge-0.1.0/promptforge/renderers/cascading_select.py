from typing import TypeVar

from prompt_toolkit.filters import Condition
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.layout import HSplit, Layout, Window
from prompt_toolkit.layout.containers import ConditionalContainer
from prompt_toolkit.layout.controls import FormattedTextControl

from promptforge.renderers.base import PromptRenderer

T = TypeVar("T")
U = TypeVar("U")


class CascadingSelectRenderer(PromptRenderer):
    """
    Renderer for cascading select prompts.

    This class is responsible for creating the layout and formatted text
    for cascading select prompts.
    """

    def create_layout(self) -> Layout:
        """
        Create and return the layout for the cascading select prompt.

        Returns
        -------
        Layout
            The layout for the cascading select prompt.
        """
        body = FormattedTextControl(text=self.get_formatted_text)
        error_container = ConditionalContainer(
            content=Window(
                height=1,
                content=FormattedTextControl(
                    text=lambda: (
                        f"{self.prompt.symbols['error']} {self.prompt.error_message}"
                        if self.prompt.error_message
                        else ""
                    ),
                ),
                style="class:error",
            ),
            filter=Condition(lambda: self.prompt.error_message is not None),
        )
        return Layout(
            HSplit(
                [
                    Window(
                        height=1,
                        content=FormattedTextControl(
                            text=f"{self.prompt.symbols['pointer']} {self.prompt.get_current_message()}",
                            style="class:prompt",
                        ),
                    ),
                    Window(height=1, char=self.prompt.symbols["horizontal_line"]),
                    Window(
                        content=body,
                        wrap_lines=False,
                        always_hide_cursor=True,
                        allow_scroll_beyond_bottom=True,
                    ),
                    error_container,
                    Window(
                        height=1,
                        content=FormattedTextControl(
                            text=self.get_instructions(),
                            style="class:instruction",
                        ),
                    ),
                ]
            )
        )

    def get_formatted_text(self) -> FormattedText:
        """
        Get the formatted text for the cascading select prompt options.

        Returns
        -------
        FormattedText
            The formatted text for the cascading select prompt options.
        """
        result = []
        choices = (
            self.prompt.choices1
            if self.prompt.state == "selecting_first"
            else self.prompt.get_current_choices2()
        )
        current = (
            self.prompt.current1
            if self.prompt.state == "selecting_first"
            else self.prompt.current2
        )
        if not choices:
            return FormattedText(
                [
                    (
                        "class:error",
                        f"{self.prompt.symbols['error']} No options available.",
                    )
                ]
            )
        for idx, choice in enumerate(choices):
            is_active = idx == current
            pointer = self.prompt.symbols["pointer"] if is_active else " "
            style = "class:highlight" if is_active else ""
            result.append((style, f"{pointer} {choice}\n"))
        return FormattedText(result)

    def get_instructions(self) -> str:
        """
        Get the instructions for using the cascading select prompt.

        Returns
        -------
        str
            The instruction text for the cascading select prompt.
        """
        if self.prompt.state == "selecting_first":
            return (
                "Use arrows to navigate, Enter to select the first option. "
                "Enter '/back' to go back or '/view' to see your answers."
            )
        elif self.prompt.state == "selecting_second":
            return (
                "Use arrows to navigate, Enter to select the second option. "
                "Enter '/back' to go back or '/view' to see your answers."
            )
        else:
            return ""
