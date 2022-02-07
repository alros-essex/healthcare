from abc import ABC, abstractmethod

class EventListener(ABC):
    
    @abstractmethod
    def notify(self, event):
        pass