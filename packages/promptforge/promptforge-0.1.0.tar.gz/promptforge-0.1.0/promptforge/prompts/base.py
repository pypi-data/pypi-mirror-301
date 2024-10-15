from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from prompt_toolkit.application import Application
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.styles import Style
from rich.console import Console

from promptforge.utils.event_emitter import EventEmitter
from promptforge.utils.exceptions import (
    PromptCancelledException,
    PromptNavigationException,
)
from promptforge.utils.symbols import SYMBOLS
from promptforge.utils.themes import THEME


class Prompt(EventEmitter, ABC):
    """
    Abstract base class for all prompts.

    Attributes
    ----------
    console : Console
        Rich console for output.
    app : Application
        Prompt Toolkit application instance.
    symbols : dict
        Dictionary of symbols used in prompts.
    theme : dict
        Dictionary of theme styles used in prompts.
    style : Style
        Prompt Toolkit style object.
    """

    def __init__(
        self,
        console: Optional[Console] = None,
        symbols: Optional[dict] = None,
        theme: Optional[dict] = None,
        results: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize the Prompt base class.

        Parameters
        ----------
        console : Optional[Console], optional
            Rich console instance (default is None).
        symbols : Optional[dict], optional
            Dictionary of symbols (default is None).
        theme : Optional[dict], optional
            Dictionary of theme styles (default is None).
        """
        super().__init__()
        self.console = console or Console()
        self.symbols = symbols or SYMBOLS
        self.theme = theme or THEME
        self.style = Style.from_dict(self.theme)
        self.app: Optional[Application] = None
        self.results = results or {}
        self.kb = KeyBindings()
        self.input_buffer = Buffer()
        self.error_message: Optional[str] = None
        self.renderer = None
        self._register_common_key_bindings()

    def get_formatted_text(self) -> FormattedText:
        return self.renderer.get_formatted_text()

    def get_instructions(self) -> str:
        return self.renderer.get_instructions()

    def display_current_answers(self):
        """
        Display the current answers collected so far.
        """
        if self.results:
            self.console.print("\n[bold]Current Answers:[/bold]")
            for key, value in self.results.items():
                self.console.print(f"{key}: {value}")
        else:
            self.console.print("\n[bold]No answers collected yet.[/bold]")

    def _register_common_key_bindings(self):
        """
        Register common key bindings for all prompts.
        """

        @self.kb.add("c-c")
        def cancel(event):
            self.app.exit(result=None)

    def _check_special_commands(self, text: str):
        """
        Check if the input text is a special command and handle it.

        Parameters
        ----------
        text : str
            The input text to check.

        Raises
        ------
        PromptNavigationException
            If the user wants to navigate back.
        """
        text = text.strip().lower()
        if text == "/back":
            raise PromptNavigationException()
        elif text == "/view":
            self.renderer.display_current_answers()
            raise PromptNavigationException(target_prompt=self.__class__.__name__)

    def run(self):
        """
        Run the prompt application.

        Returns
        -------
        Any
            The result of the prompt.
        """
        try:
            result = self.app.run()
        except KeyboardInterrupt:
            raise PromptCancelledException("Prompt cancelled by user.")

        if result is None:
            raise PromptCancelledException("Prompt cancelled by user.")
        return result

    @abstractmethod
    def _register_key_bindings(self):
        """
        Register key bindings for the prompt.
        """
        pass
