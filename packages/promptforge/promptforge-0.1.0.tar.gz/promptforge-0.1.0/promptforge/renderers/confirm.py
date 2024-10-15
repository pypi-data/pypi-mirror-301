from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.layout import HSplit, Layout, Window
from prompt_toolkit.layout.controls import FormattedTextControl

from promptforge.renderers.base import PromptRenderer


class ConfirmRenderer(PromptRenderer):
    """
    Renderer for confirm prompts.

    This class is responsible for creating the layout and formatted text
    for confirm prompts.
    """

    def create_layout(self) -> Layout:
        """
        Create and return the layout for the confirm prompt.

        Returns
        -------
        Layout
            The layout for the confirm prompt.
        """
        body = FormattedTextControl(text=self.get_formatted_text)
        return Layout(
            HSplit(
                [
                    Window(
                        height=1, content=FormattedTextControl(text=self.prompt.message)
                    ),
                    Window(height=1, char=self.prompt.symbols["horizontal_line"]),
                    Window(height=1, content=body),
                    Window(
                        height=1,
                        content=FormattedTextControl(text=self.get_instructions),
                        style="class:instruction",
                    ),
                ]
            )
        )

    def get_formatted_text(self) -> FormattedText:
        """
        Get the formatted text for the confirm prompt options.

        Returns
        -------
        FormattedText
            The formatted text for the confirm prompt options.
        """
        yes_style = "class:selected" if self.prompt.choice else "class:unselected"
        no_style = "class:selected" if not self.prompt.choice else "class:unselected"
        yes_checkbox = (
            self.prompt.symbols["selected_checkbox"]
            if self.prompt.choice
            else self.prompt.symbols["unselected_checkbox"]
        )
        no_checkbox = (
            self.prompt.symbols["selected_checkbox"]
            if not self.prompt.choice
            else self.prompt.symbols["unselected_checkbox"]
        )
        return FormattedText(
            [
                (yes_style, f"{yes_checkbox} Yes "),
                (no_style, f"{no_checkbox} No"),
            ]
        )

    def get_instructions(self) -> str:
        """
        Get the instructions for using the confirm prompt.

        Returns
        -------
        str
            The instruction text for the confirm prompt.
        """
        return (
            "Use Left/Right arrows to toggle, Enter to confirm. "
            "Enter '/back' to go back or '/view' to see your answers."
        )
