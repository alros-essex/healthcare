from .clinic import Clinic
from .state import State
from .state_manage_staff import StateManageStaff

class StateManageDoctors(StateManageStaff):

    def __init__(self):
        super().__init__('doctor', State.HIRE_A_DOCTOR, State.FIRE_A_DOCTOR)

    def _get_managed_staff(self, clinic:Clinic):
        return clinic.doctors