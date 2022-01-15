from abc import abstractmethod, ABC

from .employee import Employee

class HealthcareProfessional(Employee, ABC):

    def __init__(self, name: str, employee_number: str):
        super().__init__(name, employee_number)

    @abstractmethod
    def consultation(self):
        """Conducts a consultation
        
        Args:
            None
        Returns:
            Array of String: results of the consultation
        """
        pass