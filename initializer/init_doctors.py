from healthcare.doctor import Doctor
from .init_hiring_staff import InitHiringStaff

class InitDoctors(InitHiringStaff):
    """template class for Init Hiring Staff"""

    def _get_type_of_staff(self):
        return 'doctors'

    def _get_candidates_to_hire(self):
        return [
            Doctor('James Kildare', 'DR001'),
            Doctor('Gregory House', 'DR002'),
            Doctor('Augustus Bedford Forrest', 'DR003'),
            Doctor('Benjamin Franklin Pierce', 'DR004')
        ]
    
    def _get_candidates_to_hire_count(self) -> int:
        return 4
