from healthcare.receptionist import Receptionist
from healthcare.storage import Storage
from console.state import State

from .handle_state_hire_staff import StateHireStaff

class StateHireReceptionist(StateHireStaff):

    def __init__(self, storage:Storage):
        super().__init__(State.MANAGE_RECEPTIONISTS, storage)
    
    def _get_instance(self, name:str, employee_number:str):
        return Receptionist(name, employee_number)