from abc import ABC, abstractmethod
from healthcare.clinic import Clinic

class StateHandler(ABC):

    @abstractmethod
    def handle(self, healtcare:Clinic):
        pass
