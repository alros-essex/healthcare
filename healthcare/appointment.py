from datetime import datetime
from .healthcare_professional import HealthcareProfessional
from .patient import Patient

class Appointment():
    """
    Represents an appointment
    """
    def __init__(self, type:str, staff:HealthcareProfessional, patient:Patient, date:datetime):
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
        self._date = date

    @property
    def type(self):
        return self._type

    @property
    def staff(self):
        return self._staff

    @property
    def patient(self):
        return self._patient

    @property
    def date(self):
        return self._date

    def __lt__(self, other):
        return self.date < other.date
    
    def __le__(self, other):
        return self.date <= other.date

    def __eq__(self, other):
        return self.date == other.date
    
    def __ne__(self, other):
        return self.date != other.date
    
    def __gt__(self, other):
        return self.date > other.date
    
    def __ge__(self, other):
        return self.date >= other.date