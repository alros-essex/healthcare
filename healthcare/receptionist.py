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

    def make_appointment(self,  staff:HealthcareProfessional, patient:Patient, time:datetime, urgent:bool):
        appointment_type = AppointmentType.URGENT if urgent else AppointmentType.NORMAL
        self._schedule.add_appoitment(Appointment(appointment_type, staff, patient, time))

    def cancel_appointment(self, appointment:Appointment):
        self._schedule.cancel_appoitment(appointment)

    def lookup_patient(self, first_name:str, surname:str) -> Patient:
        return self._storage.select_patient(first_name=first_name, surname=surname)

    def register_patient(self, patient:Patient):
        self._storage.insert_patient(patient)

    def find_next_free_timeslot(self, professional:HealthcareProfessional, urgent:bool, initial:datetime):
        starting = self._round_initial_time(initial)
        appointments = self._appointments_as_dict(self._schedule.find_appoitment(filter_professional=professional))
        return self._find_next_slot(appointments, urgent, starting)

    def _appointments_as_dict(self, appointments):
        indexed = {}
        for appointment in appointments:
            indexed[appointment.date] = appointment
        return indexed

    def find_patient_appointments(self, patient:Patient):
        return self._schedule.find_appoitment(filter_patient=patient)

    def _round_initial_time(self, initial:datetime):
        if initial.minute != 0 and initial.minute != 30:
            return datetime(initial.year, initial.month, initial.day, initial.hour + (0 if initial.minute<=30 else 1), 30 if initial.minute<=30 else 0)
        else:
            return initial

    def _find_next_slot(self, appointments, urgent, starting:datetime):
        time_slot = self._next_slot(urgent, starting)
        empty_slot = None
        while empty_slot is None:
            if time_slot in appointments:
                time_slot = self._next_slot(urgent, time_slot)
            else:
                empty_slot = time_slot
        return empty_slot

    def _next_slot(self, urgent:bool, starting:datetime) -> datetime:
        slot = starting + timedelta(minutes=30)
        if not self._is_it_open(starting, urgent):
            slot = self._urgent_next_opening_time(slot) if urgent else self._non_urgent_next_opening_time(slot)
        return slot

    # TODO manage weekends

    def _is_it_open(self, time:datetime, urgent:bool):
        opening = datetime(time.year, time.month, time.day, 8 if urgent else 9)
        closing = datetime(time.year, time.month, time.day, 14 if urgent else 13)
        return closing >= time and time >= opening and time.weekday()<5

    def _non_urgent_next_opening_time(self, starting:datetime):
        return self._next_opening_time(starting, 9)
        
    def _urgent_next_opening_time(self, starting:datetime):
        return self._next_opening_time(starting, 8)

    def _next_opening_time(self, starting:datetime, starts_at:int):
        # opening today
        opening = starting.replace(hour=starts_at, minute=0, second=0, microsecond=0)
        # if it's already open, next is tomorrow
        opening = opening if opening > starting else opening + timedelta(days=1)
        # if opening is on a Saturday or a Sunday, move to Monday
        # sorry... this clinic is closed in the weekends!
        return opening if opening.weekday()<5 else opening + timedelta(days=7-opening.weekday())