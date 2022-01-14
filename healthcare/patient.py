class Patient():
    """
    Models a patient of the clinic
    """
    def __init__(self, name:str, address:str, phone:str):
        """creates the instance
        
        Args:
            name: patient's name
            address: patient's address
            phone: patient's phone
        Returns:
            None
        """
        self._name = name
        self._address = address
        self._phone = phone

    @property
    def name(self):
        return self._name

    @property
    def address(self):
        return self._address

    @property
    def phone(self):
        return self._phone