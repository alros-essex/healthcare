from collections import defaultdict
from datetime import date, datetime, time, timedelta

from healthcare.patient import Patient

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

    def cancel_appoitment(self, appointment:Appointment):
        """deletes an appoitment
        
        Args:
            appointment: the appointment to delete
        Returns:
            None
        """
        self._appoitments[appointment.staff.employee_number].pop(appointment.date)

    def find_appoitment(self, filter_professional:HealthcareProfessional=None, 
        filter_professionals=[], filter_date:date=None, filter_patient:Patient=None, flatten:bool = False):
        """finds an appoitment
        
        Args:
            filter_professional: filter by healthcare professional (default None)
            filter_professionals: filter by list of healthcare professionals (default None)
            filter_date: filter by date
            filter_patient: filter by patient
        Returns:
            Appointment: dict of professional -> (dict of date -> appoitment)
        """
        appointments = []
        if filter_professional is not None or len(filter_professionals)>0:
            employee_numbers_to_consider = [p.employee_number for p in self._merge_professional_filters(filter_professional, filter_professionals)]
        else:
            employee_numbers_to_consider = list(self._appoitments.keys())

        for employee_number in employee_numbers_to_consider:
            app = self._appoitments[employee_number]
            if filter_date is not None:
                app = self._filter_by_date(app, filter_date)
            if filter_patient is not None:
                app = self._filter_by_patient(app, filter_patient)
            appointments.append(app)
        return self._flatten(appointments) if flatten else appointments

    def _merge_professional_filters(self, filter_professional:HealthcareProfessional, filter_professionals):
        filter = []
        if filter_professional is not None:
            filter.append(filter_professional)
        filter = filter + filter_professionals
        return filter
        
    def _filter_by_date(self, professional_appointments, filter_date:date):
        return {k: v for k, v in professional_appointments.items() if v.is_on(filter_date)}

    def _filter_by_patient(self, professional_appointments, filter_patient:Patient):
        return {key:value for (key,value) in professional_appointments.items() if value.patient == filter_patient}

    def _flatten(self, appoitments):
        return [app for cal in appoitments for k,app in cal.items() if app is not None]