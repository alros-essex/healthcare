from datetime import datetime
from .appointment_schedule import AppointmentSchedule
from .clinic import Clinic
from .console_utility import ConsoleUtility
from .state import State
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
        appointments = schedule.get_by_date(datetime.date(2022, 1, 20))

    def _print_options(self):
        ConsoleUtility.print_option('[B]ack')
        
    def _get_user_choice(self):
        return ConsoleUtility.prompt_user_for_input(['B'])