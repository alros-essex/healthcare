from abc import ABC, abstractmethod
from healthcare.storage import Storage
from console.state import State

from .console_utility import ConsoleUtility
from .handle_state import StateHandler

class StateManageStaff(StateHandler, ABC):
    
    def __init__(self, managed_type, state_hire:State):
        self._type = managed_type.__name__
        self._next_state = {}
        self._next_state['H'] = state_hire
        self._next_state['B']=State.MANAGE_EMPLOYEES

    def handle(self, context:dict):
        self._print_status()
        self._print_options()
        return self._next_state[self._get_user_choice()]

    def _print_status(self):
        ConsoleUtility.print_light('{} MENU'.format(self._type.upper()))
        for staff in self._get_managed_staff():
            ConsoleUtility.print_light('- {}: {}'.format(staff.employee_number, staff.name))

    def _print_options(self):
        ConsoleUtility.print_option('[H]ire a {}'.format(self._type))
        ConsoleUtility.print_option('[B]ack')

    def _get_user_choice(self):
        return ConsoleUtility.prompt_user_for_input(['H', 'F', 'B'])

    @abstractmethod
    def _get_managed_staff(self):
        pass