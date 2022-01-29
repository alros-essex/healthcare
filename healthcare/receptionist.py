from datetime import datetime, timedelta

from .appointment_schedule import AppointmentSchedule
from .appointment_type import AppointmentType
from .appointment import Appointment
from .healthcare_professional import HealthcareProfessional
from .storage import Storage
from .employee import Employee
from .employee_role import EmployeeRole
from .patient import Patient


class Receptionist(Employee):

    def __init__(self, name: str, employee_number: str, schedule:AppointmentSchedule = None, storage:Storage = None):
        super().__init__(name, employee_number)
        self._schedule = schedule
        self._storage = storage

    @property
    def role(self) -> EmployeeRole:
        return EmployeeRole.RECEPTIONIST

    # TODO try to remove it
    def connect_to_schedule(self, schedule:AppointmentSchedule) -> None:
        self._schedule = schedule
    
    # TODO try to remove it
    def connect_to_storage(self, storage:Storage) -> None:
        self._storage = storage

    def register_appointment(self,  appointment:Appointment):
        self._schedule.add_appoitment(appointment)

    def cancel_appointment(self, appointment:Appointment):
        self._schedule.cancel_appoitment(appointment)

    def lookup_patient(self, first_name:str, surname:str) -> Patient:
        return self._storage.select_patient(first_name=first_name, surname=surname)

    def register_patient(self, patient:Patient):
        self._storage.insert_patient(patient)

    def find_patient_appointments(self, patient:Patient):
        return self._schedule.find_appoitment(filter_patient=patient)

    def propose_appointment(self, professional:HealthcareProfessional, patient:Patient, urgent:bool, initial:datetime) -> Appointment:
        return self._schedule.find_next_available(professional, patient, urgent, initial)