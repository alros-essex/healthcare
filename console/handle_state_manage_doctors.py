from healthcare.storage import Storage
from healthcare.doctor import Doctor
from console.state import State

from .handle_state_manage_staff import StateManageStaff

class StateManageDoctors(StateManageStaff):

    def __init__(self, storage:Storage):
        super().__init__(Doctor, State.HIRE_A_DOCTOR)
        self._storage = storage

    def _get_managed_staff(self):
        return self._storage.select_doctors()