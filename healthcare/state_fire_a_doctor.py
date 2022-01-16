from .doctor import Doctor
from .state import State
from .state_fire_staff import StateFireStaff

class StateFireDoctor(StateFireStaff):

    def __init__(self):
        super().__init__(State.MANAGE_DOCTORS, Doctor)
