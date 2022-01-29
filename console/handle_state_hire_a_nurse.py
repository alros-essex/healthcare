from healthcare.nurse import Nurse
from healthcare.storage import Storage
from console.state import State

from .handle_state_hire_staff import StateHireStaff

class StateHireNurse(StateHireStaff):

    def __init__(self, storage:Storage):
        super().__init__(State.MANAGE_NURSES, storage)
    
    def _get_instance(self, name:str, employee_number:str):
        return Nurse(name, employee_number)