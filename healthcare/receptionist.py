from datetime import date, datetime

from healthcare.appointment_schedule import AppointmentSchedule
from .appointment import Appointment
from .doctor import Doctor
from .healthcare_professional import HealthcareProfessional
from .employee import Employee
from .patient import Patient
from healthcare import appointment


class Receptionist(Employee):

    def __init__(self, name: str, employee_number: str):
        super().__init__(name, employee_number)

    def make_appointment(self, schedule:AppointmentSchedule, staff:HealthcareProfessional, patient:Patient, time:datetime, urgent:bool):
        # TODO implement types
        schedule.add_appoitment(Appointment('', staff, patient, time))

    def cancel_appointment(self):
        pass

    def lookup_patient(self, clinic, name:str, surname:str):
        return next(filter(lambda p: ', '.join([surname, name]) == p.name,clinic.patients), None)

    def register_patient(self, clinic, patient:Patient):
        clinic.register_patient(patient)

    def find_next_free_timeslot(self, schedule:AppointmentSchedule, doctor:Doctor, urgent:bool, starting:datetime):
        return schedule.find_next_available(doctor, urgent, starting)
