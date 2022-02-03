from datetime import datetime
import enum
import time
import random
from healthcare.appointment import Appointment
from healthcare.appointment_schedule import AppointmentSchedule
from healthcare.doctor import Doctor
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
        user = None
        if receptionist is not None:
            loop = True
            while loop:
                user, loop = self._talk_with_receptionist(receptionist, user)
        return State.CONNECTED

    def _find_a_receptionist(self) -> Receptionist:
        """utility method to find the first receptionist available"""
        receptionists = self._storage.select_receptionists()
        if len(receptionists) == 0 or len(self._storage.select_doctors()) == 0:
            ConsoleUtility.print_light('<it looks like nobody works here (Clinic must hire at least one receptionist and one doctor)>')
            return None
        receptionist:Receptionist = receptionists[random.randint(0, len(receptionists)-1)]
        return receptionist

    def _talk_with_receptionist(self, receptionist:Receptionist, patient:Patient): 
        """workflow with the receptionist"""
        if patient is None:
            patient = self._front_desk_identity_user(receptionist)
        appointments = self._print_appointments(receptionist, patient)
        self._pause()
        ConsoleUtility.print_conversation('Receptionist> How can I help you?')
        ConsoleUtility.print_option('I want to [M]ake an appointment')
        if len(appointments) > 0:
            ConsoleUtility.print_option('I want to [G]o to my next appointment')
            ConsoleUtility.print_option('I want to [C]ancel appointment')
        ConsoleUtility.print_option('I [L]eave now, bye')
        input = ConsoleUtility.prompt_user_for_input(options=['M','G','C','L'])
        if input == 'M':
            self._make_an_appointment(receptionist, patient)
            return patient, True
        elif input == 'G':
            self._see_staff(receptionist, patient, appointments[0])
            return patient, True
        elif input == 'C':
            self._cancel_an_appointment(receptionist, patient=patient)
            return patient, True
        else:
            return patient, False
    
    def _front_desk_identity_user(self, receptionist:Receptionist) -> Patient:
        ConsoleUtility.print_conversation('Receptionist> Hello! Can I help you?')
        self._pause()
        ConsoleUtility.print_light('you> Hi, yes.')
        self._pause()
        ConsoleUtility.print_conversation('Receptionist> What\'s your name?')
        name = ConsoleUtility.prompt_user_for_input()
        patient = receptionist.lookup_patient(name)
        if patient is None:
            ConsoleUtility.print_conversation('Receptionist> You are not yet in the system, I need to register you as a patient')
            self._pause()
            patient = self._register_new_patient(receptionist, name = name)
        return patient

    def _print_appointments(self, receptionist:Receptionist, patient:Patient):
        appointments = receptionist.find_patient_appointments(patient)
        ConsoleUtility.print_conversation('Receptionist> Currently, you have {} appointment{}'.format(len(appointments),'s' if len(appointments)>1 else ''))
        for idx, appointment in enumerate(appointments):
            ConsoleUtility.print_light('{} with {}'.format(idx+1, appointment.date, appointment.staff))
        return appointments

    def _make_an_appointment(self, receptionist:Receptionist, patient:Patient):
        ConsoleUtility.print_conversation('Receptionist> With whom do you need an appointment?')
        index = 1
        options = []
        ConsoleUtility.print_option('[{}] Doctor {}'.format(index, patient.doctor.name))
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

    def _see_staff(self, receptionist:Receptionist, patient:Patient, appointment:Appointment):
        from healthcare.doctor import Doctor
        ConsoleUtility.print_conversation('{role}> Hi, I am {role} {name}'.format(
            role = appointment.staff.role.value, name = appointment.staff.name))
        self._pause()
        ConsoleUtility.print_conversation('{}> Let\'s start the consultation...'.format(appointment.staff.role.value))
        for i in range(0,3):
            self._pause()
            ConsoleUtility.print_conversation('{}> ...'.format(appointment.staff.role.value))
        ConsoleUtility.print_light(appointment.staff.consultation(patient))
        self._pause()
        if self._can_issue_prescription(appointment.staff) and len(patient.prescriptions)>0:
            ConsoleUtility.print_conversation('{}> Do you need a repeat?'.format(appointment.staff.role.value))
            input = ConsoleUtility.prompt_user_for_input(options=['Y','N'])
            if input == 'Y':
                doctor:Doctor = appointment.staff
                patient.request_repeat(doctor)
                ConsoleUtility.print_conversation('{role}> Here\'s your repeat')
                self._pause()
                ConsoleUtility.print_light('you> Thank you')
        ConsoleUtility.print_conversation('{}> Take care.'.format(appointment.staff.role.value))
        self._pause()
        ConsoleUtility.print_light('you> Bye')
        receptionist.cancel_appointment(appointment)

    def _can_issue_prescription(self, staff:HealthcareProfessional) -> bool:
        return hasattr(staff, 'issue_prescription') and callable(getattr(staff, 'issue_prescription'))

    def _register_new_patient(self, receptionist:Receptionist, name):
        patient = self._identify_user(name)
        doctor = self._choose_a_doctor(receptionist)
        receptionist.register_patient(patient, doctor)
        ConsoleUtility.print_conversation('Receptionist> Thank you, now you are one of our patients')
        return patient

    def _default_or_input(self, default):
        if default is None:
            return ConsoleUtility.prompt_user_for_input()
        else:
            ConsoleUtility.print_light(default)
            return default

    def _identify_user(self, name):
        ConsoleUtility.print_conversation('Receptionist> What is your address?')
        address = ConsoleUtility.prompt_user_for_input()
        ConsoleUtility.print_conversation('Receptionist> What is your phone number?')
        phone = ConsoleUtility.prompt_user_for_input()
        return Patient(name, address, phone)

    def _choose_a_doctor(self, receptionist:Receptionist):
        doctors = receptionist.find_available_doctors()
        ConsoleUtility.print_conversation('Receptionist> You should choose a doctor')
        options = []
        for index, doctor in enumerate(doctors):
            options.append(doctor)
            ConsoleUtility.print_option('[{}] Doctor {}'.format(index +1, doctor.name))
            index = index + 1
        doctor = options[int(ConsoleUtility.prompt_user_for_input(validation = lambda i: int(i)>0 and int(i)<=index)) - 1]
        return doctor

    def _cancel_an_appointment(self, receptionist:Receptionist, patient:Patient):
        appointments = self._print_appointments(receptionist, patient)
        ConsoleUtility.print_conversation('Receptionist> Which one do you want to cancel?')
        input = ConsoleUtility.prompt_user_for_input(options = [str(o) for o in range(1, len(appointments)+1)])
        appointment = appointments[int(input)-1]
        receptionist.cancel_appointment(appointment)
        ConsoleUtility.print_conversation('Receptionist> The appointment {} has been cancelled'.format(appointment))

    def _find_next_appointment(self, receptionist:Receptionist, patient:Patient):
        receptionist.find_patient_appointments(patient)

    def _pause(self):
        time.sleep(0.5 if self._quick else 1.5)
