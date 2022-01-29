from .doctor import Doctor
from .patient import Patient

class Prescription():
    """
    Represents a prescription for a patient
    """
    def __init__(self, type:str, patient:Patient, doctor:Doctor, quantity:int, dosage:str):
        """creates the instance
        
        Args:
            type: type of the prescription
            patient: patient receiving the prescription
            doctor: doctor issuing the prescription
            quantity: amount
            dosage: how to dose it
        Returns:
            None
        """
        self._type = type
        self._patient = patient
        self._doctor = doctor
        self._quantity = quantity
        self._dosage = dosage

    @property
    def type(self) -> str:
        return self._type

    @property
    def patient(self):
        return self._patient
    
    @property
    def doctor(self):
        return self._doctor

    @property
    def quantity(self):
        return self._quantity

    @property
    def dosage(self):
        return self._dosage

    def __str__(self) -> str:
        return '{quantity} packets, {type} {dosage}'.format(
            quantity = self.quantity, type = self.type, dosage = self.dosage)