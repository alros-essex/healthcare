from abc import ABC, abstractmethod
from console.handle_state import StateHandler
from healthcare.storage import Storage
from console.state import State

from .console_utility import ConsoleUtility

class StateFireStaff(StateHandler, ABC):
    
    def __init__(self, next_state:State, type, storage:Storage):
        self._next_state = next_state
        self._type = type

    def handle(self, context:dict):
        # TODO
        pass
        '''
        ConsoleUtility.print_option('Please insert employee number')
        employee_number = ConsoleUtility.prompt_user_for_input()
        fired, message = clinic.fire(employee_number, self._type)
        if not fired:
            ConsoleUtility.print_error('There was an error: {}'.format(message))
        return self._next_state
        '''
