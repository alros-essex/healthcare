from .handle_state_manage_staff import StateManageStaff

class StateManageDoctors(StateManageStaff):

    def __init__(self, storage):
        from healthcare.doctor import Doctor
        from console.state import State
        super().__init__(Doctor, State.HIRE_A_DOCTOR)
        self._storage = storage

    def _get_managed_staff(self):
        return self._storage.select_doctors()