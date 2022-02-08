from enum import Enum

class AppointmentType(Enum):
    """models the two types of appointment"""
    NORMAL = 'NORMAL'
    URGENT = 'URGENT'