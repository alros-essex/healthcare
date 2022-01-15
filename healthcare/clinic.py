from .healthcare_professional import HealthcareProfessional
from .doctor import Doctor
from .nurse import Nurse
from .receptionist import Receptionist

class Clinic():

    def __init__(self):
        self._staff = []
    
    def hire(self, professional:HealthcareProfessional):
        self._staff.append(professional)

    def hire(self, receptionist: Receptionist):
        self._staff.append(receptionist)

    @property
    def doctors(self):
        return self._get_by_type(Doctor)

    @property
    def nurses(self):
        return self._get_by_type(Nurse)

    @property
    def receptionists(self):
        return self._get_by_type(Receptionist)

    def _get_by_type(self, type):
        return list(filter(lambda staff: isinstance(staff,type), self._staff))

    