import random

from healthcare.patient import Patient
from .healthcare_professional import HealthcareProfessional

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
        super().__init__(name, employee_number, 'doctor')

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

    _drug_names = [
        'Javalin 1000',
        'Pythoxib 500',
        'Kothlinax 40ml',
        'Rubyonrailaxetate',
        'Prologlin',
        'Rustolin drops',
        'Scalanin 400mg'
        'Visualbasicaxolin',
        'Lispodin',
        'Malbolgex'
    ]

    def consultation(self, patient:Patient) -> str:
        '''conducts a consultation
        
        Args:
            patient: patient
        Returns:
            str: result of the consultation
        '''
        return self._consultation_results[random.randint(0, len(self._consultation_results)-1)].format(patient.firstname+' '+patient.surname)

    def issue_prescription(self) -> str:
        '''prescribe a drug
        
        Args:
            None
        Returns:
            str: name of the drug
        '''
        return self._drug_names[random.randint(0, len(self._drug_names)-1)]

