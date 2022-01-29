from abc import ABC, abstractmethod

class StateHandler(ABC):

    @abstractmethod
    def handle(self, context:dict):
        pass
