from healthcare.receptionist import Receptionist
from healthcare.storage import Storage


from console.state import State

from .handle_state_fire_staff import StateFireStaff

class StateFireReceptionist(StateFireStaff):

    def __init__(self, storage:Storage):
        super().__init__(State.MANAGE_RECEPTIONISTS, Receptionist, storage)
