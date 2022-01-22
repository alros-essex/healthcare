from collections import defaultdict
from datetime import date, datetime, time, timedelta

from .appointment import Appointment
from .healthcare_professional import HealthcareProfessional
from healthcare import appointment


class AppointmentSchedule():
    """
    Represents the schedule of the appointments
    """
    def __init__(self):
        """creates the instance
        
        Args:
            None
        Returns:
            None
        """
        self._appoitments = defaultdict(lambda: defaultdict(lambda: None))

    @property
    def appointments(self):
        return self._appoitments

    def add_appoitment(self, appointment:Appointment):
        """creates an appoitment
        
        Args:
            None
        Returns:
            None
        """
        self._appoitments[appointment.staff.employee_number][appointment.date]=appointment

    def cancel_appoitment(self):
        """deletes an appoitment
        
        Args:
            None
        Returns:
            Appointment: appoitment just deleted
        """
        pass

    def find_appoitment(self, filter_professional=None, filter_professionals=[], filter_date:date=None):
        """finds an appoitment
        
        Args:
            filter_professional: filter by healthcare professional (default None)
            filter_professionals: filter by list of healthcare professionals (default None)
            filter_date: filter by date
        Returns:
            Appointment: dict of professional -> (dict of date -> appoitment)
        """
        appointments = []
        for p in self._merge_professional_filters(filter_professional, filter_professionals):
            appointments.append(self._appoitments[p.employee_number] if filter_date is None else self._filter_by_date(self._appoitments[p.employee_number], filter_date))
        return appointments

    def _merge_professional_filters(self, filter_professional, filter_professionals):
        filter = []
        if filter_professional is not None:
            filter.append(filter_professional)
        filter = filter + filter_professionals
        return filter
        
    def _filter_by_date(self, professional_appointments, filter_date:date):
        return {k: v for k, v in professional_appointments.items() if v.is_on(filter_date)}