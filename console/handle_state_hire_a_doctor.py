from healthcare.doctor import Doctor
from console.state import State
from healthcare.storage import Storage

from .handle_state_hire_staff import StateHireStaff

class StateHireDoctor(StateHireStaff):

    def __init__(self, storage:Storage):
        super().__init__(State.MANAGE_DOCTORS, storage)
    
    def _get_instance(self, name:str, employee_number:str):
        return Doctor(name, employee_number)