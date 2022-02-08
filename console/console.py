from colorama import Fore, Back
from healthcare.appointment_schedule import AppointmentSchedule
from healthcare.storage import Storage
from .state import State
from .handle_state_as_patient_go import StateAsPatientGoHandler
from .handle_state_connected import StateConnectedHandler
from .handle_state_hire_a_doctor import StateHireDoctor
from .handle_state_manage_doctors import StateManageDoctors
from .handle_state_manage_employee import StateManageEmployee
from .handle_state_manage_patients import StateManagePatients
from .handle_state_hire_a_nurse import StateHireNurse
from .handle_state_manage_nurses import StateManageNurses
from .handle_state_hire_a_receptionist import StateHireReceptionist
from .handle_state_manage_receptionists import StateManageReceptionists
from .handle_state_view_appointments import StateViewAppointmentsHandler

LOG = '@log'

class Console():

    def __init__(self, storage:Storage, schedule:AppointmentSchedule, quick:bool=False):
        self._quick = quick
        self._handlers = {}
        self._handlers[State.CONNECTED] = StateConnectedHandler(storage)
        self._handlers[State.MANAGE_EMPLOYEES] = StateManageEmployee()
        self._handlers[State.MANAGE_DOCTORS] = StateManageDoctors(storage)
        self._handlers[State.HIRE_A_DOCTOR] = StateHireDoctor(storage)
        self._handlers[State.MANAGE_NURSES] = StateManageNurses(storage)
        self._handlers[State.HIRE_A_NURSE] = StateHireNurse(storage)
        self._handlers[State.MANAGE_RECEPTIONISTS] = StateManageReceptionists(storage)
        self._handlers[State.HIRE_A_RECEPTIONIST] = StateHireReceptionist(storage)
        self._handlers[State.MANAGE_PATIENTS] = StateManagePatients(storage)
        self._handlers[State.AS_A_PATIENT_GO] = StateAsPatientGoHandler(storage, schedule, quick=quick)
        self._handlers[State.VIEW_APPOINTMENTS] = StateViewAppointmentsHandler(storage, schedule)

    def loop(self):
        self._state = State.CONNECTED
        context = {}
        while self._state != State.QUIT:
            self._state = self._handlers[self._state].handle(context)
  

    def print_formatted(self, output):
        """
        Prints formatted lines

        Args:
            output: a (formatted) string or an array of (formatted) strings
        Returns:
            None
        """
        if isinstance(output, list):
            # it's a list: recursively process it
            for line in output:
                self.print_formatted(line)
            else:
                # print and extract keys
                self._print_formatted(output)

    def _print_formatted(self, line):
        """
        Prints formatted line

        Args:
            line: a (formatted) string
        Returns:
            None
        """
        if line.startswith(LOG):
            '[INFO] {color_fg}{color_bg}{line}{reset_bg}{reset_fg}'.format(line = line[len(LOG):],
                color_fg = Fore.GREEN, color_bg = Back.BLACK, reset_bg = Back.RESET, reset_fg = Fore.RESET)
        print(line)
