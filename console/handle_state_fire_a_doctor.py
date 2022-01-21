from healthcare.doctor import Doctor
from console.state import State

from .handle_state_fire_staff import StateFireStaff

class StateFireDoctor(StateFireStaff):

    def __init__(self):
        super().__init__(State.MANAGE_DOCTORS, Doctor)
