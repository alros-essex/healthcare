from healthcare.storage import Storage
from .init_hiring_staff import InitHiringStaff

from healthcare.receptionist import Receptionist
from healthcare.appointment_schedule import AppointmentSchedule

class InitReceptionists(InitHiringStaff):
    def _get_type_of_staff(self):
        return 'receptionists'

    def _get_candidates_to_hire(self, storage:Storage, schedule:AppointmentSchedule):
        return [
            Receptionist('Pam Beesly', 'RC001', storage = storage, schedule=schedule),
            Receptionist('Randy Marsh', 'RC002', storage = storage, schedule=schedule)
        ]
    
    def _get_candidates_to_hire_count(self) -> int:
        return 2