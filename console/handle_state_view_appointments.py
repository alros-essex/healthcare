from datetime import datetime, date
import re
from healthcare.appointment_schedule import AppointmentSchedule
from healthcare.clinic import Clinic
from console.state import State

from .console_utility import ConsoleUtility
from .handle_state import StateHandler

class StateViewAppointmentsHandler(StateHandler):
    
    def __init__(self):
        self._next_state = {}
        self._next_state['B']=State.CONNECTED

    def handle(self, clinic:Clinic):
        self._print_status(clinic.appointment_schedule, clinic.doctors, clinic.nurses)
        self._print_options()
        return self._next_state[self._get_user_choice()]

    def _print_status(self, schedule:AppointmentSchedule, doctors, nurses):
        ConsoleUtility.print_light('Please enter a date in format dd-mm-yyyy')
        input = ConsoleUtility.prompt_user_for_input(validation=lambda i: re.search("^\d{2}-\d{2}-\d{4}$", i) is not None )
        appointment_calendars = schedule.find_appoitment(filter_professionals=doctors, filter_date=self._parse_date(input))
        for appointment_calendar in appointment_calendars:
            for appointment_date in sorted(list(appointment_calendar.keys())):
                ConsoleUtility.print_light('- {}'.format(appointment_calendar[appointment_date]))

    def _print_options(self):
        ConsoleUtility.print_option('[B]ack')
        
    def _get_user_choice(self):
        return ConsoleUtility.prompt_user_for_input(['B'])

    def _parse_date(self, input:str) -> datetime:
        """parses a date in yyyy-mm-dd format
        
        Args:
            input: date as a string
        Returns:
            datetime
        """
        el = re.split("-", input)
        return datetime(int(el[2]),int(el[1]),int(el[0]))