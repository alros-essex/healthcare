from collections import defaultdict
from datetime import date, datetime, time, timedelta

from .appointment import Appointment
from .healthcare_professional import HealthcareProfessional


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

    def find_appoitment(self, professional:HealthcareProfessional):
        """finds an appoitment
        
        Args:
            professional: the healthcare professional
        Returns:
            Appointment: the found appointment
        """
        return self._appoitments[professional.employee_number]

    def get_by_date(self, date:date):
        all_appointments = []
        professionals = self.appoitments.keys()
        for professional in professionals:
            appointments = self.appointments[professional.employee_number]
            all_appointments.append([appointment for appointment in appointments if appointment.is_on(date)])
        return sorted(all_appointments, key=date)

