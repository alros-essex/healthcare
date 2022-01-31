from abc import ABC, abstractmethod
from console.handle_state import StateHandler

from console.state import State
from healthcare.storage import Storage

from .console_utility import ConsoleUtility

class StateHireStaff(StateHandler, ABC):
    
    def __init__(self, next_state:State, storage:Storage):
        self._next_state = next_state
        self._storage = storage

    def handle(self, context:dict):
        ConsoleUtility.print_option('Please insert name')
        name = ConsoleUtility.prompt_user_for_input()
        ConsoleUtility.print_option('Please insert employee number')
        employee_number = ConsoleUtility.prompt_user_for_input()
        employee = self._get_instance(name, employee_number, self._storage)
        self._storage.insert_employee(employee)
        return self._next_state

    @abstractmethod
    def _get_instance(self, name:str, employee_number:str, storage:Storage):
        pass