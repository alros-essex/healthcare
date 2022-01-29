from .init_hiring_staff import InitHiringStaff

from healthcare.receptionist import Receptionist
from healthcare.appointment_schedule import AppointmentSchedule

class InitReceptionists(InitHiringStaff):
    def _get_type_of_staff(self):
        return 'receptionists'

    def _get_candidates_to_hire(self):
        return [
            Receptionist('Pam Beesly', 'RC001'),
            Receptionist('Randy Marsh', 'RC002')
        ]