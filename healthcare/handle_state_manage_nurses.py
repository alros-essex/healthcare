from .clinic import Clinic
from .nurse import Nurse
from .state import State
from .handle_state_manage_staff import StateManageStaff

class StateManageNurses(StateManageStaff):

    def __init__(self):
        super().__init__(Nurse, State.HIRE_A_NURSE, State.FIRE_A_NURSE)

    def _get_managed_staff(self, clinic:Clinic):
        return clinic.nurses