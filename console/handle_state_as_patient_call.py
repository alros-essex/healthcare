from datetime import datetime

from healthcare.patient import Patient
from healthcare.clinic import Clinic
from console.state import State
from healthcare.receptionist import Receptionist

from .console_utility import ConsoleUtility
from .handle_state import StateHandler
from .handle_state_as_patient_base import StateAsPatientBaseHandler

class StateAsPatientCallHandler(StateAsPatientBaseHandler):

    def __init__(self, quick: bool = False):
        super().__init__(quick=quick)

    def handle(self, clinic:Clinic, context:dict):
        user = self._have_a_call(clinic, context.get('user'))
        context['user']=user
        return State.AS_A_PATIENT

    def _have_a_call(self, clinic:Clinic, user:Patient):
        receptionist = clinic.call()
        if receptionist is None:
            ConsoleUtility.print_error('The phone rings, but nobody is answering (did they hire a receptionist?)')  
            return user
        else:
            return self._talk_with(clinic, receptionist, user)

    def _talk_with(self, clinic:Clinic, receptionist:Receptionist, user:Patient):
        ConsoleUtility.print_conversation('{}, this is {}, how can I help you?'.format(clinic.name, receptionist.name))
        ConsoleUtility.print_option('I want to [R]egister as a patient')
        ConsoleUtility.print_option('I want to [M]ake an appointment')
        ConsoleUtility.print_option('I want to [C]ancel an appointment')
        ConsoleUtility.print_option('Can you remind me [W]hen is my appointment?')
        choice = ConsoleUtility.prompt_user_for_input(['R', 'M','C','W'])
        if choice == 'R':
            return self._register_new_patient(clinic, receptionist, user)
        elif choice == 'M':
            return self._make_an_appointment(clinic, receptionist, user)
        elif choice == 'C':
            return self._cancel_an_appointment(receptionist)
        else:
            return self._find_next_appointment(receptionist)
