from .receptionist import Receptionist
from .state import State
from .handle_state_hire_staff import StateHireStaff

class StateHireReceptionist(StateHireStaff):

    def __init__(self):
        super().__init__(State.MANAGE_RECEPTIONISTS)
    
    def _get_instance(self, name:str, employee_number:str):
        return Receptionist(name, employee_number)