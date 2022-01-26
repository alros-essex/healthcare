from datetime import datetime

from .appointment_type import AppointmentType
from .healthcare_professional import HealthcareProfessional
from .patient import Patient

class Appointment():
    """
    Represents an appointment
    """
    def __init__(self, type:AppointmentType, staff:HealthcareProfessional, patient:Patient, date:datetime):
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
    def type(self) -> AppointmentType:
        return self._type

    @property
    def staff(self) ->HealthcareProfessional:
        return self._staff

    @property
    def patient(self) -> Patient:
        return self._patient

    @property
    def date(self) -> datetime:
        return self._date

    def is_on(self, filter_date:datetime.date) -> bool:
        return self.date.year == filter_date.year and self.date.month == filter_date.month and self.date.day == filter_date.day

    def __lt__(self, other) -> bool:
        return self.date < other.date
    
    def __le__(self, other) -> bool:
        return self.date <= other.date

    def __eq__(self, other) -> bool:
        return self.date == other.date
    
    def __ne__(self, other) -> bool:
        return self.date != other.date
    
    def __gt__(self, other) -> bool:
        return self.date > other.date
    
    def __ge__(self, other) -> bool:
        return self.date >= other.date

    def __str__(self) -> str:
        return "{staff} with {patient} - {date}".format(
            staff=self.staff,patient=self.patient,date=self.date,type=self.type)