from colorama import Fore, Back, Style
from .clinic import Clinic
from .state import State
from .state_connected_handler import StateConnectedHandler

LOG = '@log'

class Console():

    def __init__(self):
        self._clinic = Clinic()
        self._state = State.CONNECTED
        self._handlers = {}
        self._handlers[State.CONNECTED] = StateConnectedHandler()

    def loop(self):
        while True:
            self._handlers[self._state].handle(self._clinic)
  

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

CONSOLE = Console()