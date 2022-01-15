from healthcare import receptionist
from .clinic import Clinic
from .console_utility import ConsoleUtility
from .state import State
from .state_handler import StateHandler

class StateConnectedHandler(StateHandler):
    
    def __init__(self):
        self._next_state = {}
        self._next_state['D']=State.MANAGE_DOCTORS
        self._next_state['N']=State.MANAGE_NURSES
        self._next_state['R']=State.MANAGE_RECEPTIONISTS

    def handle(self, clinic:Clinic):
        self._print_status(clinic)
        self._print_options()
        return self._next_state[self._get_user_choice()]

    def _print_status(self, clinic:Clinic):
        ConsoleUtility.print_light('STATUS')
        ConsoleUtility.print_light('-       doctors: {}'.format(len(clinic.doctors)))
        ConsoleUtility.print_light('-        nurses: {}'.format(len(clinic.nurses)))
        ConsoleUtility.print_light('- receptionists: {}'.format(len(clinic.receptionists)))

    def _print_options(self):
        ConsoleUtility.print_option('Manage [D]doctors')
        ConsoleUtility.print_option('Manage [N]nurses')
        ConsoleUtility.print_option('Manage [R]eceptionists')
        
    def _get_user_choice(self):
        return ConsoleUtility.prompt_user_for_input(['D','N','R'])