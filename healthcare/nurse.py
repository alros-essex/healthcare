from healthcare_processional import HealthcareProfessional

class Nurse(HealthcareProfessional):
    """
    Models a nurse
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