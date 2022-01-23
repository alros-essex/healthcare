from abc import abstractmethod, ABC

from healthcare.patient import Patient

from .employee import Employee

class HealthcareProfessional(Employee, ABC):

    def __init__(self, name: str, employee_number: str, role:str):
        super().__init__(name, employee_number)
        self._role = role

    @abstractmethod
    def consultation(self, patient:Patient):
        """Conducts a consultation
        
        Args:
            patient: patient in need
        Returns:
            Array of String: results of the consultation
        """
        pass

    @property
    def role(self):
        return self._role