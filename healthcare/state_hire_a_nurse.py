from .nurse import Nurse
from .state import State
from .state_hire_staff import StateHireStaff

class StateHireNurse(StateHireStaff):

    def __init__(self):
        super().__init__(State.MANAGE_NURSES)
    
    def _get_instance(self, name:str, employee_number:str):
        return Nurse(name, employee_number)