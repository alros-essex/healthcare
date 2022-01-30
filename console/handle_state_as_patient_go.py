from datetime import datetime
import enum
import time
import random
from healthcare.appointment import Appointment
from healthcare.appointment_schedule import AppointmentSchedule
from healthcare.healthcare_professional import HealthcareProfessional

from healthcare.storage import Storage
from healthcare.patient import Patient
from console.state import State
from healthcare.receptionist import Receptionist

from .console_utility import ConsoleUtility
from .handle_state import StateHandler

class StateAsPatientGoHandler(StateHandler):

    def __init__(self, storage:Storage, schedule:AppointmentSchedule, quick: bool = False):
        self._quick=quick
        self._storage = storage
        self._schedule = schedule

    def handle(self, context:dict):
        receptionist = self._find_a_receptionist()
        justId = False
        if receptionist is not None:
            loop = True
            while loop:
                user, loop = self._talk_with_receptionist(receptionist, context, justId)
                context['user'] = user
                justId = True
        return State.CONNECTED

    def _find_a_receptionist(self):
        receptionists = self._storage.select_receptionists()
        if len(receptionists) == 0:
            ConsoleUtility.print_light('<it looks like nobody works here (Clinic must hire at least one receptionist)>')
            return None
        receptionist:Receptionist = receptionists[random.randint(0, len(receptionists)-1)]
        receptionist.connect_to_schedule(self._schedule)
        receptionist.connect_to_storage(self._storage)
        return receptionist

    def _talk_with_receptionist(self, receptionist:Receptionist, context, justId:bool):
        user:Patient = context.get('user')
        if not justId:
            patient = self._front_desk_identity_user(receptionist, user)
        else:
            patient = user
        appointments = self._print_appointments(receptionist, patient)
        context['appointment'] = appointments
        self._pause()
        ConsoleUtility.print_conversation('Receptionist> How can I help you{}?'.format(' now' if justId else ''))
        ConsoleUtility.print_option('[M]ake an appointment')
        if len(appointments) > 0:
            ConsoleUtility.print_option('[S]ee a professional (next appointment)')
            ConsoleUtility.print_option('[C]ancel appointment')
        ConsoleUtility.print_option('[G]o away')
        input = ConsoleUtility.prompt_user_for_input(options=['M','S','C','G'])
        if input == 'M':
            self._make_an_appointment(receptionist, user=patient)
            return patient, True
        elif input == 'S':
            self._see_staff(receptionist, patient, appointments[0])
            return patient, True
        elif input == 'C':
            self._cancel_an_appointment(receptionist, patient=patient)
            return patient, True
        else:
            return patient, False

    def _front_desk_identity_user(self, receptionist:Receptionist, user:Patient) -> Patient:
        if user is not None:
            # handle configuration
            ConsoleUtility.print_conversation('Receptionist> Can I help you?')
            self._pause()
            ConsoleUtility.print_light('you> My name is {}'.format(user))
            self._pause()
            name = user.firstname
            surname = user.surname
        else:
            ConsoleUtility.print_conversation('Receptionist> Hello. Can I help you?')
            self._pause()
            ConsoleUtility.print_light('you> Hi, yes.')
            self._pause()
            ConsoleUtility.print_conversation('Receptionist> What\'s your name?')
            name = ConsoleUtility.prompt_user_for_input()
        patient = receptionist.lookup_patient(name)
        if patient is None:
            ConsoleUtility.print_conversation('Receptionist> You are not yet in the system, I need to register you as a patient')
            self._pause()
            patient = self._register_new_patient(receptionist, name = name, patient=user)
        return patient

    def _see_staff(self, receptionist:Receptionist, patient:Patient, appointment:Appointment):
        ConsoleUtility.print_conversation('{role}> Hi, I am {role} {name}'.format(
            role = appointment.staff.role.value, name = appointment.staff.name))
        self._pause()
        ConsoleUtility.print_conversation('{}> Let\'s start the consultation...'.format(appointment.staff.role.value))
        for i in range(0,3):
            self._pause()
            ConsoleUtility.print_conversation('{}> ...'.format(appointment.staff.role.value))
        ConsoleUtility.print_light(appointment.staff.consultation(patient))
        self._pause()
        if self._can_issue_prescription(appointment.staff):
            ConsoleUtility.print_conversation('{}> Do you need a prescription?'.format(appointment.staff.role.value))
            input = ConsoleUtility.prompt_user_for_input(options=['Y','N'])
            if input == 'Y':
                prescription = appointment.staff.issue_prescription(patient)
                ConsoleUtility.print_conversation('{role}> Here\'s your prescription: {prescription}'.format(
                    role = appointment.staff.role.value, prescription = prescription))
                self._pause()
                ConsoleUtility.print_light('you> Thank you')
        ConsoleUtility.print_conversation('{}> Take care.'.format(appointment.staff.role.value))
        self._pause()
        ConsoleUtility.print_light('you> Bye')
        receptionist.cancel_appointment(appointment)

    def _can_issue_prescription(self, staff:HealthcareProfessional) -> bool:
        return hasattr(staff, 'issue_prescription') and callable(getattr(staff, 'issue_prescription'))

    def _register_new_patient(self, receptionist:Receptionist, name = None, patient:Patient=None):
        if patient is None:
            patient = self._identify_user(name)
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

    def _identify_user(self, name=None):
        if name is None:
            ConsoleUtility.print_conversation('Receptionist> Can I have your name, please?')
            name = ConsoleUtility.prompt_user_for_input()
        ConsoleUtility.print_conversation('Receptionist> What is your address?')
        address = ConsoleUtility.prompt_user_for_input()
        ConsoleUtility.print_conversation('Receptionist> What is your phone number?')
        # TODO validation
        phone = ConsoleUtility.prompt_user_for_input()
        return Patient(name, address, phone)

    def _make_an_appointment(self, receptionist:Receptionist, user:Patient, name = None):
        if user is None:
            if name is None:
                ConsoleUtility.print_conversation('Receptionist> Can I have your name, please?')
                name = ConsoleUtility.prompt_user_for_input()
        else:
            # handle prefilled configuration
            name = user.name
        ConsoleUtility.print_conversation('Receptionist> Let me check in the system.')
        self._pause()
        patient = receptionist.lookup_patient(name)
        if patient == None:
            ConsoleUtility.print_conversation('Receptionist> You are not yet in the system, I need to register you as a patient')
            patient = self._register_new_patient(receptionist, name)
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
