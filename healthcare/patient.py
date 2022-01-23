class Patient():
    """
    Models a patient of the clinic
    """
    def __init__(self, firstname:str, surname:str, address:str, phone:str):
        """creates the instance
        
        Args:
            firstname: patient's first name
            surname: patient's surname
            address: patient's address
            phone: patient's phone
        Returns:
            None
        """
        self._name = ', '.join([surname, firstname])
        self._firstname = firstname
        self._surname = surname
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

    @property
    def firstname(self):
        return self._firstname

    @property
    def surname(self):
        return self._surname

    def __lt__(self, other):
        return other is not None and self.name < other.name
    
    def __le__(self, other):
        return other is not None and self.name <= other.name

    def __eq__(self, other):
        return other is not None and self.name == other.name
    
    def __ne__(self, other):
        return other is not None and self.name != other.name
    
    def __gt__(self, other):
        return other is not None and self.name > other.name
    
    def __ge__(self, other):
        return other is not None and self.name >= other.name

    def __str__(self) -> str:
        return self.name