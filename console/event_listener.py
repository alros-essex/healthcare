from abc import ABC, abstractmethod
from healthcare.event import Event

class EventListener(ABC):
    
    @abstractmethod
    def notify(self, event:Event):
        pass