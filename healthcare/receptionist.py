from datetime import datetime, timedelta

from healthcare.appointment_schedule import AppointmentSchedule
from .appointment import Appointment
from .healthcare_professional import HealthcareProfessional
from .employee import Employee
from .patient import Patient


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

    def _next_slot(self, urgent:bool, starting:datetime):
        slot = starting + timedelta(minutes=30)
        if not self._is_it_open(starting, urgent):
            slot = self._urgent_next_opening_time(slot) if urgent else self._non_urgent_next_opening_time(slot)
        return slot

    # TODO manage weekends

    def _is_it_open(self, time:datetime, urgent:bool):
        opening = datetime(time.year, time.month, time.day, 8 if urgent else 9)
        closing = datetime(time.year, time.month, time.day, 14 if urgent else 13)
        return closing >= time and time >= opening

    def _non_urgent_next_opening_time(self, starting:datetime):
        opening = starting.replace(hour=9, minute=0, second=0, microsecond=0)
        return opening if opening > starting else opening + timedelta(days=1)

    def _urgent_next_opening_time(self, starting:datetime):
        opening = starting.replace(hour=8, minute=0, second=0, microsecond=0)
        return opening if opening > starting else opening + timedelta(days=1)