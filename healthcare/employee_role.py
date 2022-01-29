from enum import Enum

class EmployeeRole(Enum):
    RECEPTIONIST = 'Receptionist'
    DOCTOR = 'Doctor'
    NURSE = 'Nurse'

    def pretty_print(self):
        pass