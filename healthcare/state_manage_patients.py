from abc import ABC, abstractmethod
from .clinic import Clinic
from .console_utility import ConsoleUtility
from .state import State
from .state_handler import StateHandler

class StateManagePatients(StateHandler):
    
    def __init__(self):
        self._next_state = {}
        self._next_state['B']=State.CONNECTED

    def handle(self, clinic:Clinic):
        self._print_status(clinic)
        self._print_options()
        return self._next_state[self._get_user_choice()]

    def _print_status(self, clinic:Clinic):
        ConsoleUtility.print_light('PATIENTS')
        columns = 3
        page = 15 * columns
        for index, patient in enumerate(clinic.patients, 1):
            print(patient.name.ljust(30), end='')
            if index % columns == 0:
                print()
            if index % page ==0 and index >- page:
                ConsoleUtility.print_option('[ENTER] for more')
                ConsoleUtility.prompt_user_for_input()
        if len(clinic.patients) % columns != 0:
            print('\n')

    def _print_options(self):
        ConsoleUtility.print_option('[B]ack')

    def _get_user_choice(self):
        return ConsoleUtility.prompt_user_for_input(['B'])
