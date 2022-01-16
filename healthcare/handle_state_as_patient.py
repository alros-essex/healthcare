from healthcare import receptionist
from .clinic import Clinic
from .console_utility import ConsoleUtility
from .state import State
from .handle_state import StateHandler

class StateAsPatientHandler(StateHandler):
    
    def __init__(self):
        self._next_state = {}
        self._next_state['C']=State.AS_A_PATIENT_CALL
        self._next_state['G']=State.AS_A_PATIENT_GO
        self._next_state['Q']=State.QUIT

    def handle(self, clinic:Clinic):
        self._print_options()
        return self._next_state[self._get_user_choice()]

    def _print_options(self):
        ConsoleUtility.print_light('You are patient now:')
        ConsoleUtility.print_option('[C]all the clinic')
        ConsoleUtility.print_option('[G]o to the clinic')
        ConsoleUtility.print_option('[Q]quit')
        
    def _get_user_choice(self):
        return ConsoleUtility.prompt_user_for_input(['C','G','Q'])