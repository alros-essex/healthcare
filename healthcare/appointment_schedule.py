from collections import defaultdict
from datetime import date, datetime, timedelta

from healthcare import appointment
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

    def add_appoitment(self):
        """creates an appoitment
        
        Args:
            None
        Returns:
            Appointment: appointment just created
        """
        pass

    def cancel_appoitment(self):
        """deletes an appoitment
        
        Args:
            None
        Returns:
            Appointment: appoitment just deleted
        """
        pass

    def find_next_available(self, professional:HealthcareProfessional, urgent:bool, initial:datetime):
        starting = datetime(initial.year, initial.month, initial.day, initial.hour + (0 if initial.minute<30 else 1), 30 if initial.minute<30 else 0)
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

    def _get_appointments(self, professional:HealthcareProfessional):
        return self._appoitments[professional.employee_number]

    def _next_slot(self, urgent:bool, starting:datetime):
        slot = starting
        if not self._it_it_open(starting, urgent):
            slot = self._urgent_next_opening_time(slot) if urgent else self._non_urgent_next_opening_time(slot)
        return slot

    # TODO manage weekends

    def _it_it_open(self, time:datetime, urgent:bool):
        opening = datetime(time.year, time.month, time.day, 8 if urgent else 9)
        closing = datetime(time.year, time.month, time.day, 14 if urgent else 13)
        return opening > time and time > closing

    def _non_urgent_next_opening_time(self, starting:datetime):
        opening = starting.replace(hour=9, minute=0, second=0, microsecond=0)
        return opening if opening > starting else opening + timedelta(days=1)

    def _urgent_next_opening_time(self, starting:datetime):
        opening = starting.replace(hour=8, minute=0, second=0, microsecond=0)
        return opening if opening > starting else opening + timedelta(days=1)

