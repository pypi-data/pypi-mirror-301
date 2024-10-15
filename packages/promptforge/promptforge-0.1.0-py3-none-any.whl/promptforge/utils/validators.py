import re
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional


class BaseValidator(ABC):
    """
    Abstract base class for validators.
    """

    @abstractmethod
    def validate(self, input_value: str) -> Optional[str]:
        """
        Validate the input value.

        Parameters
        ----------
        input_value : str
            The input value to validate.

        Returns
        -------
        Optional[str]
            An error message if validation fails, None otherwise.
        """
        pass


class LengthValidator(BaseValidator):
    """
    Validates that input length is within a specified range.

    Parameters
    ----------
    min_length : int, optional
        Minimum length of the input (default is 0).
    max_length : Optional[int], optional
        Maximum length of the input (default is None).
    """

    def __init__(self, min_length: int = 0, max_length: Optional[int] = None):
        self.min_length = min_length
        self.max_length = max_length

    def validate(self, input_value: str) -> Optional[str]:
        """
        Validate the input length.

        Parameters
        ----------
        input_value : str
            The input value to validate.

        Returns
        -------
        Optional[str]
            An error message if validation fails, None otherwise.
        """
        if len(input_value) < self.min_length:
            return f"Input must be at least {self.min_length} characters long."
        if self.max_length and len(input_value) > self.max_length:
            return f"Input must be no more than {self.max_length} characters long."
        return None


class NonEmptyValidator(BaseValidator):
    """
    Validates that input is not empty.
    """

    def validate(self, input_value: str) -> Optional[str]:
        """
        Validate that the input is not empty.

        Parameters
        ----------
        input_value : str
            The input value to validate.

        Returns
        -------
        Optional[str]
            An error message if validation fails, None otherwise.
        """
        if not input_value.strip():
            return "Input cannot be empty."
        return None


class EmailValidator(BaseValidator):
    """
    Validates that the input is a valid email address.
    """

    EMAIL_REGEX = r"(^[\w\.-]+@[\w\.-]+\.\w{2,}$)"

    def validate(self, input_value: str) -> Optional[str]:
        """
        Validate that the input is a valid email address.

        Parameters
        ----------
        input_value : str
            The input value to validate.

        Returns
        -------
        Optional[str]
            An error message if validation fails, None otherwise.
        """
        if not re.match(self.EMAIL_REGEX, input_value):
            return "Please enter a valid email address."
        return None


class DateValidator(BaseValidator):
    """
    Validator for dates in YYYY-MM-DD format.
    """

    def validate(self, input_value: str) -> Optional[str]:
        try:
            datetime.strptime(input_value, "%Y-%m-%d")
            return None
        except ValueError:
            return "Please enter a date in the format YYYY-MM-DD."
