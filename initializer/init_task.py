from abc import ABC, abstractmethod

class InitTask(ABC):
    """base task for the initialization, to be extended by all the other tasks"""

    def __init__(self, sub_steps_count:int, description:str):
        self._sub_steps_count = sub_steps_count
        self._description = description

    @abstractmethod
    def init(self, storage, schedule):
        """Initialize the headthcare and update the progress bar

        Args:
            healthcare: healthcare to be initialized
        Returns:
            None
        """
        pass

    def add_event_listener(self, event_listener):
        """to monitor the progress"""
        self._event_listener = event_listener

    @property
    def sub_steps_count(self):
        return self._sub_steps_count

    @property
    def description(self):
        return self._description

    def _notify(self, message:str):
        from .event import Event
        self._event_listener.notify(Event(message))
