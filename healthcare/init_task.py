from abc import ABC, abstractmethod
from .healthcare import Healthcare
from .event import Event
from .event_listener import EventListener

class InitTask(ABC):
    def __init__(self, sub_steps_count:int, description:str):
        self._sub_steps_count = sub_steps_count
        self._description = description

    @abstractmethod
    def init(self, healthcare:Healthcare):
        """Initialize the headthcare and update the progress bar

        Args:
            healthcare: healthcare to be initialized
        Returns:
            None
        """
        pass

    def add_event_listener(self, event_listener:EventListener):
        self._event_listener = event_listener

    @property
    def sub_steps_count(self):
        return self._sub_steps_count

    @property
    def description(self):
        return self._description

    def _notify(self, message:str):
        self._event_listener.notify(Event(message))
