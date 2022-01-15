from .doctor import Doctor
from .state import State
from .state_hire_staff import StateHireStaff

class StateHireDoctor(StateHireStaff):

    def __init__(self):
        super().__init__(State.MANAGE_DOCTORS)
    
    def _get_instance(self, name:str, employee_number:str):
        return Doctor(name, employee_number)