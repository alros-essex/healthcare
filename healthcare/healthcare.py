from .healthcare_professional import HealthcareProfessional
from .receptionist import Receptionist

class Healthcare():

    def __init__(self):
        self._healthcare_professionals = []
        self._receptionists = []
    
    def hire(self, professional:HealthcareProfessional):
        self._healthcare_professionals.append(professional)

    def hire(self, receptionist: Receptionist):
        self._receptionists.append(receptionist)


    