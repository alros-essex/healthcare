from abc import ABC, abstractmethod

from console.state import State
from healthcare.clinic import Clinic

from .console_utility import ConsoleUtility

class StateHireStaff(ABC):
    
    def __init__(self, next_state:State):
        self._next_state = next_state

    def handle(self, clinic:Clinic):
        ConsoleUtility.print_option('Please insert name')
        name = ConsoleUtility.prompt_user_for_input()
        ConsoleUtility.print_option('Please insert employee number')
        employee_number = ConsoleUtility.prompt_user_for_input()
        employee = self._get_instance(name, employee_number)
        hired, message = clinic.hire(employee)
        if not hired:
            ConsoleUtility.print_error('There was an error: {}'.format(message))
        return self._next_state

    @abstractmethod
    def _get_instance(self, name:str, employee_number:str):
        pass