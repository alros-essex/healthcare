from healthcare.doctor import Doctor
from console.state import State
from healthcare.storage import Storage

from .handle_state_fire_staff import StateFireStaff

class StateFireDoctor(StateFireStaff):

    def __init__(self, storage:Storage):
        super().__init__(State.MANAGE_DOCTORS, Doctor, storage)
