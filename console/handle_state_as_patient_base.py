from abc import ABC
from datetime import datetime
import time
from healthcare.storage import Storage

from healthcare.patient import Patient
from console.state import State
from healthcare.receptionist import Receptionist

from .console_utility import ConsoleUtility
from .handle_state import StateHandler

class StateAsPatientBaseHandler(StateHandler, ABC):

    def __init__(self, storage:Storage, quick:bool=False):
        self._quick = quick
        self._storage = storage

    def _register_new_patient(self, receptionist:Receptionist, name = None, surname = None, patient:Patient=None):
        if patient is None:
            patient = self._identify_user(name, surname)
        else:
            # handle prefilled configuration
            ConsoleUtility.print_conversation('Receptionist> Do you have an id?') 
            self._pause()
            ConsoleUtility.print_light('you> Here it is!')
            self._pause()
            ConsoleUtility.print_conversation('Receptionist> I see... {}'.format(patient))
            self._pause()
        receptionist.register_patient(patient)
        ConsoleUtility.print_conversation('Receptionist> Thank you, now you are one of our patients')
        return patient

    def _default_or_input(self, default):
        if default is None:
            return ConsoleUtility.prompt_user_for_input()
        else:
            ConsoleUtility.print_light(default)
            return default

    def _identify_user(self, name=None, surname=None):
        if surname is None:
            ConsoleUtility.print_conversation('Receptionist> Can I have your surname, please?')
            surname = ConsoleUtility.prompt_user_for_input()
        if name is None :
            ConsoleUtility.print_conversation('Receptionist> ...and your first name?')
            name = ConsoleUtility.prompt_user_for_input()
        ConsoleUtility.print_conversation('Receptionist> What is your address?')
        address = ConsoleUtility.prompt_user_for_input()
        ConsoleUtility.print_conversation('Receptionist> What is your phone number?')
        # TODO validation
        phone = ConsoleUtility.prompt_user_for_input()
        return Patient(name, surname, address, phone)

    def _make_an_appointment(self, receptionist:Receptionist, user:Patient, surname = None, name = None):
        if user is None:
            if surname is None:
                ConsoleUtility.print_conversation('Receptionist> Can I have your surname, please?')
                surname = ConsoleUtility.prompt_user_for_input()
            if name is None:
                ConsoleUtility.print_conversation('Receptionist> Can I have your first name, please?')
                name = ConsoleUtility.prompt_user_for_input()
        else:
            # handle prefilled configuration
            name = user.firstname
            surname = user.surname
        ConsoleUtility.print_conversation('Receptionist> Let me check in the system.')
        self._pause()
        patient = receptionist.lookup_patient(name, surname)
        if patient == None:
            ConsoleUtility.print_conversation('Receptionist> You are not yet in the system, I need to register you as a patient')
            patient = self._register_new_patient(receptionist, name, surname)
        ConsoleUtility.print_conversation('Receptionist> With whom do you need an appointment?')
        index = 0
        options = []
        for doctor in self._storage.select_doctors():
            options.append(doctor)
            ConsoleUtility.print_option('[{}] Doctor {}'.format(index +1, doctor.name))
            index = index + 1
        for nurse in self._storage.select_nurses():
            options.append(nurse)
            ConsoleUtility.print_option('[{}] Nurse {}'.format(index + 1, nurse.name))
            index = index + 1
        staff = options[int(ConsoleUtility.prompt_user_for_input(validation = lambda i: int(i)>0 and int(i)<=index)) - 1]
        ConsoleUtility.print_conversation('Receptionist> Is it urgent?')
        ConsoleUtility.print_option('[Y]es')
        ConsoleUtility.print_option('[N]o')
        urgent = ConsoleUtility.prompt_user_for_input(['Y', 'N']) == 'Y'
        accepted = False
        next_timeslot = datetime.now()
        while not accepted:
            possible_appointment = receptionist.propose_appointment(staff, patient, urgent, next_timeslot)
            ConsoleUtility.print_conversation('Receptionist> {} would be ok for you?'.format(possible_appointment.date))
            ConsoleUtility.print_option('[Y]es')
            ConsoleUtility.print_option('[N]o')
            accepted = ConsoleUtility.prompt_user_for_input(['Y', 'N']) == 'Y'
            next_timeslot = possible_appointment.date
        receptionist.register_appointment(possible_appointment)
        ConsoleUtility.print_conversation('Receptionist> Thank you, the appointment has been registered')

    def _cancel_an_appointment(self, receptionist:Receptionist, patient:Patient):
        appointments = self._print_appointments(receptionist, patient)
        ConsoleUtility.print_conversation('Receptionist> Which one do you want to cancel?')
        input = ConsoleUtility.prompt_user_for_input(options = [str(o) for o in range(1, len(appointments)+1)])
        appointment = appointments[int(input)-1]
        receptionist.cancel_appointment(appointment)
        ConsoleUtility.print_conversation('Receptionist> The appointment {} has been cancelled'.format(appointment))

    def _find_next_appointment(self, receptionist:Receptionist, patient:Patient):
        receptionist.find_patient_appointments(patient)

    def _print_appointments(self, receptionist:Receptionist, patient:Patient):
        appointments = receptionist.find_patient_appointments(patient)
        ConsoleUtility.print_conversation('Receptionist> Currently, you have {} appointment{}'.format(len(appointments),'s' if len(appointments)>1 else ''))
        for idx, appointment in enumerate(appointments):
            ConsoleUtility.print_light('{} with {}'.format(idx+1, appointment.date, appointment.staff))
        return appointments

    def _pause(self):
        time.sleep(0.5 if self._quick else 1.5)
