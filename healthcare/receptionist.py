from datetime import datetime, timedelta
from healthcare import appointment_type

from .appointment_schedule import AppointmentSchedule
from .appointment_type import AppointmentType
from .appointment import Appointment
from .healthcare_professional import HealthcareProfessional
from .employee import Employee
from .employee_role import EmployeeRole
from .patient import Patient


class Receptionist(Employee):

    def __init__(self, name: str, employee_number: str):
        super().__init__(name, employee_number)

    @property
    def role(self):
        return EmployeeRole.RECEPTIONIST

    def make_appointment(self, schedule:AppointmentSchedule, staff:HealthcareProfessional, patient:Patient, time:datetime, urgent:bool):
        appointment_type = AppointmentType.URGENT if urgent else AppointmentType.NORMAL
        schedule.add_appoitment(Appointment(appointment_type, staff, patient, time))

    def cancel_appointment(self, schedule:AppointmentSchedule, appointment:Appointment):
        schedule.cancel_appoitment(appointment)

    def lookup_patient(self, clinic, name:str, surname:str):
        return next(filter(lambda p: ', '.join([surname, name]) == p.name,clinic.patients), None)

    def register_patient(self, clinic, patient:Patient):
        clinic.register_patient(patient)

    def find_next_free_timeslot(self, schedule:AppointmentSchedule, professional:HealthcareProfessional, urgent:bool, initial:datetime):
        starting = self._round_initial_time(initial)
        appointments = schedule.find_appoitment(filter_professional=professional)[0] #being just one professional I have only 1 result
        return self._find_next_slot(appointments, urgent, starting)

    def find_patient_appointments(self, schedule:AppointmentSchedule, patient:Patient):
        return schedule.find_appoitment(filter_patient=patient, flatten=True)

    def _round_initial_time(self, initial:datetime):
        if initial.minute != 0 and initial.minute != 30:
            return datetime(initial.year, initial.month, initial.day, initial.hour + (0 if initial.minute<=30 else 1), 30 if initial.minute<=30 else 0)
        else:
            return initial

    def _find_next_slot(self, appointments, urgent, starting:datetime):
        time_slot = self._next_slot(urgent, starting)
        empty_slot = None
        while empty_slot is None:
            if appointments[time_slot] is None:
                empty_slot = time_slot
            else:
                time_slot = self._next_slot(urgent, time_slot)
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