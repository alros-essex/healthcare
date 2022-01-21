from healthcare.nurse import Nurse
from healthcare.state import State

from .handle_state_hire_staff import StateHireStaff

class StateHireNurse(StateHireStaff):

    def __init__(self):
        super().__init__(State.MANAGE_NURSES)
    
    def _get_instance(self, name:str, employee_number:str):
        return Nurse(name, employee_number)