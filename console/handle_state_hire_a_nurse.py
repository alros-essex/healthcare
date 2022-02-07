from .handle_state_hire_staff import StateHireStaff

class StateHireNurse(StateHireStaff):

    def __init__(self, storage):
        from console.state import State
        super().__init__(State.MANAGE_NURSES, storage)
    
    def _get_instance(self, name:str, employee_number:str):
        from healthcare.nurse import Nurse
        return Nurse(name, employee_number)