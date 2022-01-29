from healthcare.nurse import Nurse
from healthcare.storage import Storage
from console.state import State

from .handle_state_fire_staff import StateFireStaff

class StateFireNurse(StateFireStaff):

    def __init__(self, storage:Storage):
        super().__init__(State.MANAGE_NURSES, Nurse, storage)
