from .init_hiring_staff import InitHiringStaff

class InitReceptionists(InitHiringStaff):
    """template class for Init Hiring Staff"""
    
    def _get_type_of_staff(self):
        return 'receptionists'

    def _get_candidates_to_hire(self):
        from healthcare.receptionist import Receptionist
        return [
            Receptionist('Pam Beesly', 'RC001'),
            Receptionist('Randy Marsh', 'RC002')
        ]
    
    def _get_candidates_to_hire_count(self) -> int:
        return 2