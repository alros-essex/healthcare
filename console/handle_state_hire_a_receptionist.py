from .handle_state_hire_staff import StateHireStaff

class StateHireReceptionist(StateHireStaff):

    def __init__(self, storage):
        from console.state import State
        super().__init__(State.MANAGE_RECEPTIONISTS, storage)
    
    def _get_instance(self, name:str, employee_number:str):
        from healthcare.receptionist import Receptionist
        return Receptionist(name, employee_number)