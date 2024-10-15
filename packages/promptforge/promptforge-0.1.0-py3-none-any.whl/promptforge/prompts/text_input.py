from typing import Optional

from prompt_toolkit import Application
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.output.color_depth import ColorDepth

from promptforge.prompts.base import Prompt
from promptforge.renderers.text_input import TextInputRenderer
from promptforge.utils.exceptions import PromptNavigationException
from promptforge.utils.validators import BaseValidator


class TextInputPrompt(Prompt):
    """
    A prompt that allows the user to input text with optional validation.

    Parameters
    ----------
    message : str
        The message to display to the user.
    default : Optional[str], optional
        The default input value (default is None).
    validate : Optional[BaseValidator], optional
        Validator to apply to the input (default is None).
    """

    def __init__(
        self,
        message: Optional[str] = "",
        default: Optional[str] = None,
        validate: Optional[BaseValidator] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.message = message or ""
        self.default = default or ""
        self.validate = validate or None
        self.input_buffer = Buffer()
        self.error_message: Optional[str] = None
        self.renderer = TextInputRenderer(self)
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
        Register key bindings for text input prompt.
        """

        @self.kb.add("enter")
        def submit(event):
            text = self.input_buffer.text.strip()
            try:
                self._check_special_commands(text)
            except PromptNavigationException as e:
                self.app.exit(exception=e)
                return

            if self.validate:
                error = self.validate.validate(text)
                if error:
                    self.error_message = error
                    self.app.invalidate()
                    return
            self.app.exit(result=text)

        @self.kb.add("c-c")
        def cancel(event):
            self.app.exit(result=None)

    @classmethod
    def ask(
        cls,
        message: str,
        default: Optional[str] = None,
        validate: Optional[BaseValidator] = None,
        **kwargs,
    ) -> str:
        """
        Class method to prompt the user for input.

        Parameters
        ----------
        message : str
            The message to display to the user.
        default : Optional[str], optional
            The default input value (default is None).
        validate : Optional[BaseValidator], optional
            Validator to apply to the input (default is None).

        Returns
        -------
        str
            The user's input.
        """
        prompt = cls(message=message, default=default, validate=validate, **kwargs)
        return prompt.run()
