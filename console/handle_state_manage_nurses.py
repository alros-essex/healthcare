from .handle_state_manage_staff import StateManageStaff

class StateManageNurses(StateManageStaff):

    def __init__(self, storage):
        from healthcare.nurse import Nurse
        from console.state import State
        super().__init__(Nurse, State.HIRE_A_NURSE)
        self._storage = storage

    def _get_managed_staff(self):
        return self._storage.select_nurses()