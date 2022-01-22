from datetime import datetime
import random

from healthcare.patient import Patient
from healthcare.clinic import Clinic
from console.state import State
from healthcare.receptionist import Receptionist

from .console_utility import ConsoleUtility
from .handle_state import StateHandler
from .handle_state_as_patient_base import StateAsPatientBaseHandler

class StateAsPatientGoHandler(StateAsPatientBaseHandler):

    def handle(self, clinic:Clinic):
        receptionist = self._find_a_receptionist(clinic)
        if receptionist is not None:
            self._talk_with_receptionist(clinic, receptionist)
        return State.AS_A_PATIENT

    def _find_a_receptionist(self, clinic:Clinic):
        if len(clinic.receptionists) == 0:
            ConsoleUtility.print_light('it looks like nobody works here (Clinic must hire at least one receptionist)')
            return None
        return clinic.receptionists[random.randint(0, len(clinic.receptionists)-1)]

    def _talk_with_receptionist(self, clinic:Clinic, receptionist:Receptionist):
        ConsoleUtility.print_conversation('Can I help you? What\'s your surnname?')
        surname = ConsoleUtility.prompt_user_for_input()
        ConsoleUtility.print_conversation('...and your first name?')
        name = ConsoleUtility.prompt_user_for_input()
        patient = receptionist.lookup_patient(clinic, name, surname)
        if patient is None:
            ConsoleUtility.print_conversation('You are not yet in the system, I need to register you as a patient')
            patient = self._register_new_patient(clinic, receptionist, name = name, surname = surname)
        ConsoleUtility.print_conversation('How can I help you?')
        appointments = receptionist.find_patient_appointments(clinic.appointment_schedule, patient)
        ConsoleUtility.print_conversation('Currently, you have {} appointment{}'.format(len(appointments),'s' if len(appointments)>1 else ''))
        for appointment in appointments:
            ConsoleUtility.print_light('{} with {}'.format(appointment.date, appointment.staff))

        # ConsoleUtility.print_option('I want to [R]egister as a patient')
  