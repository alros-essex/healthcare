from healthcare.storage import Storage
from healthcare.receptionist import Receptionist
from console.state import State

from .handle_state_manage_staff import StateManageStaff

class StateManageReceptionists(StateManageStaff):

    def __init__(self, storage:Storage):
        super().__init__(Receptionist, State.HIRE_A_RECEPTIONIST, State.FIRE_A_RECEPTIONIST)
        self._storage = storage

    def _get_managed_staff(self):
        return self._storage.select_receptionists()