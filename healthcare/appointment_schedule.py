from collections import defaultdict
from datetime import date, datetime, timedelta

from healthcare.appointment import Appointment
from healthcare.appointment_type import AppointmentType

class AppointmentSchedule():
    """
    Represents the schedule of the appointments
    """
    from .storage import Storage
    from .patient import Patient
    from .appointment import Appointment
    from .healthcare_professional import HealthcareProfessional

    def __init__(self, storage:Storage):
        """creates the instance
        
        Args:
            storage: db instance
        Returns:
            None
        """
        self._storage = storage

    @property
    def appointments(self):
        return self._storage.select_appointments()

    def add_appoitment(self, appointment:Appointment):
        """creates an appoitment
        
        Args:
            None
        Returns:
            None
        """
        self._storage.insert_appointment(appointment)

    def cancel_appoitment(self, appointment:Appointment):
        """deletes an appoitment
        
        Args:
            appointment: the appointment to delete
        Returns:
            None
        """
        self._storage.delete_appointment(appointment)

    def find_next_available(self, professional:HealthcareProfessional, patient:Patient, urgent:bool, initial:datetime):
        starting = self._round_initial_time(initial)
        appointments = self._appointments_as_dict(self.find_appoitment(filter_professional=professional))
        slot = self._find_next_slot(appointments, urgent, starting)
        return Appointment(type = AppointmentType.URGENT if urgent else AppointmentType.NORMAL,
            staff = professional, patient = patient, date = slot)

    def _round_initial_time(self, initial:datetime):
        if initial.minute != 0 and initial.minute != 30:
            return datetime(initial.year, initial.month, initial.day, initial.hour + (0 if initial.minute<=30 else 1), 30 if initial.minute<=30 else 0)
        else:
            return initial

    def _appointments_as_dict(self, appointments):
        indexed = {}
        for appointment in appointments:
            indexed[appointment.date] = appointment
        return indexed

    def _find_next_slot(self, appointments, urgent, starting:datetime) -> datetime:
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

    def find_appoitment(self, filter_professional:HealthcareProfessional=None, 
        filter_professionals=[], filter_date:date=None, filter_patient:Patient=None):
        """finds an appoitment
        
        Args:
            filter_professional: filter by healthcare professional (default None)
            filter_professionals: filter by list of healthcare professionals (default None)
            filter_date: filter by date
            filter_patient: filter by patient
        Returns:
            Appointment: dict of professional -> (dict of date -> appoitment)
        """
        employee_numbers_to_consider = [p.employee_number for p in self._merge_professional_filters(filter_professional, filter_professionals)] if filter_professional is not None or len(filter_professionals)>0 else None
        return self._storage.select_appointments(filter_patient=filter_patient, filter_employee_numbers=employee_numbers_to_consider, filter_date = filter_date)

    def find_dates_with_appointments(self):
        return self._storage.select_appointment_dates()

    def _merge_professional_filters(self, filter_professional:HealthcareProfessional, filter_professionals):
        filter = []
        if filter_professional is not None:
            filter.append(filter_professional)
        filter = filter + filter_professionals
        return filter
