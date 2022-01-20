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

    def find_next_available(self, professional:HealthcareProfessional, urgent:bool, initial:datetime):
        if initial.minute != 0 and initial.minute != 30:
            starting = datetime(initial.year, initial.month, initial.day, initial.hour + (0 if initial.minute<=30 else 1), 0 if initial.minute<=30 else 30)
        else:
            starting = initial
        appointments = self._get_appointments(professional)
        time_slot = self._next_slot(urgent, starting)
        empty_slot = None
        while empty_slot is None:
            if appointments[time_slot] is None:
                empty_slot = time_slot
            else:
                time_slot = self._next_slot(urgent, time_slot)
        return empty_slot


    def find_appoitment(self):
        """finds an appoitment
        
        Args:
            None
        Returns:
            Appointment: the found appointment
        """
        pass

    def get_by_date(self, date:date):
        all_appointments = []
        professionals = self.appoitments.keys()
        for professional in professionals:
            appointments = self.appointments[professional.employee_number]
            all_appointments.append([appointment for appointment in appointments if appointment.is_on(date)])
        return sorted(all_appointments, key=date)

    def _get_appointments(self, professional:HealthcareProfessional):
        return self._appoitments[professional.employee_number]

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

