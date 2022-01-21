from abc import ABC, abstractmethod
from healthcare.clinic import Clinic
from healthcare.state import State

from .console_utility import ConsoleUtility
from .handle_state import StateHandler

class StateManageEmployee(StateHandler, ABC):
    
    def __init__(self):
        self._next_state = {}
        self._next_state['D'] = State.MANAGE_DOCTORS
        self._next_state['N'] = State.MANAGE_NURSES
        self._next_state['R'] = State.MANAGE_RECEPTIONISTS
        self._next_state['B']=State.CONNECTED

    def handle(self, clinic:Clinic):
        self._print_options()
        return self._next_state[self._get_user_choice()]

    def _print_options(self):
        ConsoleUtility.print_option('Manage [D]octors')
        ConsoleUtility.print_option('Manage [N]urses')
        ConsoleUtility.print_option('Manage [R]eceptionists')
        ConsoleUtility.print_option('[B]ack')

    def _get_user_choice(self):
        return ConsoleUtility.prompt_user_for_input(['D', 'D', 'R', 'B'])
