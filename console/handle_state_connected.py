from healthcare.storage import Storage
from console.state import State

from .console_utility import ConsoleUtility
from .handle_state import StateHandler

class StateConnectedHandler(StateHandler):
    
    def __init__(self, storage:Storage):
        self._storage = storage
        self._next_state = {}
        self._next_state['E']=State.MANAGE_EMPLOYEES
        self._next_state['P']=State.MANAGE_PATIENTS
        self._next_state['A']=State.VIEW_APPOINTMENTS
        self._next_state['T']=State.AS_A_PATIENT
        self._next_state['Q']=State.QUIT

    def handle(self, context:dict):
        self._print_status()
        self._print_options()
        return self._next_state[self._get_user_choice()]

    def _print_status(self):
        ConsoleUtility.print_light('STATUS')
        ConsoleUtility.print_light('-       doctors: {}'.format(len(self._storage.select_doctors())))
        ConsoleUtility.print_light('-        nurses: {}'.format(len(self._storage.select_nurses())))
        ConsoleUtility.print_light('- receptionists: {}'.format(len(self._storage.select_receptionists())))
        ConsoleUtility.print_light('-      patients: {}'.format(len(self._storage.select_patients())))

    def _print_options(self):
        ConsoleUtility.print_option('Manage [E]employees')
        ConsoleUtility.print_option('Manage [P]atients')
        ConsoleUtility.print_option('View [A]ppointments')
        ConsoleUtility.print_option(' --- ')
        ConsoleUtility.print_option('Play as a patien[T]')
        ConsoleUtility.print_option(' --- ')
        ConsoleUtility.print_option('[Q]quit')
        
    def _get_user_choice(self):
        return ConsoleUtility.prompt_user_for_input(['E', 'P', 'A', 'T', 'Q'])