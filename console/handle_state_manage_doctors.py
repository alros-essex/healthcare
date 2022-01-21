from healthcare.clinic import Clinic
from healthcare.doctor import Doctor
from healthcare.state import State

from .handle_state_manage_staff import StateManageStaff

class StateManageDoctors(StateManageStaff):

    def __init__(self):
        super().__init__(Doctor, State.HIRE_A_DOCTOR, State.FIRE_A_DOCTOR)

    def _get_managed_staff(self, clinic:Clinic):
        return clinic.doctors