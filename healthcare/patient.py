from healthcare.prescription import Prescription


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
        self._prescriptions = {}

    @property
    def name(self):
        return self._name

    @property
    def address(self):
        return self._address

    @property
    def phone(self):
        return self._phone

    def request_repeat(self, doctor):
        for p in self.prescriptions.values():
            doctor.approve_repeat(p)

    def request_appointment(self) -> None:
        # TODO
        pass

    def accept_prescription(self, prescription:Prescription) -> None:
        self._prescriptions[prescription.type] = prescription

    @property
    def prescriptions(self):
        return self._prescriptions

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