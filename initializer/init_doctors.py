from healthcare.doctor import Doctor
from healthcare.storage import Storage
from .init_hiring_staff import InitHiringStaff

class InitDoctors(InitHiringStaff):
    def _get_type_of_staff(self):
        return 'doctors'

    def _get_candidates_to_hire(self, storage:Storage, schedule):
        return [
            Doctor('James Kildare', 'DR001', storage),
            Doctor('Gregory House', 'DR002', storage),
            Doctor('Augustus Bedford Forrest', 'DR003', storage),
            Doctor('Benjamin Franklin Pierce', 'DR004', storage)
        ]
    
    def _get_candidates_to_hire_count(self) -> int:
        return 4
