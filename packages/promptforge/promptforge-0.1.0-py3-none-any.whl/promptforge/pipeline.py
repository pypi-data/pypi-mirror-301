from typing import Any, Callable, Dict, List, Optional

from promptforge.factory import PromptFactory
from promptforge.utils.cancel import cancel
from promptforge.utils.exceptions import (
    PromptCancelledException,
    PromptNavigationException,
)


def prompt_pipeline(
    prompt_definitions: List[Dict[str, Any]],
    on_cancel: Optional[Callable[[Dict[str, Any]], Any]] = None,
) -> Dict[str, Any]:
    """
    Group multiple prompts together and execute them sequentially.

    Parameters
    ----------
    prompt_definitions : List[Dict[str, Any]]
        A list of dictionaries where each dictionary defines a prompt with
        keys such as 'name', 'type', and other prompt-specific arguments.
    on_cancel : Optional[Callable[[Dict[str, Any]], Any]], optional
        A callback function that is called if any prompt is cancelled.
        It receives the results collected so far.

    Returns
    -------
    Dict[str, Any]
        A dictionary containing the results of the prompts.

    Raises
    ------
    PromptCancelledException
        If any prompt in the group is cancelled.
    """
    results = {}
    index = 0

    def handle_prompt_cancelled():
        """Handle prompt cancellation."""
        if on_cancel:
            on_cancel(results)
        else:
            cancel("Operation cancelled.")
        raise PromptCancelledException("Prompt cancelled by user.")

    try:
        while index < len(prompt_definitions):
            prompt_def = prompt_definitions[index]
            name = prompt_def.get("name")
            prompt_type = prompt_def.get("type")
            prompt_args = prompt_def.copy()
            prompt_args.pop("name", None)
            prompt_args.pop("type", None)

            try:
                prompt_args_evaluated = {}
                for key, value in prompt_args.items():
                    if callable(value):
                        prompt_args_evaluated[key] = value(results)
                    else:
                        prompt_args_evaluated[key] = value
                prompt = PromptFactory.create_prompt(
                    prompt_type, **prompt_args_evaluated
                )
                result = prompt.run()
                results[name] = result
                index += 1
            except PromptNavigationException as nav_exc:
                index = _handle_navigation_exception(nav_exc, prompt_definitions, index)
            except PromptCancelledException:
                handle_prompt_cancelled()
    except KeyboardInterrupt:
        handle_prompt_cancelled()

    return results


def _handle_navigation_exception(
    nav_exc: PromptNavigationException,
    prompt_definitions: List[Dict[str, Any]],
    current_index: int,
) -> int:
    """Handle navigation exceptions and determine the next prompt index."""
    target_prompt = nav_exc.target_prompt
    if target_prompt:
        # Find index of target prompt
        for i, pd in enumerate(prompt_definitions):
            if pd.get("name") == target_prompt:
                return i
        # Target prompt not found; stay at current index
        return current_index
    elif current_index > 0:
        return current_index - 1
    return current_index
