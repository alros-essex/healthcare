from .clinic import Clinic
from .receptionist import Receptionist
from .state import State
from .handle_state_manage_staff import StateManageStaff

class StateManageReceptionists(StateManageStaff):

    def __init__(self):
        super().__init__(Receptionist, State.HIRE_A_RECEPTIONIST, State.FIRE_A_RECEPTIONIST)

    def _get_managed_staff(self, clinic:Clinic):
        return clinic.receptionists