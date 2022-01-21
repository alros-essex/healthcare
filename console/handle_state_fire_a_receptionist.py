from healthcare.receptionist import Receptionist
from console.state import State

from .handle_state_fire_staff import StateFireStaff

class StateFireReceptionist(StateFireStaff):

    def __init__(self):
        super().__init__(State.MANAGE_RECEPTIONISTS, Receptionist)
