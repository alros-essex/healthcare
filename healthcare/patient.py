class Patient():
    """
    Models a patient of the clinic
    """
    def __init__(self, name:str, surname:str, address:str, phone:str):
        """creates the instance
        
        Args:
            name: patient's name
            surname: patient's surname
            address: patient's address
            phone: patient's phone
        Returns:
            None
        """
        self._name = ', '.join([surname, name])
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

    def __lt__(self, other):
        return self.name < other.name
    
    def __le__(self, other):
        return self.name <= other.name

    def __eq__(self, other):
        return self.name == other.name
    
    def __ne__(self, other):
        return self.name != other.name
    
    def __gt__(self, other):
        return self.name > other.name
    
    def __ge__(self, other):
        return self.name >= other.name