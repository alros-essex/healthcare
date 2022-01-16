from .nurse import Nurse
from .state import State
from .handle_state_fire_staff import StateFireStaff

class StateFireNurse(StateFireStaff):

    def __init__(self):
        super().__init__(State.MANAGE_NURSES, Nurse)
