from datetime import date, datetime, timedelta

from .appointment import Appointment
from .appointment_type import AppointmentType

class AppointmentSchedule():
    """
    Represents the schedule of the appointments
    """

    _instance = None

    @classmethod
    def instance(cls):
        if cls._instance is None:
            from .storage import Storage
            cls._instance = AppointmentSchedule(Storage.instance())
        return cls._instance

    @classmethod
    def reset(cls):
        """to be called when storage is reset"""
        cls._instance = None

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
        """returns all the appointments
        
        Args:
            None
        Returns:
            array of Appointment
        """
        return self._storage.select_appointments()

    def add_appoitment(self, appointment:Appointment) -> None:
        """saves an appoitment
        
        Args:
            appointment: the Appointment that must be stored
        Returns:
            None
        """
        self._storage.insert_appointment(appointment)

    def cancel_appoitment(self, appointment:Appointment) -> None:
        """deletes an appoitment
        
        Args:
            appointment: the Appointment to delete
        Returns:
            None
        """
        self._storage.delete_appointment(appointment)

    def find_next_available(self, professional:HealthcareProfessional, patient:Patient, urgent:bool, initial:datetime) -> Appointment:
        """finds a potential appointment slot for the given professional and patient

        Args:
            professional: the HealthcareProfessional
            patient: the Patient in need
            urgent: if True, it will use also the urgent-only timeslots
            initial: first possible datetime 
        Returns:
            Appointment (not saved)
        """
        starting = self._round_initial_time(initial)
        appointments = self._appointments_as_dict(self.find_appointments(filter_professional=professional))
        slot = self._find_next_slot(appointments, urgent, starting)
        return Appointment(type = AppointmentType.URGENT if urgent else AppointmentType.NORMAL,
            staff = professional, patient = patient, date = slot)

    def _round_initial_time(self, initial:datetime) -> datetime:
        """rounds the datetime to xx:00 or xx:30
        
        Args:
            initial: datetime to be rounded
        Returns:
            rounded datetime
        """
        if initial.minute != 0 and initial.minute != 30:
            return datetime(initial.year, initial.month, initial.day, initial.hour + (0 if initial.minute<=30 else 1), 30 if initial.minute<=30 else 0)
        else:
            return initial

    def _appointments_as_dict(self, appointments):
        """convenience method to reindex an array of appointments
        
        Args:
            appointments: array of Appointment
        Returns:
            dict where the key is the Appoitment datetime
        """
        indexed = {}
        for appointment in appointments:
            indexed[appointment.date] = appointment
        return indexed

    def _find_next_slot(self, appointments, urgent, starting:datetime) -> datetime:
        """finds the next empty timeslot
        
        Args:
            appoitments: one professiona's appointments
            urgent: True to use the urgent-only timeslots
            starting: first possible datetime
        Returns:
            first possible datetime
        """
        time_slot = self._next_slot(urgent, starting)
        empty_slot = None
        while empty_slot is None:
            if time_slot in appointments:
                time_slot = self._next_slot(urgent, time_slot)
            else:
                empty_slot = time_slot
        return empty_slot

    def _next_slot(self, urgent:bool, starting:datetime) -> datetime:
        """finds the next slot of time

        Args:
            urgent: True to use the urgent-only timeslots
            starting: first possible datetime
        Returns:
            first possible datetime
        """
        slot = starting + timedelta(minutes=30)
        if not self._is_it_open(starting, urgent):
            slot = self._urgent_next_opening_time(slot) if urgent else self._non_urgent_next_opening_time(slot)
        return slot

    # TODO manage weekends

    def _is_it_open(self, time:datetime, urgent:bool) -> bool:
        """checks if the clinic is open

        Args:
            time: datetime to check
            urgent: True to enable urgent-only timeslots
        Returns:
            True, if the clinic is open for the requested urgency level
        """
        opening = datetime(time.year, time.month, time.day, 8 if urgent else 9)
        closing = datetime(time.year, time.month, time.day, 14 if urgent else 13)
        return closing >= time and time >= opening and time.weekday()<5

    def _non_urgent_next_opening_time(self, starting:datetime) -> datetime:
        """calculates the next opening for non-urgent appointments
        If the specified datetime is in the middle of the day, the next day's opening will be returned
        
        Args:
            starting: datetime to use as base in the calculation
        Returns:
            datetime corresponding to the next opening
        """
        return self._next_opening_time(starting, 9)
        
    def _urgent_next_opening_time(self, starting:datetime) -> datetime:
        """calculates the next opening for urgent appointments
        If the specified datetime is in the middle of the day, the next day's opening will be returned
        
        Args:
            starting: datetime to use as base in the calculation
        Returns:
            datetime corresponding to the next opening
        """
        return self._next_opening_time(starting, 8)

    def _next_opening_time(self, starting:datetime, starts_at:int) -> datetime:
        """helper method for _non_urgent_next_opening_time and _urgent_next_opening_time
        
        Args:
            starting: datetime to use as base in the calculation
            starts_at: opening time to use
        Returns:
            datetime corresponding to the next opening
        """
        # opening today
        opening = starting.replace(hour=starts_at, minute=0, second=0, microsecond=0)
        # if it's already open, next is tomorrow
        opening = opening if opening > starting else opening + timedelta(days=1)
        # if opening is on a Saturday or a Sunday, move to Monday
        # sorry... this clinic is closed in the weekends!
        return opening if opening.weekday()<5 else opening + timedelta(days=7-opening.weekday())

    def find_appointments(self, filter_professional:HealthcareProfessional=None, 
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
        employee_numbers_to_consider = [p.employee_number for p in self._merge_professional_filters(filter_professional, filter_professionals)] if filter_professional is not None or len(filter_professionals)>0 else []
        return self._storage.select_appointments(filter_patient=filter_patient, filter_employee_numbers=employee_numbers_to_consider, filter_date = filter_date)

    def find_dates_with_appointments(self):
        """returns all dates when there is at least one appointment
        
        Args:
            None
        Returns:
            array of strings
        """
        return self._storage.select_appointment_dates()

    def _merge_professional_filters(self, filter_professional:HealthcareProfessional, filter_professionals):
        """helper method to merge two search filters
        
        Args:
            filter_professional: single professional (can be None)
            filter_professionals: array of professionals (can be empty)
        Returns:
            arrays of professionals
        """
        filter = []
        if filter_professional is not None:
            filter.append(filter_professional)
        filter = filter + filter_professionals
        return filter
