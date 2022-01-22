from datetime import datetime

from healthcare.patient import Patient
from healthcare.clinic import Clinic
from console.state import State
from healthcare.receptionist import Receptionist

from .console_utility import ConsoleUtility
from .handle_state import StateHandler
from .handle_state_as_patient_base import StateAsPatientBaseHandler

class StateAsPatientCallHandler(StateAsPatientBaseHandler):

    def handle(self, clinic:Clinic):
        self._have_a_call(clinic)
        return State.AS_A_PATIENT

    def _have_a_call(self, clinic:Clinic):
        receptionist = clinic.call()
        if receptionist is None:
            ConsoleUtility.print_error('The phone rings, but nobody is answering (did they hire a receptionist?)')    
        else:
            self._talk_with(clinic, receptionist)

    def _talk_with(self, clinic:Clinic, receptionist:Receptionist):
        ConsoleUtility.print_conversation('{}, this is {}, how can I help you?'.format(clinic.name, receptionist.name))
        ConsoleUtility.print_option('I want to [R]egister as a patient')
        ConsoleUtility.print_option('I want to [M]ake an appointment')
        ConsoleUtility.print_option('I want to [C]ancel an appointment')
        ConsoleUtility.print_option('Can you remind me [W]hen is my appointment?')
        choice = ConsoleUtility.prompt_user_for_input(['R', 'M','C','W'])
        if choice == 'R':
            self._register_new_patient(clinic, receptionist)
        elif choice == 'M':
            self._make_an_appointment(clinic, receptionist)
        elif choice == 'C':
            self._cancel_an_appointment(receptionist)
        else:
            self._find_next_appointment(receptionist)
