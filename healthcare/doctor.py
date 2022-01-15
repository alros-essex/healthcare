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
        super().__init__(name, employee_number)

    def consultation(self):
        pass

    def issue_prescription(self):
        pass

