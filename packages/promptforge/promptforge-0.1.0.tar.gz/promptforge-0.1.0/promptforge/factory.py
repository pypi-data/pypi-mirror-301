from typing import Any, TypeVar

from promptforge.prompts.base import Prompt
from promptforge.prompts.cascading_select import CascadingSelectPrompt
from promptforge.prompts.confirm import ConfirmPrompt
from promptforge.prompts.multiselect import MultiSelectPrompt
from promptforge.prompts.select import SelectPrompt
from promptforge.prompts.text_input import TextInputPrompt
from promptforge.renderers.base import PromptRenderer
from promptforge.renderers.cascading_select import CascadingSelectRenderer
from promptforge.renderers.confirm import ConfirmRenderer
from promptforge.renderers.multiselect import MultiSelectRenderer
from promptforge.renderers.select import SelectRenderer
from promptforge.renderers.text_input import TextInputRenderer

P = TypeVar("P", bound="Prompt")
R = TypeVar("R", bound="PromptRenderer")


class PromptFactory:
    """
    Factory class to create prompt instances.

    Methods
    -------
    create_prompt(prompt_type: str, **kwargs)
        Create an instance of a prompt based on the prompt type.
    """

    _prompt_classes = {
        "text_input": (TextInputPrompt, TextInputRenderer),
        "select": (SelectPrompt, SelectRenderer),
        "multiselect": (MultiSelectPrompt, MultiSelectRenderer),
        "confirm": (ConfirmPrompt, ConfirmRenderer),
        "cascading_select": (CascadingSelectPrompt, CascadingSelectRenderer),
    }

    @classmethod
    def create_prompt(cls, prompt_type: str, **kwargs) -> Any:
        """
        Create an instance of a prompt based on the prompt type.

        Parameters
        ----------
        prompt_type : str
            The type of prompt to create.
        **kwargs
            Additional arguments to pass to the prompt constructor.

        Returns
        -------
        Prompt
            An instance of the requested prompt type.

        Raises
        ------
        ValueError
            If the prompt type is unknown.
        """
        prompt_class, renderer_class = cls._prompt_classes.get(
            prompt_type, (None, None)
        )
        if not prompt_class or not renderer_class:
            valid_types = ", ".join(cls._prompt_classes.keys())
            raise ValueError(
                f"Unknown prompt type: {prompt_type}. "
                f"Valid types are: {valid_types}"
            )
        prompt = prompt_class(**kwargs)
        prompt.renderer = renderer_class(prompt)
        return prompt
