from abc import abstractmethod, ABC

from .employee_role import EmployeeRole

from .employee import Employee

class HealthcareProfessional(Employee, ABC):
    """base class for healthcare professionals"""

    def __init__(self, name: str, employee_number: str, role:EmployeeRole):
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
    def role(self) -> EmployeeRole:
        return self._role