from .handle_state_hire_staff import StateHireStaff

class StateHireDoctor(StateHireStaff):

    def __init__(self, storage):
        from .state import State
        super().__init__(State.MANAGE_DOCTORS, storage)
    
    def _get_instance(self, name:str, employee_number:str):
        from healthcare.doctor import Doctor
        return Doctor(name, employee_number)