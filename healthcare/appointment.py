from healthcare_processional import HealthcareProfessional
from patient import Patient

class Appointment():
    """
    Represents an appointment
    """
    def __init__(self, type:str, staff:HealthcareProfessional, patient:Patient):
        """creates the instance
        
        Args:
            type: appointment type
            staff: member of staff who will receive the patient
            patient: patient who booked the appoitment
        Returns:
            None
        """
        self._type = type
        self._staff = staff
        self._patient = patient

    @property
    def type(self):
        return self._type

    @property
    def staff(self):
        return self._staff

    @property
    def patient(self):
        return self._patient