from typing import TypeVar

from prompt_toolkit.filters import Condition
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.layout import HSplit, Layout, Window
from prompt_toolkit.layout.containers import ConditionalContainer
from prompt_toolkit.layout.controls import FormattedTextControl

from promptforge.renderers.base import PromptRenderer

T = TypeVar("T")


class MultiSelectRenderer(PromptRenderer):
    """
    Renderer for multi-select prompts.

    This class is responsible for creating the layout and formatted text
    for multi-select prompts.
    """

    def create_layout(self) -> Layout:
        """
        Create and return the layout for the multi-select prompt.

        Returns
        -------
        Layout
            The layout for the multi-select prompt.
        """
        body = FormattedTextControl(text=self.get_formatted_text)
        window = Window(
            content=body,
            wrap_lines=False,
            always_hide_cursor=True,
            allow_scroll_beyond_bottom=True,
        )
        error_container = ConditionalContainer(
            content=Window(
                height=1,
                content=FormattedTextControl(
                    text=lambda: self.prompt.error_message or ""
                ),
                style="class:error",
            ),
            filter=Condition(lambda: self.prompt.error_message is not None),
        )
        return Layout(
            HSplit(
                [
                    Window(
                        height=1, content=FormattedTextControl(text=self.prompt.message)
                    ),
                    Window(
                        height=1,
                        content=FormattedTextControl(text=self.get_instructions),
                    ),
                    Window(height=1, char=self.prompt.symbols["horizontal_line"]),
                    window,
                    error_container,
                ]
            )
        )

    def get_formatted_text(self) -> FormattedText:
        """
        Get the formatted text for the multi-select prompt options.

        Returns
        -------
        FormattedText
            The formatted text for the multi-select prompt options.
        """
        result = []
        for idx, choice in enumerate(self.prompt.choices):
            is_active = idx == self.prompt.current
            is_selected = choice in self.prompt.selected
            pointer = self.prompt.symbols["pointer"] if is_active else " "
            checkbox = (
                self.prompt.symbols["selected_checkbox"]
                if is_selected
                else self.prompt.symbols["unselected_checkbox"]
            )
            style = "class:highlight" if is_active else ""
            result.append((style, f"{pointer} {checkbox} {choice}\n"))
        return FormattedText(result)

    def get_instructions(self) -> str:
        """
        Get the instructions for using the multi-select prompt.

        Returns
        -------
        str
            The instruction text for the multi-select prompt.
        """
        return (
            "Use arrows to navigate, Space to select, Enter to submit. "
            "Enter '/back' to go back or '/view' to see your answers."
        )
