from abc import abstractmethod, ABCMeta

class HealthcareProfessional(metaclass=ABCMeta):
    """
    Base class for healthcare professionals
    """
    def __init__(self, name:str, employee_number:str):
        """creates the instance
        
        Args:
            name: employee's name
            employee_number: employee's number
        Returns:
            None
        """
        self._name = name
        self._employee_number = employee_number

    @property
    def name(self):
        return self._name

    @property
    def employee_number(self):
        return self._employee_number

    @abstractmethod
    def consultation(self):
        """Conducts a consultation
        
        Args:
            None
        Returns:
            Array of String: results of the consultation
        """
        pass