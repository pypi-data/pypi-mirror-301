from prompt_toolkit.filters import Condition
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.layout import HSplit, Layout, VSplit, Window
from prompt_toolkit.layout.containers import ConditionalContainer
from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl

from promptforge.renderers.base import PromptRenderer


class TextInputRenderer(PromptRenderer):
    """
    Renderer for text input prompts.

    This class is responsible for creating the layout and formatted text
    for text input prompts.
    """

    def create_layout(self) -> Layout:
        """
        Create and return the layout for the text input prompt.

        Returns
        -------
        Layout
            The layout for the text input prompt.
        """
        input_control = BufferControl(buffer=self.prompt.input_buffer)
        message_control = FormattedTextControl(text=self.get_formatted_text)
        error_container = ConditionalContainer(
            content=Window(
                height=1,
                content=FormattedTextControl(
                    text=lambda: (
                        f"{self.prompt.theme['error']} {self.prompt.symbols['error']} {self.prompt.error_message}"
                        if self.prompt.error_message
                        else ""
                    )
                ),
                style="class:error",
            ),
            filter=Condition(lambda: self.prompt.error_message is not None),
        )
        return Layout(
            HSplit(
                [
                    Window(height=1, content=message_control, style="class:prompt"),
                    Window(height=1, char=self.prompt.symbols["horizontal_line"]),
                    VSplit(
                        [
                            Window(
                                width=10,
                                content=FormattedTextControl(
                                    text=f"{self.prompt.symbols['input_prompt']} ",
                                    style="class:input_prompt",
                                ),
                            ),
                            Window(content=input_control, style="class:input"),
                        ]
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
        Get the formatted text for the text input prompt.

        Returns
        -------
        FormattedText
            The formatted text for the prompt message.
        """
        return FormattedText(
            [
                (
                    "class:prompt",
                    f"{self.prompt.symbols['pointer']} {self.prompt.message}",
                )
            ]
        )

    def get_instructions(self) -> str:
        """
        Get the instructions for using the text input prompt.

        Returns
        -------
        str
            The instruction text for the text input prompt.
        """
        return (
            "Type your input and press Enter to submit. "
            "Enter '/back' to go back or '/view' to see your answers."
        )
