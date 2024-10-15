from typing import Dict, Generic, List, Optional, Tuple, TypeVar

from prompt_toolkit import Application
from prompt_toolkit.output.color_depth import ColorDepth

from promptforge.prompts.base import Prompt
from promptforge.renderers.cascading_select import CascadingSelectRenderer
from promptforge.utils.exceptions import PromptNavigationException

T = TypeVar("T")
U = TypeVar("U")


class CascadingSelectPrompt(Prompt, Generic[T, U]):
    """
    A prompt that allows the user to make a selection from a cascading menu.

    Parameters
    ----------
    message1 : str
        The message for the first selection.
    choices1 : List[T]
        The list of choices for the first selection.
    message2 : str
        The message for the second selection.
    choices2_dict : Dict[T, List[U]]
        A dictionary mapping first choices to second choices.
    default1 : Optional[T], optional
        The default selection for the first choice (default is None).
    default2 : Optional[U], optional
        The default selection for the second choice (default is None).
    """

    def __init__(
        self,
        message1: Optional[str] = "",
        choices1: Optional[List[T]] = None,
        message2: Optional[str] = "",
        choices2_dict: Optional[Dict[T, List[U]]] = None,
        default1: Optional[T] = None,
        default2: Optional[U] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.message1 = message1
        self.message2 = message2
        self.choices1 = choices1 or []
        self.choices2_dict = choices2_dict or {}
        self.default1 = default1 or ""
        self.default2 = default2 or ""
        self.current1 = (
            self.choices1.index(self.default1) if self.default1 in self.choices1 else 0
        )
        self.current2 = 0
        self.selected1 = self.choices1[self.current1] if self.choices1 else None
        self.selected2: Optional[U] = None
        self.state = "selecting_first"
        self.error_message: Optional[str] = None
        self.renderer = CascadingSelectRenderer(self)
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
        Register key bindings for the cascading select prompt.
        """

        @self.kb.add("up")
        @self.kb.add("k")
        def move_up(event):
            self._move_selection(-1)

        @self.kb.add("down")
        @self.kb.add("j")
        def move_down(event):
            self._move_selection(1)

        @self.kb.add("enter")
        def select(event):
            self._select_current_choice()

        @self.kb.add("c-c")
        def cancel(event):
            self.app.exit(result=None)

        @self.kb.add("<any>")
        def check_special_commands(event):
            if self._should_process_special_command(event):
                self._process_special_command(event)

    def _move_selection(self, direction: int):
        """Move the selection cursor in the given direction."""
        if self.state == "selecting_first":
            self.current1 = (self.current1 + direction) % len(self.choices1)
        else:
            choices2 = self.get_current_choices2()
            if choices2:
                self.current2 = (self.current2 + direction) % len(choices2)
        self.app.invalidate()

    def _select_current_choice(self):
        """Select the current choice based on the current state."""
        if self.state == "selecting_first":
            self._select_first_level()
        elif self.state == "selecting_second":
            self._select_second_level()
        self.app.invalidate()

    def _select_first_level(self):
        """Handle selection at the first level."""
        self.selected1 = self.choices1[self.current1]
        if not self.get_current_choices2():
            self.error_message = f"No options available for '{self.selected1}'."
            return
        self.state = "selecting_second"
        self.current2 = 0

    def _select_second_level(self):
        """Handle selection at the second level."""
        choices2 = self.get_current_choices2()
        if choices2:
            self.selected2 = choices2[self.current2]
            self.app.exit(result=(self.selected1, self.selected2))

    def _should_process_special_command(self, event) -> bool:
        """Determine if a special command should be processed."""
        data = event.data.strip()
        return data and data != "\n"

    def _process_special_command(self, event):
        """Process special commands entered by the user."""
        try:
            self._check_special_commands(event.data.strip())
        except PromptNavigationException as e:
            self.app.exit(exception=e)

    def get_current_choices2(self) -> List[U]:
        """
        Get the current list of second-level choices.

        Returns
        -------
        List[U]
            The list of choices for the second selection.
        """
        return self.choices2_dict.get(self.selected1, [])

    def get_current_message(self) -> str:
        """
        Get the current message based on the state.

        Returns
        -------
        str
            The current message.
        """
        return self.message1 if self.state == "selecting_first" else self.message2

    @classmethod
    def ask(
        cls,
        message1: str,
        choices1: List[T],
        message2: str,
        choices2_dict: Dict[T, List[U]],
        default1: Optional[T] = None,
        default2: Optional[U] = None,
        **kwargs,
    ) -> Optional[Tuple[T, U]]:
        """
        Class method to prompt the user for cascading selections.

        Parameters
        ----------
        message1 : str
            The message for the first selection.
        choices1 : List[T]
            The list of choices for the first selection.
        message2 : str
            The message for the second selection.
        choices2_dict : Dict[T, List[U]]
            A dictionary mapping first choices to second choices.
        default1 : Optional[T], optional
            The default selection for the first choice (default is None).
        default2 : Optional[U], optional
            The default selection for the second choice (default is None).

        Returns
        -------
        Optional[Tuple[T, U]]
            A tuple containing the first and second selections, or None if cancelled.
        """
        prompt = cls(
            message1=message1,
            choices1=choices1,
            message2=message2,
            choices2_dict=choices2_dict,
            default1=default1,
            default2=default2,
            **kwargs,
        )
        return prompt.run()
