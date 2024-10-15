from typing import Callable, Dict, List


class EventEmitter:
    """
    Handles event subscription and emission.

    Attributes
    ----------
    _subscribers : Dict[str, List[Callable]]
        Dictionary to store event subscribers.
    """

    def __init__(self):
        """Initialize the EventEmitter with an empty subscribers dictionary."""
        self._subscribers: Dict[str, List[Callable]] = {}

    def on(self, event: str, callback: Callable):
        """
        Subscribe to an event.

        Parameters
        ----------
        event : str
            The name of the event.
        callback : Callable
            The function to call when the event is emitted.
        """
        self._subscribers.setdefault(event, []).append(callback)

    def emit(self, event: str, *args, **kwargs):
        """
        Emit an event, calling all subscribed callbacks.

        Parameters
        ----------
        event : str
            The name of the event.
        *args
            Positional arguments to pass to the callbacks.
        **kwargs
            Keyword arguments to pass to the callbacks.
        """
        for callback in self._subscribers.get(event, []):
            callback(*args, **kwargs)
