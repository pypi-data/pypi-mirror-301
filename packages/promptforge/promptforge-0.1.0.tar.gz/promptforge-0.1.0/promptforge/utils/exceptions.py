from typing import Optional


class PromptException(Exception):
    """
    Base exception class for prompt errors.
    """

    pass


class ValidationError(PromptException):
    """
    Exception raised for validation errors.

    Parameters
    ----------
    message : str
        The error message.
    """

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class PromptCancelledException(PromptException):
    """
    Exception raised when a prompt is cancelled by the user.
    """

    def __init__(self, message: str = "Prompt cancelled by user."):
        """
        Initialize the PromptCancelledException.

        Parameters
        ----------
        message : str, optional
            The error message (default is "Prompt cancelled by user.").
        """
        super().__init__(message)
        self.message = message


class PromptNavigationException(PromptException):
    """
    Exception raised when the user wants to navigate to a different prompt.
    """

    def __init__(self, target_prompt: Optional[str] = None):
        """
        Initialize the PromptNavigationException.

        Parameters
        ----------
        target_prompt : Optional[str], optional
            The key of the target prompt to navigate to (default is None, which means 'back').
        """
        super().__init__(f"Navigate to prompt: {target_prompt}")
        self.target_prompt = target_prompt
