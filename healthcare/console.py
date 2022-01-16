from colorama import Fore, Back, Style
from .clinic import Clinic
from .state import State
from .state_connected_handler import StateConnectedHandler
from .state_hire_a_doctor import StateHireDoctor
from .state_fire_a_doctor import StateFireDoctor
from .state_manage_doctors import StateManageDoctors
from .state_hire_a_nurse import StateHireNurse
from .state_fire_a_nurse import StateFireNurse
from .state_manage_nurses import StateManageNurses
from .state_hire_a_receptionist import StateHireReceptionist
from .state_fire_a_receptionist import StateFireReceptionist
from .state_manage_receptionists import StateManageReceptionists


LOG = '@log'

class Console():

    def __init__(self):
        self._handlers = {}
        self._handlers[State.CONNECTED] = StateConnectedHandler()
        self._handlers[State.MANAGE_DOCTORS] = StateManageDoctors()
        self._handlers[State.HIRE_A_DOCTOR] = StateHireDoctor()
        self._handlers[State.FIRE_A_DOCTOR] = StateFireDoctor()
        self._handlers[State.MANAGE_NURSES] = StateManageNurses()
        self._handlers[State.HIRE_A_NURSE] = StateHireNurse()
        self._handlers[State.FIRE_A_NURSE] = StateFireNurse()
        self._handlers[State.MANAGE_RECEPTIONISTS] = StateManageReceptionists()
        self._handlers[State.HIRE_A_RECEPTIONIST] = StateHireReceptionist()
        self._handlers[State.FIRE_A_RECEPTIONIST] = StateFireReceptionist()

    def loop(self, clinic:Clinic):
        self._state = State.CONNECTED
        while True:
            self._state = self._handlers[self._state].handle(clinic)
  

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
