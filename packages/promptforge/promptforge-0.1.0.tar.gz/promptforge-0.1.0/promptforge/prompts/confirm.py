from typing import Optional

from prompt_toolkit import Application
from prompt_toolkit.output.color_depth import ColorDepth

from promptforge.prompts.base import Prompt
from promptforge.renderers.confirm import ConfirmRenderer
from promptforge.utils.exceptions import PromptNavigationException


class ConfirmPrompt(Prompt):
    """
    A prompt that accepts a yes or no answer, returning a boolean value.

    Parameters
    ----------
    message : str
        The message to display to the user.
    default : bool, optional
        The default choice (True for Yes, False for No) (default is True).
    """

    def __init__(
        self,
        message: Optional[str] = "",
        default: bool = True,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.message = message
        self.default = default
        self.choice = default
        self.renderer = ConfirmRenderer(self)
        self._register_key_bindings()

        self.app = Application(
            layout=self.renderer.create_layout(),
            key_bindings=self.kb,
            style=self.style,
            full_screen=False,
            color_depth=ColorDepth.TRUE_COLOR,
            mouse_support=True,
            erase_when_done=True,
        )

    def _register_key_bindings(self):
        """
        Register key bindings for the confirm prompt.
        """

        @self.kb.add("left")
        @self.kb.add("h")
        @self.kb.add("right")
        @self.kb.add("l")
        def toggle(event):
            self.choice = not self.choice
            self.app.invalidate()

        @self.kb.add("enter")
        def submit(event):
            self.app.exit(result=self.choice)

        @self.kb.add("c-c")
        def cancel(event):
            self.app.exit(result=None)

        @self.kb.add("<any>")
        def check_special_commands(event):
            if event.data.strip() == "\n":
                return  # Skip Enter key
            if event.data.strip():
                try:
                    self._check_special_commands(event.data)
                except PromptNavigationException as e:
                    self.app.exit(exception=e)

    @classmethod
    def ask(
        cls,
        message: str,
        default: bool = True,
        **kwargs,
    ) -> bool:
        """
        Class method to prompt the user for confirmation.

        Parameters
        ----------
        message : str
            The message to display to the user.
        default : bool, optional
            The default choice (True for Yes, False for No) (default is True).

        Returns
        -------
        bool
            True if the user confirmed, False otherwise.
        """
        prompt = cls(message=message, default=default, **kwargs)
        return prompt.run()
