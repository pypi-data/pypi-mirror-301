from abc import ABC, abstractmethod

from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.layout import Layout


class PromptRenderer(ABC):
    """
    Abstract base class for prompt renderers.

    This class defines the interface for creating layouts and formatted text
    for different types of prompts.

    Parameters
    ----------
    prompt : Prompt
        The prompt instance that this renderer is associated with.

    Attributes
    ----------
    prompt : Prompt
        The prompt instance that this renderer is associated with.
    """

    def __init__(self, prompt):
        self.prompt = prompt

    def display_current_answers(self):
        """
        Display the current answers collected so far.
        """
        self.prompt.console.print("\n[bold]Current Answers:[/bold]")
        if self.prompt.results:
            for key, value in self.prompt.results.items():
                self.prompt.console.print(f"- {key}: {value}")
        else:
            self.prompt.console.print("No answers collected yet.")
        self.prompt.console.print()  # Add an empty line

    @abstractmethod
    def create_layout(self) -> Layout:
        """
        Create and return the layout for the prompt.

        Returns
        -------
        Layout
            The layout for the prompt.
        """
        pass

    @abstractmethod
    def get_formatted_text(self) -> FormattedText:
        """
        Get the formatted text for the prompt.

        Returns
        -------
        FormattedText
            The formatted text for the prompt.
        """
        pass

    @abstractmethod
    def get_instructions(self) -> str:
        """
        Get the instructions for using the prompt.

        Returns
        -------
        str
            The instruction text for the prompt.
        """
        pass
