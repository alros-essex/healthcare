from abc import abstractmethod, ABC
from .employee import Employee

class HealthcareProfessional(Employee, ABC):
    """base class for healthcare professionals"""

    def __init__(self, name: str, employee_number: str, role):
        super().__init__(name, employee_number)
        self._role = role

    @abstractmethod
    def consultation(self, patient):
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