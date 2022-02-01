import random
from .employee_role import EmployeeRole
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
        super().__init__(name, employee_number, EmployeeRole.DOCTOR)
        from .storage import Storage
        self._storage = Storage.instance()

    # possible results of the consultations
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

    def consultation(self, patient) -> str:
        """conducts a consultation
        
        Args:
            patient: Patient
        Returns:
            str: result of the consultation
        """
        if len(patient.prescriptions)==0 or random.randint(1,2)==1:
            prescription = self.issue_prescription(patient)
            return 'Gave a prescription of {}'.format(prescription)
        return self._consultation_results[random.randint(0, len(self._consultation_results)-1)].format(patient.name)

    # possible prescriptions
    _type = ['Javalin','Pythonxib','Kothlinax','Rubyonrailaxetate','Prologlin','Rustolin','Malbolgex']

    def issue_prescription(self, patient):
        """prescribe a drug
        
        Args:
            patient: Patient requiring a prescription
        Returns:
            Prescription
        """
        from .prescription import Prescription
        candidates = [d for d in self._type if d not in patient.prescriptions]
        if len(candidates)==0:
            # patients already has all possible prescriptions!
            return None
        prescription = Prescription(random.choice(candidates), patient, self, random.randint(1, 5), float(random.randint(100, 10000))/100)
        patient.accept_prescription(prescription)
        self._storage.insert_prescription(prescription)
        return prescription

    def patients(self):
        return self._storage.select_patients(self)

    def approve_repeat(self, prescription) -> bool:
        return True