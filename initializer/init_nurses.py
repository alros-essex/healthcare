from healthcare.nurse import Nurse

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
