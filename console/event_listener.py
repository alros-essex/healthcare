from abc import ABC, abstractmethod
from console.event import Event

class EventListener(ABC):
    
    @abstractmethod
    def notify(self, event:Event):
        pass