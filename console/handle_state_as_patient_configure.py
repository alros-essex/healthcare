from healthcare.patient import Patient
from healthcare.clinic import Clinic

from .console_utility import ConsoleUtility
from .handle_state import StateHandler
from .state import State

class StateAsPatientConfigureHandler(StateHandler):

    def handle(self, clinic:Clinic, context:dict):
        ConsoleUtility.print_conversation('What\'s your surname?')
        surname = ConsoleUtility.prompt_user_for_input()
        ConsoleUtility.print_conversation('What\'s your name')
        name = ConsoleUtility.prompt_user_for_input()
        ConsoleUtility.print_conversation('What is your address?')
        address = ConsoleUtility.prompt_user_for_input()
        ConsoleUtility.print_conversation('What is your phone number?')
        # TODO validation
        phone = ConsoleUtility.prompt_user_for_input()
        context['user']=Patient(name, surname, address, phone)
        return State.AS_A_PATIENT