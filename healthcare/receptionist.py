class Receptionist():
    """
    Models a receptionist
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

    def make_appointment(self):
        pass

    def cancel_appointment(self):
        pass