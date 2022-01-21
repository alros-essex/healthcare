from healthcare.nurse import Nurse
from console.state import State

from .handle_state_fire_staff import StateFireStaff

class StateFireNurse(StateFireStaff):

    def __init__(self):
        super().__init__(State.MANAGE_NURSES, Nurse)
