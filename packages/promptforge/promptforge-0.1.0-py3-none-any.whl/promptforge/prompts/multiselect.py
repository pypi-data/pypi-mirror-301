from typing import Generic, List, Optional, Set, TypeVar

from prompt_toolkit import Application
from prompt_toolkit.output.color_depth import ColorDepth

from promptforge.prompts.base import Prompt
from promptforge.renderers.multiselect import MultiSelectRenderer
from promptforge.utils.exceptions import PromptNavigationException

T = TypeVar("T")


class MultiSelectPrompt(Prompt, Generic[T]):
    """
    An interactive multi-select prompt.

    Parameters
    ----------
    message : str
        The message to display to the user.
    choices : List[T]
        The list of choices for the user to select from.
    default : Optional[List[T]], optional
        The default selected options (default is None).
    min_selection : int, optional
        Minimum number of selections required (default is 1).
    max_selection : Optional[int], optional
        Maximum number of selections allowed (default is None).
    max_display : int, optional
        Maximum number of options to display at once (default is 10).
    """

    def __init__(
        self,
        message: Optional[str] = "",
        choices: Optional[List[T]] = None,
        default: Optional[List[T]] = None,
        min_selection: Optional[int] = 1,
        max_selection: Optional[int] = None,
        max_display: Optional[int] = 10,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.message = message
        self.choices = choices or []
        self.selected: Set[T] = set(default) if default else set()
        self.current = 0
        self.error_message: Optional[str] = None
        self.min_selection = min_selection
        self.max_selection = max_selection
        self.max_display = max_display
        self.renderer = MultiSelectRenderer(self)
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
        Register key bindings for the multi-select prompt.
        """

        @self.kb.add("up")
        @self.kb.add("k")
        def move_up(event):
            self._move_cursor(-1)

        @self.kb.add("down")
        @self.kb.add("j")
        def move_down(event):
            self._move_cursor(1)

        @self.kb.add("space")
        def toggle_selection(event):
            self._toggle_current_selection()
            self.app.invalidate()

        @self.kb.add("enter")
        def submit(event):
            self._submit_selection()

        @self.kb.add("c-c")
        def cancel(event):
            self.app.exit(result=None)

        @self.kb.add("<any>")
        def check_special_commands(event):
            if self._should_process_special_command(event):
                self._process_special_command(event)

    def _move_cursor(self, direction: int):
        """Move the cursor up or down."""
        self.current = (self.current + direction) % len(self.choices)
        self.app.invalidate()

    def _toggle_current_selection(self):
        """Toggle the selection status of the current choice."""
        choice = self.choices[self.current]
        if choice in self.selected:
            self.selected.remove(choice)
            self.error_message = None
        elif self.max_selection is None or len(self.selected) < self.max_selection:
            self.selected.add(choice)
            self.error_message = None
        else:
            self.error_message = f"Maximum of {self.max_selection} selections allowed."

    def _submit_selection(self):
        """Submit the current selection."""
        if self.validate():
            self.app.exit(result=list(self.selected))
        else:
            self.app.invalidate()

    def _should_process_special_command(self, event) -> bool:
        """Determine if the event should trigger a special command."""
        data = event.data.strip()
        return data and data != "\n" and event.key != "space"

    def _process_special_command(self, event):
        """Process any special commands entered by the user."""
        try:
            self._check_special_commands(event.data.strip())
        except PromptNavigationException as e:
            self.app.exit(exception=e)

    def validate(self) -> bool:
        """
        Validate the current selections.

        Returns
        -------
        bool
            True if validation passes, False otherwise.
        """
        selection_count = len(self.selected)
        if selection_count < self.min_selection:
            self.error_message = f"Select at least {self.min_selection} options."
            return False
        if self.max_selection and selection_count > self.max_selection:
            self.error_message = f"Select no more than {self.max_selection} options."
            return False
        self.error_message = None
        return True

    @classmethod
    def ask(
        cls,
        message: str,
        choices: List[T],
        default: Optional[List[T]] = None,
        min_selection: int = 1,
        max_selection: Optional[int] = None,
        max_display: int = 10,
        **kwargs,
    ) -> List[T]:
        """
        Class method to prompt the user to select multiple options.

        Parameters
        ----------
        message : str
            The message to display to the user.
        choices : List[T]
            The list of choices for the user to select from.
        default : Optional[List[T]], optional
            The default selected options (default is None).
        min_selection : int, optional
            Minimum number of selections required (default is 1).
        max_selection : Optional[int], optional
            Maximum number of selections allowed (default is None).
        max_display : int, optional
            Maximum number of options to display at once (default is 10).

        Returns
        -------
        List[T]
            The user's selected options.
        """
        prompt = cls(
            message=message,
            choices=choices,
            default=default,
            min_selection=min_selection,
            max_selection=max_selection,
            max_display=max_display,
            **kwargs,
        )
        return prompt.run()
