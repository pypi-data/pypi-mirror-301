from typing import Generic, List, Optional, TypeVar

from prompt_toolkit import Application
from prompt_toolkit.output.color_depth import ColorDepth

from promptforge.prompts.base import Prompt
from promptforge.renderers.select import SelectRenderer
from promptforge.utils.exceptions import PromptNavigationException

T = TypeVar("T")


class SelectPrompt(Prompt, Generic[T]):
    """
    A prompt that allows the user to select one option from a list.

    Parameters
    ----------
    message : str
        The message to display to the user.
    choices : List[T]
        The list of choices for the user to select from.
    default : Optional[T], optional
        The default selected option (default is None).
    """

    def __init__(
        self,
        message: Optional[str] = "",
        choices: Optional[List[T]] = None,
        default: Optional[T] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.message = message
        self.choices = choices or []
        self.current = self.choices.index(default) if default in self.choices else 0
        self.selected: Optional[T] = None
        self.error_message: Optional[str] = None
        self.renderer = SelectRenderer(self)
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
        Register key bindings for the select prompt.
        """

        @self.kb.add("up")
        @self.kb.add("k")
        def move_up(event):
            self.current = (self.current - 1) % len(self.choices)
            self.app.invalidate()

        @self.kb.add("down")
        @self.kb.add("j")
        def move_down(event):
            self.current = (self.current + 1) % len(self.choices)
            self.app.invalidate()

        @self.kb.add("enter")
        def select(event):
            self.selected = self.choices[self.current]
            self.app.exit(result=self.selected)

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
        choices: List[T],
        default: Optional[T] = None,
        **kwargs,
    ) -> T:
        """
        Class method to prompt the user to select an option.

        Parameters
        ----------
        message : str
            The message to display to the user.
        choices : List[T]
            The list of choices for the user to select from.
        default : Optional[T], optional
            The default selected option (default is None).

        Returns
        -------
        T
            The user's selected option.
        """
        prompt = cls(message=message, choices=choices, default=default, **kwargs)
        return prompt.run()
