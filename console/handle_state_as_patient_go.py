from datetime import datetime
import enum
import random
from healthcare.appointment import Appointment
from healthcare.healthcare_professional import HealthcareProfessional

from healthcare.patient import Patient
from healthcare.clinic import Clinic
from console.state import State
from healthcare.receptionist import Receptionist

from .console_utility import ConsoleUtility
from .handle_state import StateHandler
from .handle_state_as_patient_base import StateAsPatientBaseHandler

class StateAsPatientGoHandler(StateAsPatientBaseHandler):

    def __init__(self, quick: bool = False):
        super().__init__(quick=quick)

    def handle(self, clinic:Clinic, context:dict):
        receptionist = self._find_a_receptionist(clinic)
        if receptionist is not None:
            user = self._talk_with_receptionist(clinic, receptionist, context)
            context['user'] = user
        return State.AS_A_PATIENT_GO

    def _find_a_receptionist(self, clinic:Clinic):
        if len(clinic.receptionists) == 0:
            ConsoleUtility.print_light('it looks like nobody works here (Clinic must hire at least one receptionist)')
            return None
        return clinic.receptionists[random.randint(0, len(clinic.receptionists)-1)]

    def _talk_with_receptionist(self, clinic:Clinic, receptionist:Receptionist, context):
        user:Patient = context.get('user')
        patient = self._front_desk_identity_user(clinic, receptionist, user)
        appointments = self._print_appointments(clinic, receptionist, patient)
        context['appointment'] = appointments
        self._pause()
        ConsoleUtility.print_conversation('How can I help you?')
        ConsoleUtility.print_option('[M]ake an appointment')
        if len(appointments) > 0:
            ConsoleUtility.print_option('[S]ee a doctor (next appointment)')
            ConsoleUtility.print_option('[C]ancel appointment')
        ConsoleUtility.print_option('[G]o away')
        input = ConsoleUtility.prompt_user_for_input(options=['M','S','C','G'])
        if input == 'M':
            self._make_an_appointment(clinic, receptionist, user=patient)
        elif input == 'S':
            self._see_staff(clinic, patient, appointments[0])
        elif input == 'C':
            self._cancel_an_appointment(clinic, receptionist, patient=patient)
        else:
            pass

        return patient

    def _front_desk_identity_user(self, clinic:Clinic, receptionist:Receptionist, user:Patient) -> Patient:
        if user is not None:
            # handle configuration
            ConsoleUtility.print_conversation('Can I help you?')
            self._pause()
            ConsoleUtility.print_light('My name is {}'.format(user))
            self._pause()
            name = user.firstname
            surname = user.surname
        else:
            ConsoleUtility.print_conversation('Can I help you? What\'s your surnname?')
            surname = ConsoleUtility.prompt_user_for_input()
            ConsoleUtility.print_conversation('...and your first name?')
            name = ConsoleUtility.prompt_user_for_input()
        patient = receptionist.lookup_patient(clinic, name, surname)
        if patient is None:
            ConsoleUtility.print_conversation('You are not yet in the system, I need to register you as a patient')
            patient = self._register_new_patient(clinic, receptionist, name = name, surname = surname, patient=user)
        return patient

    def _see_staff(self, clinic:Clinic, patient:Patient, appointment:Appointment):
        ConsoleUtility.print_conversation('Hi, I am {} {}'.format(appointment.staff.role, appointment.staff.name))
        self._pause()
        ConsoleUtility.print_conversation('Let\'s start the consultation...')
        for i in range(0,3):
            self._pause()
            ConsoleUtility.print_conversation('...')
        ConsoleUtility.print_light(appointment.staff.consultation(patient))
        self._pause()
        if self._can_issue_prescription(appointment.staff):
            ConsoleUtility.print_conversation('Do you need a prescription?')
            input = ConsoleUtility.prompt_user_for_input(options=['Y','N'])
            if input == 'Y':
                prescription = appointment.staff.issue_prescription()
                ConsoleUtility.print_conversation('Here\'s your prescription: {}'.format(prescription))
                clinic.register_prescription(patient, appointment.staff, prescription)
        ConsoleUtility.print_conversation('Take care.')
        clinic.appointment_schedule.cancel_appoitment(appointment)

    def _can_issue_prescription(self, staff:HealthcareProfessional) -> bool:
        return hasattr(staff, 'issue_prescription') and callable(getattr(staff, 'issue_prescription'))