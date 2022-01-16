from abc import ABC, abstractmethod
from .clinic import Clinic
from .console_utility import ConsoleUtility
from .state import State
from .state_handler import StateHandler

class StateManageStaff(StateHandler, ABC):
    
    def __init__(self, managed_type, state_hire:State, state_fire:State):
        self._type = managed_type.__name__
        self._next_state = {}
        self._next_state['H'] = state_hire
        self._next_state['F'] = state_fire
        self._next_state['B']=State.MANAGE_EMPLOYEES

    def handle(self, clinic:Clinic):
        self._print_status(clinic)
        self._print_options()
        return self._next_state[self._get_user_choice()]

    def _print_status(self, clinic:Clinic):
        ConsoleUtility.print_light('{} MENU'.format(self._type.upper()))
        for staff in self._get_managed_staff(clinic):
            ConsoleUtility.print_light('- {}'.format(staff))

    def _print_options(self):
        ConsoleUtility.print_option('[H]ire a {}'.format(self._type))
        ConsoleUtility.print_option('[F]fire a {}'.format(self._type))
        ConsoleUtility.print_option('[B]ack')

    def _get_user_choice(self):
        return ConsoleUtility.prompt_user_for_input(['H', 'F', 'B'])

    @abstractmethod
    def _get_managed_staff(self):
        pass