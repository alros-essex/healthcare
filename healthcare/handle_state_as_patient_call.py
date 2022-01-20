from datetime import datetime
from healthcare import appointment
from healthcare.patient import Patient

from .appointment import Appointment
from .clinic import Clinic
from .console_utility import ConsoleUtility
from .state import State
from .handle_state import StateHandler
from .receptionist import Receptionist

class StateAsPatientCallHandler(StateHandler):

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

    def _register_new_patient(self, clinic:Clinic, receptionist:Receptionist, name = None, surname = None):
        if surname is None:
            ConsoleUtility.print_conversation('Can I have your surname, please?')
            surname = ConsoleUtility.prompt_user_for_input()
        if name is None:
            ConsoleUtility.print_conversation('...and your first name?')
            name = ConsoleUtility.prompt_user_for_input()
        ConsoleUtility.print_conversation('What is your address?')
        address = ConsoleUtility.prompt_user_for_input()
        ConsoleUtility.print_conversation('What is your phone number?')
        # TODO validation
        phone = ConsoleUtility.prompt_user_for_input()
        patient = Patient(name, surname, address, phone)
        receptionist.register_patient(clinic, patient)
        ConsoleUtility.print_conversation('Thank you, now you are one of our patients')
        return patient

    def _make_an_appointment(self, clinic:Clinic, receptionist:Receptionist):
        ConsoleUtility.print_conversation('Can I have your surname, please?')
        surname = ConsoleUtility.prompt_user_for_input()
        ConsoleUtility.print_conversation('Can I have your first name, please?')
        name = ConsoleUtility.prompt_user_for_input()
        patient = receptionist.lookup_patient(clinic, name, surname)
        if patient == None:
            ConsoleUtility.print_conversation('You are not yet in the system, I need to register you as a patient')
            patient = self._register_new_patient(clinic, receptionist, name, surname)
        ConsoleUtility.print_conversation('With whom do you need an appointment?')
        index = 0
        options = []
        for doctor in clinic.doctors:
            options.append(doctor)
            ConsoleUtility.print_option('[{}] Doctor {}'.format(index +1, doctor.name))
            index = index + 1
        for nurse in clinic.nurses:
            options.append(nurse)
            ConsoleUtility.print_option('[{}] Nurse {}'.format(index + 1, nurse.name))
            index = index + 1
        staff = options[int(ConsoleUtility.prompt_user_for_input(validation = lambda i: int(i)>0 and int(i)<=index)) - 1]
        ConsoleUtility.print_conversation('Is it urgent?')
        ConsoleUtility.print_option('[Y]es')
        ConsoleUtility.print_option('[N]o')
        urgent = ConsoleUtility.prompt_user_for_input(['Y', 'N']) == 'Y'
        accepted = False
        next_timeslot = datetime.now()
        while not accepted:
            next_timeslot = receptionist.find_next_free_timeslot(clinic.appointment_schedule, staff, urgent, next_timeslot)
            ConsoleUtility.print_conversation('{} would be ok for you?'.format(next_timeslot))
            ConsoleUtility.print_option('[Y]es')
            ConsoleUtility.print_option('[N]o')
            accepted = ConsoleUtility.prompt_user_for_input(['Y', 'N']) == 'Y'
        receptionist.make_appointment(clinic.appointment_schedule, staff, patient, next_timeslot, urgent)
        ConsoleUtility.print_conversation('Thank you, the appointment has been registered')

    def _cancel_an_appointment(self, receptionist:Receptionist):
        pass

    def _find_next_appointment(self, receptionist:Receptionist):
        pass