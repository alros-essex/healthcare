from healthcare.appointment_schedule import AppointmentSchedule
from healthcare.nurse import Nurse
from healthcare.storage import Storage

from .init_hiring_staff import InitHiringStaff

class InitNurses(InitHiringStaff):
    def _get_type_of_staff(self):
        return 'nurses'

    def _get_candidates_to_hire(self):
        return [
            Nurse('Haleh Adams', 'NR001'),
            Nurse('Carla Espinosa', 'NR002'),
            Nurse('Rory Williams', 'NR003'),
            Nurse('Mildred Ratched', 'NR004')
        ]

    def _get_candidates_to_hire_count(self) -> int:
        return 4