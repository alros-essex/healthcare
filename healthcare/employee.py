from abc import abstractmethod, ABC

class Employee(ABC):
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

    @property
    @abstractmethod
    def role(self):
        pass

    def __str__(self):
        return '{}'.format(self.name)
