from .receptionist import Receptionist
from .state import State
from .state_fire_staff import StateFireStaff

class StateFireReceptionist(StateFireStaff):

    def __init__(self):
        super().__init__(State.MANAGE_RECEPTIONISTS, Receptionist)
