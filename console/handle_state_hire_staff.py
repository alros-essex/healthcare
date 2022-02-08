from abc import ABC, abstractmethod
from console.handle_state import StateHandler

class StateHireStaff(StateHandler, ABC):
    
    def __init__(self, next_state, storage):
        self._next_state = next_state
        self._storage = storage

    def handle(self, context:dict):
        from .console_utility import ConsoleUtility
        ConsoleUtility.print_option('Please insert name')
        name = ConsoleUtility.prompt_user_for_input()
        ok = False
        while not ok:
            ConsoleUtility.print_option('Please insert employee number')
            employee_number = ConsoleUtility.prompt_user_for_input()
            employee = self._get_instance(name, employee_number)
            if len(self._storage.select_employee(employee_number=employee.employee_number))>0:
                ConsoleUtility.print_error('employee number already present')
            else:
                ok = True
        self._storage.insert_employee(employee)
        return self._next_state

    @abstractmethod
    def _get_instance(self, name:str, employee_number:str):
        pass