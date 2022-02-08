from .handle_state import StateHandler

class StateManagePatients(StateHandler):
    
    _columns = 3

    def __init__(self, storage):
        from console.state import State
        self._storage = storage
        self._next_state = {}
        self._next_state['B']=State.CONNECTED

    def handle(self, context:dict):
        self._print_status()
        self._print_options()
        return self._next_state[self._get_user_choice()]

    def _print_status(self):
        from .console_utility import ConsoleUtility
        ConsoleUtility.print_light('PATIENTS')
        doctors = self._storage.select_doctors()
        for i, doctor in enumerate(doctors):
            self._print_status_for_doctor(doctor)
            if i < len(doctors)-1:
                ConsoleUtility.print_option('[ENTER] for more')
                ConsoleUtility.prompt_user_for_input()
        
    def _print_status_for_doctor(self, doctor):
        from .console_utility import ConsoleUtility
        ConsoleUtility.print_option('=== Doctor {}\'s patiens ==='.format(doctor.name))
        patients = self._storage.select_patients(doctor)
        for index, patient in enumerate(patients, 1):
            print(patient.name.ljust(30), end='')
            if index % self._columns == 0:
                print()
        if len(patients) % self._columns != 0:
            print('\n')

    def _print_options(self):
        from .console_utility import ConsoleUtility
        ConsoleUtility.print_option('[B]ack')

    def _get_user_choice(self):
        from .console_utility import ConsoleUtility
        return ConsoleUtility.prompt_user_for_input(['B'])
