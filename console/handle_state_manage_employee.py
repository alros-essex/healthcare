from abc import ABC
from .handle_state import StateHandler

class StateManageEmployee(StateHandler, ABC):
    
    def __init__(self):
        from console.state import State
        self._next_state = {}
        self._next_state['D'] = State.MANAGE_DOCTORS
        self._next_state['N'] = State.MANAGE_NURSES
        self._next_state['R'] = State.MANAGE_RECEPTIONISTS
        self._next_state['B']=State.CONNECTED

    def handle(self, _):
        self._print_options()
        return self._next_state[self._get_user_choice()]

    def _print_options(self):
        from .console_utility import ConsoleUtility
        ConsoleUtility.print_option('Manage [D]octors')
        ConsoleUtility.print_option('Manage [N]urses')
        ConsoleUtility.print_option('Manage [R]eceptionists')
        ConsoleUtility.print_option('[B]ack')

    def _get_user_choice(self):
        from .console_utility import ConsoleUtility
        return ConsoleUtility.prompt_user_for_input(['D', 'N', 'R', 'B'])
