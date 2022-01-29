from datetime import datetime
from healthcare import storage
from healthcare import receptionist
from healthcare.appointment_schedule import AppointmentSchedule

from healthcare.patient import Patient
from console.state import State
from healthcare.receptionist import Receptionist
from healthcare.storage import Storage

from .console_utility import ConsoleUtility
from .handle_state import StateHandler
from .handle_state_as_patient_base import StateAsPatientBaseHandler

class StateAsPatientCallHandler(StateAsPatientBaseHandler):

    def __init__(self, storage:Storage, schedule:AppointmentSchedule, quick: bool = False):
        super().__init__(storage, quick=quick)
        self._storage = storage
        self._schedule = schedule

    def handle(self, context:dict):
        user = self._have_a_call(context.get('user'))
        context['user']=user
        return State.AS_A_PATIENT

    def _have_a_call(self, user:Patient):
        receptionist = self._find_receptionist()
        if receptionist is None:
            ConsoleUtility.print_error('The phone rings, but nobody is answering (did they hire a receptionist?)')  
            return user
        else:
            return self._talk_with(receptionist, user)

    def _find_receptionist(self):
        receptionists = self._storage.select_receptionists()
        if len(receptionists)==0:
            return None
        receptionist:Receptionist = receptionists[0]
        receptionist.connect_to_storage(self._storage)
        receptionist.connect_to_schedule(self._schedule)
        return receptionist

    def _talk_with(self, receptionist:Receptionist, user:Patient):
        ConsoleUtility.print_conversation('Clinic of Essex, this is {}, how can I help you?'.format(receptionist.name))
        ConsoleUtility.print_option('I want to [R]egister as a patient')
        ConsoleUtility.print_option('I want to [M]ake an appointment')
        ConsoleUtility.print_option('I want to [C]ancel an appointment')
        ConsoleUtility.print_option('Can you remind me [W]hen is my appointment?')
        choice = ConsoleUtility.prompt_user_for_input(['R', 'M','C','W'])
        if choice == 'R':
            return self._register_new_patient(receptionist, user)
        elif choice == 'M':
            return self._make_an_appointment(receptionist, user)
        elif choice == 'C':
            return self._cancel_an_appointment(receptionist)
        else:
            return self._find_next_appointment(receptionist, user)
