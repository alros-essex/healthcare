from enum import Enum

class State(Enum):
    CONNECTED = 'CONNECTED'
    MANAGE_DOCTORS = 'MANAGE_DOCTORS'
    MANAGE_NURSES = 'MANAGE_NURSES'
    MANAGE_RECEPTIONISTS = 'MANAGE_RECEPTIONISTS'
    HIRE_A_DOCTOR = 'HIRE_A_DOCTOR'
    FIRE_A_DOCTOR = 'FIRE_A_DOCTOR'