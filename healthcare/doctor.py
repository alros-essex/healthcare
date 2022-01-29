import random
from enum import Enum

from .employee_role import EmployeeRole
from .healthcare_professional import HealthcareProfessional
from .patient import Patient

class Doctor(HealthcareProfessional):
    """
    Models a doctor
    """
    def __init__(self, name:str, employee_number:str):
        """creates the instance
        
        Args:
            name: employee's name
            employee_number: employee's number
        Returns:
            None
        """
        super().__init__(name, employee_number, EmployeeRole.DOCTOR)

    _consultation_results = [
        'Medical history and symptoms of {} were evaluated',
        'Planned patient care for {}',
        'Diagnosed health problem of {}',
        'Symptoms of {} were evaluated',
        'Medications and treatments were administered to {}',
        'Medical procedure performed on {}',
        'Diagnostic tests were performed on {}',
        'Gave instructions about management of illnesses to {}',
        'Gave good news to {}'
    ]

    def consultation(self, patient:Patient) -> str:
        '''conducts a consultation
        
        Args:
            patient: patient
        Returns:
            str: result of the consultation
        '''
        return self._consultation_results[random.randint(0, len(self._consultation_results)-1)].format(patient.firstname+' '+patient.surname)

    _frequency = ['once a day','once a week','every two days','before meals']
    _type = ['Javalin','Pythoxib','Kothlinax','Rubyonrailaxetate','Prologlin','Rustolin','Malbolgex']
    _dosages = ['half pill','one pill','two pills']

    def issue_prescription(self, patient:Patient):
        '''prescribe a drug
        
        Args:
            None
        Returns:
            str: name of the drug
        '''
        from .prescription import Prescription
        drug = self._pick_random(self._type)
        dosage = self._pick_random(self._dosages)
        frequency = self._pick_random(self._frequency)
        return Prescription(drug, patient, self, random.randint(1, 5), '{} {}'.format(dosage, frequency))

    def _pick_random(self, values):
        return values[random.randint(1, len(values)-1)]