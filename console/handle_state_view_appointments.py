from datetime import datetime, date
import re
from healthcare.appointment_schedule import AppointmentSchedule
from healthcare.storage import Storage
from console.state import State

from .console_utility import ConsoleUtility
from .handle_state import StateHandler

class StateViewAppointmentsHandler(StateHandler):
    
    def __init__(self, storage:Storage, schedule:AppointmentSchedule):
        self._storage = storage
        self._schedule = schedule
        self._next_state = {}
        self._next_state['S']=State.VIEW_APPOINTMENTS
        self._next_state['B']=State.CONNECTED

    def handle(self, context:dict):
        self._print_status()
        self._print_options()
        return self._next_state[self._get_user_choice()]

    def _print_status(self):
        dates = self._schedule.find_dates_with_appointments()
        ConsoleUtility.print_light('Currently there are appointments in {} day{}'.format(len(dates),'s' if len(dates)>1 else ''))
        for date in dates:
            ConsoleUtility.print_light(date)
        ConsoleUtility.print_light('Please enter a date in format dd-mm-yyyy')
        input = ConsoleUtility.prompt_user_for_input(validation=lambda i: re.search("^\d{2}-\d{2}-\d{4}$", i) is not None )
        appointment_calendars = self._schedule.find_appoitment(filter_date=self._parse_date(input))
        for appointment_calendar in appointment_calendars:
            ConsoleUtility.print_light('- {}'.format(appointment_calendar))

    def _print_options(self):
        ConsoleUtility.print_option('[S]earch again')
        ConsoleUtility.print_option('[B]ack')
        
    def _get_user_choice(self):
        return ConsoleUtility.prompt_user_for_input(['S', 'B'])

    def _parse_date(self, input:str) -> date:
        """parses a date in yyyy-mm-dd format
        
        Args:
            input: date as a string
        Returns:
            datetime
        """
        el = re.split("-", input)
        return date(int(el[2]),int(el[1]),int(el[0]))