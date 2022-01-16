from healthcare import receptionist
from .clinic import Clinic
from .console_utility import ConsoleUtility
from .state import State
from .handle_state import StateHandler

class StateConnectedHandler(StateHandler):
    
    def __init__(self):
        self._next_state = {}
        self._next_state['E']=State.MANAGE_EMPLOYEES
        self._next_state['P']=State.MANAGE_PATIENTS
        self._next_state['Q']=State.QUIT

    def handle(self, clinic:Clinic):
        self._print_status(clinic)
        self._print_options()
        return self._next_state[self._get_user_choice()]

    def _print_status(self, clinic:Clinic):
        ConsoleUtility.print_light('STATUS')
        ConsoleUtility.print_light('-       doctors: {}'.format(len(clinic.doctors)))
        ConsoleUtility.print_light('-        nurses: {}'.format(len(clinic.nurses)))
        ConsoleUtility.print_light('- receptionists: {}'.format(len(clinic.receptionists)))
        ConsoleUtility.print_light('-      patients: {}'.format(len(clinic.patients)))

    def _print_options(self):
        ConsoleUtility.print_option('Manage [E]employees')
        ConsoleUtility.print_option('Manage [P]atients')
        ConsoleUtility.print_option('Manage [Q]quit')
        
    def _get_user_choice(self):
        return ConsoleUtility.prompt_user_for_input(['E','P','Q'])